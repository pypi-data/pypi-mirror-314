# -*- coding: utf-8; -*-

from unittest import TestCase

import pytest

from rattail import products as mod
from rattail.config import RattailConfig
from rattail.gpc import GPC
from rattail.db import Session


class TestProductsHandler(TestCase):

    def setUp(self):
        self.config = RattailConfig()
        self.app = self.config.get_app()
        self.handler = self.make_handler()

    def make_handler(self):
        return mod.ProductsHandler(self.config)

    def test_make_gpc(self):

        # basic real-world example
        result = self.handler.make_gpc('074305001321')
        self.assertIsInstance(result, GPC)
        self.assertEqual(str(result), '00074305001321')

        # and let it calculate check digit
        result = self.handler.make_gpc('7430500132', calc_check_digit='upc')
        self.assertIsInstance(result, GPC)
        self.assertEqual(str(result), '00074305001321')

        # can also pass integer, and let it auto-calc check digit
        # (b/c data length makes it clear check digit is missing)
        result = self.handler.make_gpc(7430500132)
        self.assertIsInstance(result, GPC)
        self.assertEqual(str(result), '00074305001321')

        # bad one should raise error
        self.assertRaises(ValueError, self.handler.make_gpc, 'BAD_VALUE')

        # unless we suppress errors
        result = self.handler.make_gpc('BAD_VALUE', ignore_errors=True)
        self.assertIsNone(result)

    def test_make_full_description(self):
        try:
            model = self.app.model
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        # basic example
        result = self.handler.make_full_description(
            brand_name="Bragg's",
            description="Apple Cider Vinegar",
            size="32oz")
        self.assertEqual(result, "Bragg's Apple Cider Vinegar 32oz")

        # product example
        product = model.Product(
            brand=model.Brand(name="Bragg's"),
            description="Apple Cider Vinegar",
            size="32oz")
        result = self.handler.make_full_description(product)
        self.assertEqual(result, "Bragg's Apple Cider Vinegar 32oz")

        # pending product example
        product = model.PendingProduct(
            brand_name="Bragg's",
            description="Apple Cider Vinegar",
            size="32oz")
        result = self.handler.make_full_description(product)
        self.assertEqual(result, "Bragg's Apple Cider Vinegar 32oz")

    def test_get_case_size(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # no case size by default
        product = model.Product()
        result = self.handler.get_case_size(product)
        self.assertIsNone(result)

        # main attr example
        product = model.Product(case_size=12)
        result = self.handler.get_case_size(product)
        self.assertEqual(result, 12)

        # cost attr example
        product = model.Product()
        vendor = model.Vendor()
        product.costs.append(model.ProductCost(vendor=vendor,
                                               case_size=24))
        session.add(product)
        session.flush()
        result = self.handler.get_case_size(product)
        self.assertEqual(result, 24)

    def test_get_url(self):
        try:
            model = self.app.model
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        app = self.config.get_app()

        # no url by default
        product = model.Product()
        result = self.handler.get_url(product)
        self.assertIsNone(result)

        # basic example
        self.config.setdefault('rattail', 'base_url', 'http://example.com')
        uuid = app.make_uuid()
        product = model.Product(uuid=uuid)
        result = self.handler.get_url(product)
        self.assertEqual(result, 'http://example.com/products/{}'.format(uuid))

    def test_locate_product_for_alt_code(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        product1 = model.Product()
        product1.codes.append('12345')
        session.add(product1)
        product2 = model.Product()
        product2.codes.append('67890')
        session.add(product2)
        session.flush()

        # unknown code returns nothing
        result = self.handler.locate_product_for_alt_code(session, 'bogus')
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_alt_code(session, '12345')
        self.assertIs(result, product1)

    def test_locate_product_for_vendor_code(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        vendor = model.Vendor()
        product1 = model.Product()
        product1.costs.append(model.ProductCost(vendor=vendor, code='12345'))
        session.add(product1)
        product2 = model.Product()
        product2.costs.append(model.ProductCost(vendor=vendor, code='67890'))
        session.add(product2)
        session.flush()

        # unknown code returns nothing
        result = self.handler.locate_product_for_vendor_code(session, 'bogus')
        self.assertIsNone(result)

        # basic example, w/ vendor restriction
        result = self.handler.locate_product_for_vendor_code(session, '12345',
                                                             vendor=vendor)
        self.assertIs(result, product1)

        # basic example, for any vendor
        result = self.handler.locate_product_for_vendor_code(session, '67890')
        self.assertIs(result, product2)

    def test_locate_product_for_gpc(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        product1 = model.Product(upc=app.make_gpc('00074305001321'))
        session.add(product1)
        product2 = model.Product(upc=app.make_gpc('0021234500000',
                                                  calc_check_digit='upc'))
        session.add(product2)
        session.flush()

        # return nothing if no gpc provided
        result = self.handler.locate_product_for_gpc(session, None)
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_gpc(
            session, app.make_gpc('00074305001321'))
        self.assertIs(result, product1)

        # type2 lookup does not happen by default
        type2 = app.make_gpc('0021234501299', calc_check_digit='upc')
        result = self.handler.locate_product_for_gpc(session, type2)
        self.assertIsNone(result)

        # but we can enable type2 lookup, then it should work
        self.config.setdefault('rattail', 'products.convert_type2_for_gpc_lookup',
                               'true')
        result = self.handler.locate_product_for_gpc(session, type2)
        self.assertIs(result, product2)

    def test_locate_product_for_upc(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        product1 = model.Product(upc=app.make_gpc('00074305001321'))
        session.add(product1)
        product2 = model.Product(upc=app.make_gpc('0021234500000',
                                                  calc_check_digit='upc'))
        session.add(product2)
        product3 = model.Product(upc=app.make_gpc('00035200007122'))
        session.add(product3)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_upc(session, None)
        self.assertIsNone(result)

        # bad data returns nothing
        result = self.handler.locate_product_for_upc(session, 'bogus')
        self.assertIsNone(result)

        # basic UPC-A, with check digit
        result = self.handler.locate_product_for_upc(session, '074305001321')
        self.assertIs(result, product1)

        # UPC-A without check digit
        result = self.handler.locate_product_for_upc(session, '07430500132')
        self.assertIs(result, product1)

        # UPC-E
        result = self.handler.locate_product_for_upc(session, '03571222')
        self.assertIs(result, product3)

        # basic GPC
        result = self.handler.locate_product_for_upc(
            session, app.make_gpc('00074305001321'))
        self.assertIs(result, product1)

        # type2 GPC lookup does not happen by default
        type2 = app.make_gpc('0021234501299', calc_check_digit='upc')
        result = self.handler.locate_product_for_upc(session, type2)
        self.assertIsNone(result)

        # but we can enable type2 lookup, then it should work
        self.config.setdefault('rattail', 'products.convert_type2_for_gpc_lookup',
                               'true')
        result = self.handler.locate_product_for_upc(session, type2)
        self.assertIs(result, product2)

    def test_locate_product_for_item_id(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        product1 = model.Product(item_id='0007430500132')
        session.add(product1)
        product2 = model.Product(item_id='0021234500000')
        session.add(product2)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_item_id(session, None)
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_item_id(session, '0007430500132')
        self.assertIs(result, product1)

    def test_locate_product_for_scancode(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # setup data
        product1 = model.Product(scancode='074305001321')
        session.add(product1)
        product2 = model.Product(scancode='074305001161')
        session.add(product2)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_scancode(session, None)
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_scancode(session, '074305001321')
        self.assertIs(result, product1)

    def test_locate_product_for_key_upc(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # set upc as product key
        self.config.setdefault('rattail', 'product.key', 'upc')

        # setup data
        product1 = model.Product(upc=app.make_gpc('00074305001321'))
        session.add(product1)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_key(session, None)
        self.assertIsNone(result)

        # basic UPC-A, with check digit
        result = self.handler.locate_product_for_key(session, '074305001321')
        self.assertIs(result, product1)

        # UPC-A without check digit
        result = self.handler.locate_product_for_key(session, '07430500132')
        self.assertIs(result, product1)

    def test_locate_product_for_key_item_id(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # set item_id as product key
        self.config.setdefault('rattail', 'product.key', 'item_id')

        # setup data
        product1 = model.Product(item_id='0007430500132')
        session.add(product1)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_key(session, None)
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_key(session, '0007430500132')
        self.assertIs(result, product1)

    def test_locate_product_for_key_scancode(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # set scancode as product key
        self.config.setdefault('rattail', 'product.key', 'scancode')

        # setup data
        product1 = model.Product(scancode='074305001321')
        session.add(product1)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_key(session, None)
        self.assertIsNone(result)

        # basic example
        result = self.handler.locate_product_for_key(session, '074305001321')
        self.assertIs(result, product1)

    def test_locate_product_for_entry(self):
        try:
            import sqlalchemy as sa
        except ImportError:
            pytest.skip("test is not relevant without sqlalchemy")

        engine = sa.create_engine('sqlite://')
        model = self.app.model
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        app = self.config.get_app()

        # set upc as product key
        self.config.setdefault('rattail', 'product.key', 'upc')

        # setup data
        vendor = model.Vendor()
        product1 = model.Product(upc=app.make_gpc('00074305001321'))
        session.add(product1)
        product2 = model.Product(upc=app.make_gpc('0021234500000',
                                                  calc_check_digit='upc'))
        session.add(product2)
        product3 = model.Product(upc=app.make_gpc('00035200007122'))
        session.add(product3)
        product4 = model.Product(item_id='42')
        product4.codes.append('4242')
        session.add(product4)
        product5 = model.Product(scancode='074305001161')
        product5.costs.append(model.ProductCost(vendor=vendor, code='12345'))
        session.add(product5)
        session.flush()

        # ask for nothing, get nothing
        result = self.handler.locate_product_for_entry(session, None)
        self.assertIsNone(result)

        # bad data returns nothing
        result = self.handler.locate_product_for_entry(session, 'bogus',
                                                       lookup_fields=[
                                                           'uuid',
                                                           'upc',
                                                           'item_id',
                                                           'scancode',
                                                           'vendor_code',
                                                           'alt_code',
                                                       ])
        self.assertIsNone(result)

        # basic UUID test
        result = self.handler.locate_product_for_entry(session, product5.uuid)
        self.assertIs(result, product5)

        # basic UPC-A, with check digit
        result = self.handler.locate_product_for_entry(session, '074305001321')
        self.assertIs(result, product1)

        # UPC-A without check digit
        result = self.handler.locate_product_for_entry(session, '07430500132')
        self.assertIs(result, product1)

        # UPC-E
        result = self.handler.locate_product_for_entry(session, '03571222')
        self.assertIs(result, product3)

        # basic GPC
        result = self.handler.locate_product_for_entry(
            session, app.make_gpc('00074305001321'))
        self.assertIs(result, product1)

        # type2 GPC lookup does not happen by default
        type2 = app.make_gpc('0021234501299', calc_check_digit='upc')
        result = self.handler.locate_product_for_entry(session, type2)
        self.assertIsNone(result)

        # but we can enable type2 lookup, then it should work
        self.config.setdefault('rattail', 'products.convert_type2_for_gpc_lookup',
                               'true')
        result = self.handler.locate_product_for_entry(session, type2)
        self.assertIs(result, product2)

        # basic item_id test
        result = self.handler.locate_product_for_entry(session, '42',
                                                       lookup_fields=['item_id'])
        self.assertIs(result, product4)

        # basic scancode test
        result = self.handler.locate_product_for_entry(session, '074305001161',
                                                       lookup_fields=['scancode'])
        self.assertIs(result, product5)

        # basic alt code test
        result = self.handler.locate_product_for_entry(session, '4242',
                                                       lookup_fields=['alt_code'])
        self.assertIs(result, product4)

        # basic vendor code test, w/ vendor restriction
        result = self.handler.locate_product_for_entry(session, '12345',
                                                       lookup_fields=['vendor_code'],
                                                       vendor=vendor)
        self.assertIs(result, product5)

        # basic vendor code test, any vendor
        result = self.handler.locate_product_for_entry(session, '12345',
                                                       lookup_fields=['vendor_code'])
        self.assertIs(result, product5)

        # bad lookup field is ignored
        result = self.handler.locate_product_for_entry(session, '12345',
                                                       lookup_fields=['bogus'])
        self.assertIsNone(result)
