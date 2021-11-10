import logging

import click

from stactools.ghcnd import stac
from stactools.ghcnd.asset import CreateDataAsset

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
        help="The output path for the STAC Item.",
    )
    def create_item_command(source: str, destination: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): The output path for the STAC Item
        """
        item = stac.create_item(source)
        item.save_object(dest_href=destination)
        item.validate()

        return None

    @ghcnd.command(
        "populate-collection",
        short_help="Populate the GHCNd STAC Collection with all items")
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The source for the data asset.",
    )
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

    @ghcnd.command(
        "create-data-asset",
        short_help="Download and process the source data into the data asset.")
    @click.option(
        "-d",
        "--downloads",
        required=True,
        help="Directory to hold downloads.",
    )
    @click.option(
        "-u",
        "--unzipped",
        required=True,
        help="Directory to hold unzipped files.",
    )
    @click.option(
        "-o",
        "--output_path",
        required=True,
        help="Path for output file (Parquet format).",
    )
    @click.option(
        "-s",
        "--start_year",
        required=False,
        help="Starting year to process (min: 1763, max: current year).",
        default=1763)
    @click.option("-e",
                  "--end_year",
                  required=False,
                  help="Final year to process (min: 1763, max: current year).",
                  default=2021)
    def create_data_asset_command(downloads: str, unzipped: str,
                                  output_path: str, start_year: int,
                                  end_year: int):
        """Download, unzip and process the yearly GHCNd data into one data asset.
         Output is held in Parquet format.

        Args:
            downloads (str): Directory to hold downloads.
            unzipped (str): Directory to hold unzipped files.
            output_path (str): Path for output file (Parquet format).
            start_year (int): Starting year to process (min: 1763, max: current year).
            end_year (int): Final year to process (min: 1763, max: current_year).
        """

        data_asset = CreateDataAsset(downloads, unzipped, output_path)
        data_asset.create_data_asset(start_year, end_year)

        return None

    return ghcnd
