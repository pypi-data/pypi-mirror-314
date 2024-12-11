"""STAC stuff."""

import pystac
from pystac import Collection, ItemCollection, Item

from .logger import logger
from urllib.parse import urljoin
from typing import List
import os
import dinamis_sdk
import requests
from requests.adapters import HTTPAdapter, Retry
from dataclasses import dataclass


class STACObjectUnresolved(Exception):
    pass


class UnconsistentCollectionIDs(Exception):
    pass


def create_session():
    """Create a requests session"""
    sess = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[400, 403, 408, 410, 419, 421, 422,
                          424, 425, 429, 500, 502, 503, 504, 505],
        allowed_methods=frozenset(["PUT", "POST"])
    )
    adapter = HTTPAdapter(max_retries=retries)
    sess.mount("http://", adapter=adapter)
    sess.mount("https://", adapter=adapter)
    return sess


def post_or_put(url: str, data: dict):
    """Post or put data to url."""
    headers = {
        "Authorization": f"Bearer {dinamis_sdk.auth.get_access_token()}"
    }
    sess = create_session()
    resp = sess.post(url, json=data, headers=headers)
    if resp.status_code == 409:
        # Exists, so update
        resp = sess.put(
            url if data["type"] == "Collection" else url + f"/{data['id']}",
            json=data,
            headers=headers
        )
        # Unchanged may throw a 404
        if not resp.status_code == 404:
            resp.raise_for_status()
    else:
        try:
            resp.raise_for_status()
        except Exception as e:
            logger.error(eval(resp.content)["detail"])
            raise(e)


def load(obj_pth):
    """Load a STAC object serialized on disk."""
    for obj_name, cls in {
        "collection": Collection,
        "item collection": ItemCollection,
        "item": Item
    }.items():
        logger.debug("Try to read file %s", obj_pth)
        try:
            obj = getattr(cls, "from_file")(obj_pth)
            logger.info("Loaded %s from file %s", obj_name, obj_pth)
            logger.debug(obj.to_dict())
            return obj
        except pystac.errors.STACTypeError:
            pass

    raise STACObjectUnresolved(f"Cannot resolve STAC object ({obj_pth})")


def get_assets_root_dir(items: List[Item]) -> str:
    """Get the common prefix of all items assets paths."""
    prefix = os.path.commonprefix([
        asset.href
        for item in items
        for asset in item.assets.values()
    ])
    if os.path.isdir(prefix):
        return prefix
    return os.path.dirname(prefix)


def check_items_collection_id(items: List[Item]):
    """Check that items collection_id is unique"""
    if len(set(item.collection_id for item in items)) != 1:
        raise UnconsistentCollectionIDs(
            "Collection ID must be the same for all items!"
        )


def get_col_href(col: Collection):
    """Retrieve collection href."""
    for link in col.links:
        if link.rel == "self":
            return link.href


def get_col_items(col: Collection) -> List[Item]:
    """Retrieve collection items."""
    col_href = get_col_href(col=col)
    return [
        load(
            os.path.join(
                os.path.dirname(col_href),
                link.href[2:]
            ) if link.href.startswith("./") else link.href
        )
        for link in col.links
        if link.rel == "item"
    ]


@dataclass
class TransactionsHandler:
    """Handle STAC and storage transactions."""
    stac_endpoint: str
    storage_endpoint: str
    storage_bucket: str
    assets_overwrite: bool

    def publish_item(self, item: Item, assets_root_dir: str):
        """Publish an item and all its assets"""
        col_id = item.collection_id
        target_root_dir = urljoin(
            self.storage_endpoint,
            self.storage_bucket,
            col_id
        )

        # Upload assets files
        for asset_name, asset in item.assets.items():
            local_filename = asset.href
            logger.debug("Local file: %s", local_filename)
            target_url = local_filename.replace(
                assets_root_dir,
                target_root_dir
            )
            logger.debug("Target file: %s", target_url)

            # Skip when target file exists and overwrite is not enabled
            if not self.assets_overwrite:
                sess = create_session()
                if sess.get(
                        dinamis_sdk.sign(target_url),
                        stream=True
                ).status_code == 200:
                    logger.info(
                        "Asset %s already exists. Skipping.",
                        target_url
                    )
                    continue

            # Upload file
            logger.info("Uploading %s ...", local_filename)
            try:
                dinamis_sdk.push(
                    local_filename=local_filename,
                    target_url=target_url
                )
            except Exception as e:
                logger.error(e)
                raise(e)

            # Update assets hrefs
            logger.debug("Updating assets HREFs ...")
            asset.href = target_url

        # Push item
        logger.info(
            "Publishing item \"%s\" in collection \"%s\"",
            item.id,
            col_id
        )
        post_or_put(
            urljoin(
                self.stac_endpoint,
                f"collections/{col_id}/items"
            ),
            item.to_dict(transform_hrefs=False)
        )

    def publish_items(self, items: List[Item]):
        """Publish items."""
        check_items_collection_id(items=items)
        assets_root_dir = get_assets_root_dir(items=items)
        logger.debug("Assets root directory: %s", assets_root_dir)
        for item in items:
            self.publish_item(
                item=item,
                assets_root_dir=assets_root_dir
            )

    def publish_collection(self, collection: Collection):
        """Publish an empty collection"""
        post_or_put(
            url=urljoin(self.stac_endpoint, "/collections"),
            data=collection.to_dict()
        )

    def publish_collection_with_items(self, collection: Collection):
        """Publish a collection and all its items."""
        items = get_col_items(col=collection)
        check_items_collection_id(items)
        self.publish_collection(collection=collection)
        self.publish_items(items=items)

    def publish_item_collection(self, item_collection: ItemCollection):
        """Publish an item collection and all of its items."""
        self.publish_items(items=item_collection.items)

    def load_and_publish(self, obj_pth: str):
        """Load and publish the serialized STAC object"""
        obj = load(obj_pth=obj_pth)
        if isinstance(obj, Collection):
            self.publish_collection_with_items(collection=obj)
        elif isinstance(obj, ItemCollection):
            self.publish_item_collection(item_collection=obj)
        else:
            raise TypeError(
                "Invalid type, must be ItemCollection or Collection "
                f"(got {type(obj)})"
            )

    def delete(self, col_id: str, item_id: str = None):
        """Delete an item or a collection."""
        logger.info("Delete item %s", item_id)
        if item_id:
            url = f"{self.stac_endpoint}/collections/{col_id}/items/{item_id}"
        else:
            url = f"{self.stac_endpoint}/collections/{col_id}"
        resp = requests.delete(
            url,
            headers={
                "Authorization":
                    f"Bearer {dinamis_sdk.auth.get_access_token()}"
            }
        )
        if resp.status_code != 200:
            logger.warning("Deletion failed")
