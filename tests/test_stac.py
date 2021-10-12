import unittest

from stactools.ghcnd import stac
from stactools.ghcnd.constants import DOI, GHCND_EPSG, GHCND_ID, LICENSE


class StacTest(unittest.TestCase):
    def test_create_collection(self):
        collection = stac.create_collection()
        collection.set_self_href("")

        self.assertEqual(collection.id, GHCND_ID)
        self.assertEqual(collection.license, LICENSE)
        self.assertEqual(collection.extra_fields["sci:doi"], DOI)
        self.assertEqual(len(collection.extra_fields["item_assets"]), 3)

        collection.validate()

    def test_create_item(self):
        item = stac.create_item("path/to/files/1900.csv.gz")

        self.assertEqual(item.id, f"GHCNd_{1900}")
        self.assertEqual(item.properties["sci:doi"], DOI)
        self.assertEqual(item.properties["proj:epsg"], GHCND_EPSG)
        self.assertEqual(len(item.assets), 3)

        # Validate
        item.validate()
