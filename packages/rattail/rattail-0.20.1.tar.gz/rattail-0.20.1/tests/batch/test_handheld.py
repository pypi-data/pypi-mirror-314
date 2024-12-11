# -*- coding: utf-8; -*-

from unittest import TestCase

from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.db import Session
    from rattail.batch import handheld as mod
except ImportError:
    pass
else:

    class TestHandheldBatchHandler(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.handler = self.make_handler()

        def make_handler(self):
            return mod.HandheldBatchHandler(self.config)

        def test_make_inventory_batch(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # prep data
            betty = model.User(username='betty')
            handbatch = model.HandheldBatch(id=1, created_by=betty)
            session.add(handbatch)
            session.commit()

            # make basic inventory batch
            invbatch = self.handler.make_inventory_batch([handbatch], betty, id=2)
            self.assertIsNotNone(invbatch)
            self.assertEqual(invbatch.id, 2)

        def test_make_label_batch(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)

            # prep data
            betty = model.User(username='betty')
            handbatch = model.HandheldBatch(id=1, created_by=betty)
            session.add(handbatch)
            session.commit()

            # make basic label batch
            lblbatch = self.handler.make_label_batch([handbatch], betty, id=2)
            self.assertIsNotNone(lblbatch)
            self.assertEqual(lblbatch.id, 2)
