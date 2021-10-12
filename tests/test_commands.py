import os.path
from pathlib import Path
from tempfile import TemporaryDirectory

import pystac
from stactools.testing import CliTestCase

from stactools.ghcnd.commands import create_ghcnd_command
from stactools.ghcnd.constants import DOI, GHCND_EPSG, GHCND_ID, LICENSE


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_ghcnd_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:

            result = self.run_command(
                ["ghcnd", "create-collection", "-d", tmp_dir])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            self.assertEqual(collection.id, GHCND_ID)
            self.assertEqual(collection.license, LICENSE)
            self.assertEqual(collection.extra_fields["sci:doi"], DOI)
            self.assertEqual(len(collection.extra_fields["item_assets"]), 3)

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            destination = os.path.join(tmp_dir, "item.json")
            result = self.run_command([
                "ghcnd",
                "create-item",
                "-s",
                "path/to/files/1900.csv.gz",
                "-d",
                destination,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item = pystac.read_file(destination)
            self.assertEqual(item.id, f"GHCNd_{1900}")
            self.assertEqual(item.properties["sci:doi"], DOI)
            self.assertEqual(item.properties["proj:epsg"], GHCND_EPSG)
            self.assertEqual(len(item.assets), 3)

            item.validate()

    def test_populate_collection(self):
        with TemporaryDirectory() as tmp_dir:
            result = self.run_command([
                "ghcnd", "populate-collection", "-d", tmp_dir, "-st", "1900",
                "-e", "1910"
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in Path(tmp_dir).rglob('*.json')]
            self.assertEqual(len(jsons), 12)
