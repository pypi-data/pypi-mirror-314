# -*- coding: utf-8; -*-

from unittest import TestCase

import pytest

from rattail import db as mod


class TestModule(TestCase):

    def test_basic(self):
        try:
            from sqlalchemy import orm
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # Session is legitimate
        self.assertTrue(isinstance(mod.Session, orm.sessionmaker))

        # SessionBase warns of deprecation
        # (we don't test for that, just here for the coverage)
        session = mod.SessionBase()
