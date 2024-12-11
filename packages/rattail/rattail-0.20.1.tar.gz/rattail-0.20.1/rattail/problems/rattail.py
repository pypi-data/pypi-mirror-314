# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Problem Reports for Rattail Systems
"""

import datetime

from rattail.problems import ProblemReport


class RattailProblemReport(ProblemReport):
    """
    Base class for problem reports pertaining to a Rattail systems.
    """
    system_key = 'rattail'


class DuplicatedProductKeys(RattailProblemReport):
    """
    Checks for duplicated product keys.

    This report is only useful if you expect to *not* have any product
    keys duplicated in your system.
    """
    problem_key = 'duplicated_product_keys'
    problem_title = "Duplicated product keys"

    def find_problems(self, **kwargs):
        """ """
        problems = []
        keys = {}

        session = self.app.make_session()
        model = self.app.model

        field = self.app.get_product_key_field()
        prop = getattr(model.Product, field)

        products = session.query(model.Product)\
                          .filter(prop != None)\
                          .order_by(prop)\
                          .all()

        def organize(product, i):
            key = getattr(product, field)
            keys.setdefault(key, []).append(product)

        self.progress_loop(organize, products,
                           message="Organizing products by key")

        def inspect(key, i):
            products = keys[key]
            if len(products) > 1:

                # nb. pre-cache some data for report
                for product in products:
                    product.brand

                problems.append((key, products))

        self.progress_loop(inspect, keys,
                           message="Finding duplicated keys")

        session.close()
        return problems

    def get_email_context(self, problems, **kwargs):
        """ """
        kwargs = super().get_email_context(problems, **kwargs)

        kwargs['product_key_label'] = self.app.get_product_key_label()

        return kwargs


class PendingProducts(RattailProblemReport):
    """
    Shows list of pending product records, if any present.
    """
    problem_key = 'pending_products'
    problem_title = "Pending products"

    def find_problems(self, **kwargs):
        session = self.app.make_session()
        model = self.model

        pending = session.query(model.PendingProduct)\
                         .filter(model.PendingProduct.status_code == self.enum.PENDING_PRODUCT_STATUS_PENDING)\
                         .all()

        ready = session.query(model.PendingProduct)\
                       .filter(model.PendingProduct.status_code == self.enum.PENDING_PRODUCT_STATUS_READY)\
                       .all()

        session.close()
        problems = pending + ready
        return problems

    def get_email_context(self, problems, **kwargs):
        kwargs = super().get_email_context(problems, **kwargs)

        kwargs['products_handler'] = self.app.get_products_handler()

        url = self.config.base_url()
        if url:
            url = f'{url}/products/pending/'
        kwargs['url'] = url

        return kwargs


class ProductWithoutPrice(RattailProblemReport):
    """
    Looks for products which have null (or $0) regular price.
    """
    problem_key = 'product_without_price'
    problem_title = "Products with no price"

    def find_problems(self, **kwargs):
        from sqlalchemy import orm

        problems = []
        session = self.app.make_session()
        model = self.model
        products = session.query(model.Product)\
                          .order_by(model.Product.upc)\
                          .options(orm.joinedload(model.Product.brand))\
                          .options(orm.joinedload(model.Product.department))\
                          .options(orm.joinedload(model.Product.regular_price))

        def inspect(product, i):
            price = product.regular_price
            if not price or not price.price:
                problems.append(product)

        self.progress_loop(inspect, products,
                           message="Looking for products with no price")
        session.close()
        return problems


class StaleInventoryBatch(RattailProblemReport):
    """
    Looks for "stale" inventory batches, those which were created but
    not executed within a certain amount of time.
    """
    problem_key = 'stale_inventory_batch'
    problem_title = "Stale inventory batches"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cutoff_days = self.config.getint(
            'rattail', 'problems.stale_inventory_batches.cutoff_days',
            default=4)

    def find_problems(self, **kwargs):
        from sqlalchemy import orm

        session = self.app.make_session()
        model = self.model

        today = self.app.localtime().date()
        cutoff = today - datetime.timedelta(days=self.cutoff_days)
        cutoff = datetime.datetime.combine(cutoff, datetime.time(0))
        cutoff = self.app.localtime(cutoff)

        batches = session.query(model.InventoryBatch)\
                         .filter(model.InventoryBatch.executed == None)\
                         .filter(model.InventoryBatch.created <= self.app.make_utc(cutoff))\
                         .options(orm.joinedload(model.InventoryBatch.created_by)\
                                  .joinedload(model.User.person))\
                         .all()

        session.close()
        return batches

    def get_email_context(self, problems, **kwargs):
        kwargs = super().get_email_context(problems, **kwargs)
        kwargs['cutoff_days'] = self.cutoff_days
        return kwargs


class UpgradePending(RattailProblemReport):
    """
    Looks for any system upgrades which have yet to be executed.
    """
    problem_key = 'upgrade_pending'
    problem_title = "Pending upgrade"

    def find_problems(self, **kwargs):
        from sqlalchemy import orm

        session = self.app.make_session()
        model = self.model
        upgrades = session.query(model.Upgrade)\
                          .filter(model.Upgrade.status_code == self.enum.UPGRADE_STATUS_PENDING)\
                          .options(orm.joinedload(model.Upgrade.created_by)\
                                   .joinedload(model.User.person))\
                          .all()
        session.close()
        return upgrades
