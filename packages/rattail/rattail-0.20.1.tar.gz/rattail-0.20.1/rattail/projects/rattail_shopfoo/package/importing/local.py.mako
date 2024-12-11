## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Rattail -> "Self" data import
"""

import decimal

from sqlalchemy import orm

from rattail.importing.local import FromRattailLocal
from rattail.db.model import Product
from ${pkg_name} import importing as ${integration_pkgname}_importing
from ${pkg_name}.db.model import ${integration_studly_prefix}ProductCache


class ${integration_studly_prefix}ProductCacheImporter(FromRattailLocal, ${integration_pkgname}_importing.model.${integration_studly_prefix}ProductCacheImporter):
    """
    Product -> ${integration_studly_prefix}ProductCache
    """
    host_model_class = Product
    key = 'uuid'
    supported_fields = [
        'uuid',
        'product_uuid',
        '${integration_pkgname}_id',
        'brand_name',
        'description',
        'price',
        # 'available',
    ]

    def setup(self):
        super(${integration_studly_prefix}ProductCacheImporter, self).setup()
        self.cache_${integration_pkgname}_products()

    def cache_${integration_pkgname}_products(self):
        self.${integration_pkgname}_products = self.cache_model(
            ${integration_studly_prefix}ProductCache,
            key='product_uuid')

    def query(self):
        model = self.model
        return self.host_session.query(model.Product)\
                                .options(orm.joinedload(model.Product.brand))\
                                .options(orm.joinedload(model.Product.regular_price))

    def identify_${integration_pkgname}_product(self, product):
        if hasattr(self, '${integration_pkgname}_products'):
            return self.${integration_pkgname}_products.get(product.uuid)

        try:
            return self.session.query(${integration_studly_prefix}ProductCache)<%text>\</%text>
                               .filter(${integration_studly_prefix}ProductCache.product == product)<%text>\</%text>
                               .one()
        except orm.exc.NoResultFound:
            pass

    def identify_${integration_pkgname}_product_uuid(self, product):

        # re-use existing uuid if product already in cache
        ${integration_pkgname}_product = self.identify_${integration_pkgname}_product(product)
        if ${integration_pkgname}_product:
            return ${integration_pkgname}_product.uuid

        # otherwise make a new uuid, for new cache record
        return self.app.make_uuid()

    def normalize_host_object(self, product):
        return {
            'uuid': self.identify_${integration_pkgname}_product_uuid(product),
            'product_uuid': product.uuid,
            '${integration_pkgname}_id': str(product.upc),
            'brand_name': product.brand.name if product.brand else None,
            'description': product.description,
            'price': self.normalize_host_price(product),
            # 'available': None,
        }

    def normalize_host_price(self, product):
        if product.regular_price and product.regular_price.price is not None:
            return product.regular_price.price.quantize(decimal.Decimal('0.01'))
