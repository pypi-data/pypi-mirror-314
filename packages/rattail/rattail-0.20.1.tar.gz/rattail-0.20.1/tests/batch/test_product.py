# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.batch import product as mod
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
            return mod.ProductBatchHandler(self.config)

        def test_make_label_batch(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # prep data
            betty = model.User(username='betty')
            prodbatch = model.ProductBatch(id=1, created_by=betty)
            session.add(prodbatch)
            session.commit()

            # make basic label batch
            lblbatch = self.handler.make_label_batch(prodbatch, betty, id=2)
            self.assertIsNotNone(lblbatch)
            self.assertEqual(lblbatch.id, 2)

        def test_make_pricing_batch(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # prep data
            betty = model.User(username='betty')
            prodbatch = model.ProductBatch(id=1, created_by=betty)
            session.add(prodbatch)
            session.commit()

            # make basic pricing batch
            prcbatch = self.handler.make_pricing_batch(prodbatch, betty, id=2)
            self.assertIsNotNone(prcbatch)
            self.assertEqual(prcbatch.id, 2)
