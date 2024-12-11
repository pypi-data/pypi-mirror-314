# -*- coding: utf-8; -*-

import os
import shutil
import decimal
from unittest import TestCase

from rattail.config import RattailConfig
from rattail.excel import ExcelWriter
from rattail.gpc import GPC

try:
    import sqlalchemy as sa
    from rattail.batch import vendorcatalog as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestProductBatchHandler(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.handler = self.make_handler()

        def make_handler(self):
            return mod.VendorCatalogHandler(self.config)

        def test_allow_future(self):

            # off by default
            result = self.handler.allow_future()
            self.assertFalse(result)

            # but can be enabled via config
            self.config.setdefault('rattail.batch', 'vendor_catalog.allow_future',
                                   'true')
            result = self.handler.allow_future()
            self.assertTrue(result)

        def test_populate_from_file(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)
            app = self.config.get_app()

            # we'll need a user to create the batches
            user = model.User(username='ralph')
            session.add(user)

            # make root folder to contain all temp files
            tempdir = app.make_temp_dir()

            # generate sample xlsx file
            path = os.path.join(tempdir, 'sample.xlsx')
            writer = ExcelWriter(path, ['UPC', 'Vendor Code', 'Unit Cost'])
            writer.write_header()
            writer.write_row(['074305001321', '123456', 4.19], row=2)
            writer.save()

            # make, configure folder for batch files
            filesdir = os.path.join(tempdir, 'batch_files')
            os.makedirs(filesdir)
            self.config.setdefault('rattail', 'batch.files', filesdir)

            # make the basic batch
            batch = model.VendorCatalogBatch(uuid=app.make_uuid(),
                                             id=1, created_by=user)
            session.add(batch)

            # batch must have certain attributes, else error
            self.assertRaises(ValueError, self.handler.populate_from_file, batch)
            self.handler.set_input_file(batch, path) # sets batch.filename
            self.assertRaises(ValueError, self.handler.populate_from_file, batch)
            batch.parser_key = 'rattail.contrib.generic'

            # and finally, test our method proper
            self.handler.setup_populate(batch)
            self.handler.populate_from_file(batch)
            self.assertEqual(len(batch.data_rows), 1)
            row = batch.data_rows[0]
            self.assertEqual(row.item_entry, '074305001321')
            self.assertEqual(row.vendor_code, '123456')
            self.assertEqual(row.unit_cost, decimal.Decimal('4.19'))

            shutil.rmtree(tempdir)
            session.rollback()
            session.close()

        def test_identify_product(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)
            app = self.config.get_app()

            # make a test user, vendor, product, cost
            user = model.User(username='ralph')
            session.add(user)
            vendor = model.Vendor()
            session.add(vendor)
            product = model.Product(upc=GPC('074305001321'))
            session.add(product)
            cost = model.ProductCost(vendor=vendor,
                                     code='123456',
                                     case_size=12,
                                     case_cost=decimal.Decimal('54.00'),
                                     unit_cost=decimal.Decimal('4.50'))
            product.costs.append(cost)

            # also a batch to contain the rows
            batch = model.VendorCatalogBatch(uuid=app.make_uuid(),
                                             id=1, created_by=user,
                                             vendor=vendor,
                                             filename='sample.xlsx',
                                             parser_key='rattail.contrib.generic')
            session.add(batch)

            # row w/ no interesting attributes cannot yield a product
            row = model.VendorCatalogBatchRow()
            batch.data_rows.append(row)
            result = self.handler.identify_product(row)
            self.assertIsNone(result)

            # but if we give row a upc, product is found
            row.upc = GPC('074305001321')
            result = self.handler.identify_product(row)
            self.assertIs(result, product)

            # now try one with vendor code instead of upc
            row = model.VendorCatalogBatchRow(vendor_code='123456')
            batch.data_rows.append(row)
            result = self.handler.identify_product(row)
            self.assertIs(result, product)

            session.rollback()
            session.close()

        def test_refresh_row(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)
            app = self.config.get_app()

            # make a test user, vendor, product
            user = model.User(username='ralph')
            session.add(user)
            vendor = model.Vendor()
            session.add(vendor)
            product = model.Product(upc=GPC('074305001321'))
            session.add(product)

            # also a batch to contain the rows
            batch = model.VendorCatalogBatch(uuid=app.make_uuid(),
                                             id=1, created_by=user,
                                             vendor=vendor,
                                             filename='sample.xlsx',
                                             parser_key='rattail.contrib.generic')
            session.add(batch)

            # empty row is just marked as product not found
            row = model.VendorCatalogBatchRow()
            batch.data_rows.append(row)
            self.handler.refresh_row(row)
            self.assertEqual(row.status_code, row.STATUS_PRODUCT_NOT_FOUND)

            # row with upc is matched with product; also make sure unit
            # cost is calculated from case cost
            row = model.VendorCatalogBatchRow(upc=GPC('074305001321'),
                                              case_size=12,
                                              case_cost=decimal.Decimal('58.00'))
            batch.data_rows.append(row)
            self.handler.refresh_row(row)
            self.assertIs(row.product, product)
            self.assertEqual(row.status_code, row.STATUS_NEW_COST)
            self.assertEqual(row.case_cost, 58)
            self.assertEqual(row.case_size, 12)
            self.assertEqual(row.unit_cost, decimal.Decimal('4.8333'))

            # now we add a cost to the master product, and make sure new
            # row will reflect an update for that cost
            cost = model.ProductCost(vendor=vendor, 
                                     case_size=12,
                                     case_cost=decimal.Decimal('54.00'),
                                     unit_cost=decimal.Decimal('4.50'))
            product.costs.append(cost)
            row = model.VendorCatalogBatchRow(upc=GPC('074305001321'),
                                              case_size=12,
                                              case_cost=decimal.Decimal('58.00'))
            batch.data_rows.append(row)
            self.handler.refresh_row(row)
            self.assertIs(row.product, product)
            self.assertEqual(row.status_code, row.STATUS_CHANGE_COST)
            self.assertEqual(row.old_case_cost, 54)
            self.assertEqual(row.case_cost, 58)
            self.assertEqual(row.old_unit_cost, decimal.Decimal('4.50'))
            self.assertEqual(row.unit_cost, decimal.Decimal('4.8333'))

            # and finally let's refresh everything, note that row #2
            # should now *also* get "change cost" status
            row = batch.data_rows[1]
            self.assertEqual(row.status_code, row.STATUS_NEW_COST)
            self.handler.setup_refresh(batch)
            for row in batch.data_rows:
                self.handler.refresh_row(row)
            self.assertEqual(row.status_code, row.STATUS_CHANGE_COST)

            session.rollback()
            session.close()
