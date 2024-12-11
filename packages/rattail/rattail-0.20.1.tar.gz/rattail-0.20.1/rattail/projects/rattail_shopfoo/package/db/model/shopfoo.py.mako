## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Integration data models for ${integration_name}
"""

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

from rattail.db import model
from rattail.db.model.shopfoo import ShopfooProductBase, ShopfooProductExportBase


class ${integration_studly_prefix}ProductCache(ShopfooProductBase, model.Base):
    """
    Local cache table for ${integration_name} products
    """
    __tablename__ = '${integration_pkgname}_product_cache'

    @declared_attr
    def __table_args__(cls):
        return cls.__product_table_args__() + (
            sa.UniqueConstraint('${integration_pkgname}_id', name='${integration_pkgname}_product_uq_${integration_pkgname}_id'),
        )

    __versioned__ = {
        # 'exclude': [
        #     'in_stock',
        #     'last_sold',
        #     'last_updated',
        #     'units_on_hand',
        # ],
    }

    ${integration_pkgname}_id = sa.Column(sa.String(length=25), nullable=False)

    brand_name = sa.Column(sa.String(length=100), nullable=True)

    description = sa.Column(sa.String(length=255), nullable=True)

    price = sa.Column(sa.Numeric(precision=13, scale=2), nullable=True)

    # last_sold = sa.Column(sa.Date(), nullable=True)

    # last_updated = sa.Column(sa.Date(), nullable=True)

    # units_on_hand = sa.Column(sa.Numeric(precision=13, scale=2), nullable=True)

    available = sa.Column(sa.Boolean(), nullable=True)

    def __str__(self):
        return self.description or ""


class ${integration_studly_prefix}ProductExport(ShopfooProductExportBase, model.Base):
    """
    History table for product exports which have been submitted to ${integration_name}
    """
    __tablename__ = '${integration_pkgname}_product_export'
