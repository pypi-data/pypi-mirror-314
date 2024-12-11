"""Theia-dumper Command Line Interface."""
import click
from .stac import TransactionsHandler


@click.group(help="Theia-dumper CLI")
def app() -> None:
    """Click group for theia-dumper subcommands."""
    pass


@app.command(help="Publish a static STAC object")
@click.argument("stac_obj_path")
@click.option(
    '--stac_endpoint',
    type=str,
    default="https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr"
)
@click.option(
    '--storage_endpoint',
    type=str,
    default="https://s3-data.meso.umontpellier.fr"
)
@click.option(
    '--storage_bucket',
    type=str,
    default="sm1-gdc"
)
@click.option("--overwrite", default=False)
def publish(
        stac_obj_path: str,
        stac_endpoint: str,
        storage_endpoint: str,
        storage_bucket: str,
        overwrite: bool
):
    """Push a STAC object."""
    handler = TransactionsHandler(
        stac_endpoint=stac_endpoint,
        storage_endpoint=storage_endpoint,
        storage_bucket=storage_bucket,
        assets_overwrite=overwrite
    )
    handler.load_and_publish(stac_obj_path)
