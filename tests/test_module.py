import unittest

import stactools.ghcnd


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.ghcnd.__version__)
