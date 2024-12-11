# -*- coding: utf-8; -*-

from rattail.trainwreck import config as mod
from rattail.testing import DataTestCase

try:
    import sqlalchemy
except ImportError:
    pass
else:

    class TestTrainwreckConfig(DataTestCase):

        def test_configure(self):
            self.assertFalse(hasattr(self.config, 'trainwreck_engines'))
            ext = mod.TrainwreckConfig()
            ext.configure(self.config)
            self.assertEqual(self.config.trainwreck_engines, {})
