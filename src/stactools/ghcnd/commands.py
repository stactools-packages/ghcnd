import logging

import click

from stactools.ghcnd import stac
from stactools.ghcnd.constants import YEARS_URL

logger = logging.getLogger(__name__)


def create_ghcnd_command(cli):
    """Creates the stactools-ghcnd command line utility."""
    @cli.group(
        "ghcnd",
        short_help=("Commands for working with stactools-ghcnd"),
    )
    def ghcnd():
        pass

    @ghcnd.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output location for the STAC Collection.",
    )
    def create_collection_command(destination: str):
        """Creates a STAC Collection

        Args:
            destination (str): The output folder for the Collection.
        """
        collection = stac.create_collection()
        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)
        collection.validate()

        return None

    @ghcnd.command("create-item", short_help="Create a STAC item")
    @click.option(
        "-s",
        "--source",
        required=True,
        help="HREF of the Asset associated with the Item.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="An HREF for the STAC Collection.",
    )
    def create_item_command(source: str, destination: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
        """
        item = stac.create_item(source)
        item.save_object(dest_href=destination)
        item.validate()

        return None

    @ghcnd.command(
        "populate-collection",
        short_help="Populate the GHCNd STAC Collection with all items")
    @click.option("-s",
                  "--source",
                  required=False,
                  help="The source directory for the Item data assets.",
                  default=YEARS_URL)
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection.",
    )
    def populate_collection_command(source: str, destination: str):
        """Populate the GHCNd STAC Collection with all items

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
        """

        collection = stac.create_collection()

        # Create items for all years in range
        item = stac.create_item(source)
        collection.add_item(item)

        collection.normalize_hrefs(destination)
        collection.save(dest_href=destination)
        collection.validate()

        return None

    return ghcnd
