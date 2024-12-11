# Theia dumper

<p align="center">
<img src="docs/logo.png" width="320px">
<br>
<a href="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/releases">
<img src="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/badges/release.svg">
</a>
<a href="https://forgemia.inra.fr/cdos-pub/theia-dumper/-/commits/main">
<img src="https://forgemia.inra.fr/cdos-pub/theia-dumper/badges/main/pipeline.svg">
</a>
<a href="LICENSE">
<img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
</a>
</p>

**Theia-dumper** enables to share Spatio Temporal Assets Catalogs (STAC) on the 
THEIA-MTP geospatial data center.

## Quickstart

Installation:

```commandline
pip install theia-dumper  # Install the package from pip

theia_dumper publish /data/stac/collection.json       # Publish collection
theia_dumper publish /data/stac/item_collection.json  # Publish item collection
```

## Usage

### Prerequisites

The user must be allowed to push files and metadata into the spatial data infrastructure:

- Files
- STAC objects

In order to ask the permission to do so, the user must perform a [merge request](https://docs.gitlab.com/ee/user/project/merge_requests/) 
in [this repository](https://forgemia.inra.fr/cdos-pub/admin/cdos-ops), modifying two files 
(here we assure that the user is named `jacques.chirac`!):

- `buckets.json`: add a bucket and a path prefix where the files will be uploaded,

Typically, one should use the `gdc-sm1` bucket, with a path prefix which is not already 
used, e.g.:

```json
    ...,
    "jacques.chirac": [
      {
        "s3_endpoint": "s3-data.meso.umontpellier.fr",
        "buckets": [
            "sm1-gdc/collection1234",
            "sm1-gdc/collection4567", 
            "sm1-gdc/collection_chirac/1", 
            "sm1-gdc/collection_chirac/2"
        ]
      }
    ],
    ...
```

- `transations_rules.json`: itemize the STAC collections IDs that will be created and modified.

```json
    ...,
    "jacques.chirac": [
        "collectionXYZ", 
        "collection123"
    ],
    ...
```

Note that collections IDs and buckets/paths prefixes are completely independant.

### CLI

In the `theia-dumper` CLI, the `--storage_bucket` argument concatenates the actual bucket and 
the path prefix.

For instance if jacques wants to upload a collection in `sm1-gdc/collection1234`, he will have to call:

```commandLine
theia-dumper /home/jacques/stac/collection.json --storage_bucket sm1-gdc/collection1234
```

## Contact

remi cresson @ inrae

