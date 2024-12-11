# -*- coding: utf-8; -*-

from unittest import TestCase

import pytest

from rattail.vendors import catalogs as mod
from rattail.config import make_config


class TestCatalogParser(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.app = self.config.get_app()
        self.parser = self.make_parser()

    def make_config(self):
        return make_config([], extend=False)

    def make_parser(self):
        return mod.CatalogParser(self.config)

    def test_key_required(self):

        # someone must define the parser key
        self.assertRaises(NotImplementedError, getattr, self.parser, 'key')

    def test_make_row(self):
        try:
            model = self.app.model
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # make a basic row, it should work
        row = self.parser.make_row()
        self.assertIsInstance(row, model.VendorCatalogBatchRow)
