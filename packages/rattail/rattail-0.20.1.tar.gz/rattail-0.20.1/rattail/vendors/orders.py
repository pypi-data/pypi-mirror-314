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
Vendor Order Files
"""

import decimal

from rattail.exceptions import RattailError
from rattail.excel import ExcelReaderXLSX


class OrderParserNotFound(RattailError):
    """
    Exception raised when an order file parser is required, but cannot
    be located.
    """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"Vendor order parser not found for key: {self.key}"


class OrderParser:
    """
    Base class for all vendor order parsers.
    """
    vendor_key = None

    def __init__(self, config):
        self.config = config
        self.app = self.config.get_app()

    @property
    def key(self):
        """
        Key for the parser.  Must be unique among all order parsers.
        """
        raise NotImplementedError(f"Order parser has no key: {repr(self)}")

    @property
    def title(self):
        """
        Human-friendly title for the parser.
        """
        raise NotImplementedError(f"Order parser has no title: {self.key}")

    def get_vendor(self, session):
        """
        Fetch the :class:`~rattail.db.model.vendors.Vendor` record
        which is associated with the current parser, if any.
        """
        if self.vendor_key:
            return self.app.get_vendor_handler().get_vendor(session, self.vendor_key)

    def parse_order_date(self, path):
        """
        Parse the order date from the order file.
        """

    def parse_order_number(self, path):
        """
        Parse the order number from the order file.
        """

    def parse_order_items(self, path, progress=None):
        """
        Parse all data items (rows) from the order file.
        """
        raise NotImplementedError

    def make_order_item(self, **kwargs):
        """
        Make and return a
        :class:`~rattail.db.model.purchase.PurchaseItem` instance.
        """
        model = self.app.model
        return model.PurchaseItem(**kwargs)


class ExcelOrderParser(OrderParser):
    """
    Base class for Excel vendor order parsers.
    """

    def get_excel_reader(self, path):
        """
        Return an :class:`~rattail.excel.ExcelReaderXLSX` instance for
        the given path.
        """
        if not hasattr(self, 'excel_reader'):
            kwargs = self.get_excel_reader_kwargs()
            self.excel_reader = ExcelReaderXLSX(path, **kwargs)
        return self.excel_reader

    def get_excel_reader_kwargs(self, **kwargs):
        """
        Should return kwargs for the Excel reader factory.
        """
        return kwargs

    def decimal(self, value, scale=2):
        """
        Convert a value to a decimal.
        """
        if value is None:
            return

        # no reason to convert integers, really
        if isinstance(value, (int, decimal.Decimal)):
            return value

        # float becomes rounded decimal
        if isinstance(value, float):
            return decimal.Decimal(f"{{:0.{scale}f}}".format(value))

        # string becomes decimal
        value = value.strip()
        if value:
            return decimal.Decimal(value)


class DefaultOrderParser(ExcelOrderParser):
    """
    Default order parser for Excel files.

    .. autoattribute:: key

    .. autoattribute:: title
    """
    key = 'default'
    title = "Default Excel Parser"

    # TODO: needs sane default parser logic
