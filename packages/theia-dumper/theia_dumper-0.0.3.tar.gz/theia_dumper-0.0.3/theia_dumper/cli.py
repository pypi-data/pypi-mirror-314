"""Theia-dumper Command Line Interface."""
import click
from .stac import TransactionsHandler


@click.group()
def theia_dumper() -> None:
    pass

@theia_dumper.command(context_settings={'show_default': True})
@click.argument("stac_obj_path")
@click.option(
    '--stac_endpoint',
    help="Endpoint to which STAC objects will be sent",
    type=str,
    default="https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr"
)
@click.option(
    '--storage_endpoint',
    type=str,
    help="Storage endpoint assets will be sent to",
    default="https://s3-data.meso.umontpellier.fr"
)
@click.option(
    '-b',
    '--storage_bucket',
    help="Storage bucket assets will be sent to",
    type=str,
    default="sm1-gdc"
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite assets if already existing")
def publish(
        stac_obj_path: str,
        stac_endpoint: str,
        storage_endpoint: str,
        storage_bucket: str,
        overwrite: bool
):
    """
    Publish a STAC object (collection or item collection)
    """
    handler = TransactionsHandler(
        stac_endpoint=stac_endpoint,
        storage_endpoint=storage_endpoint,
        storage_bucket=storage_bucket,
        assets_overwrite=overwrite
    )
    handler.load_and_publish(stac_obj_path)
