# -*- coding: utf-8; -*-

try:
    from rattail.db import model
    from ... import DataTestCase
except ImportError:
    pass
else:

    class TestDataSyncChange(DataTestCase):

        def test_unicode(self):
            change = model.DataSyncChange()
            self.assertEqual(str(change), "(empty)")

            change = model.DataSyncChange(payload_type='Product', payload_key='00074305001321')
            self.assertEqual(str(change), "Product: 00074305001321")

            change = model.DataSyncChange(payload_type='Product', payload_key='00074305001321', deletion=True)
            self.assertEqual(str(change), "Product: 00074305001321 (deletion)")
