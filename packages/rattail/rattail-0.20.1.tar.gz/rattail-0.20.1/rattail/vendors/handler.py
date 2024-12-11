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
Vendors Handler
"""

from rattail.app import GenericHandler
from rattail.util import load_entry_points


class VendorHandler(GenericHandler):
    """
    Base class and default implementation for vendor handlers.
    """

    def choice_uses_dropdown(self):
        """
        Returns boolean indicating whether a vendor choice should be
        presented to the user via a dropdown (select) element, vs.  an
        autocomplete field.  The latter is the default because
        potentially the vendor list can be quite large, so we avoid
        loading them all in the dropdown unless so configured.

        :returns: Boolean; if true then a dropdown should be used;
           otherwise (false) autocomplete is used.
        """
        return self.config.getbool('rattail', 'vendors.choice_uses_dropdown',
                                   default=False)

    def get_vendor(self, session, key, **kwargs):
        """
        Locate and return the vendor corresponding to the given key.

        The key can be a UUID value, but most often it will instead be
        a "generic" key specific to this purpose.  Any generic key can
        be defined within the settings, pointing to a valid vendor.
        
        For instance, we can define a key of ``'poser.acme'`` to
        denote the hypothetical "Acme Distribution" vendor, and we add
        a namespace unique to our app just to be safe.

        We then create a setting in the DB pointing to our *actual*
        vendor by way of its UUID:

        .. code-block:: sql

           INSERT INTO SETTING (name, value) 
           VALUES ('rattail.vendor.poser.acme',
                   '7e6d69a2700911ec93533ca9f40bc550');

        From then on we could easily fetch the vendor by this key.
        This is mainly useful to allow catalog and invoice parsers to
        "loosely" associate with a particular vendor by way of this
        key, which could be shared across organizations etc.

        :param session: Active database session.

        :param key: Value to use when searching for the vendor.

        :returns: The :class:`~rattail.db.model.vendors.Vendor`
           instance if found; otherwise ``None``.
        """
        from sqlalchemy import orm

        model = self.model

        # Vendor.uuid match?
        vendor = session.get(model.Vendor, key)
        if vendor:
            return vendor

        # Vendor.id match?
        try:
            return session.query(model.Vendor)\
                          .filter(model.Vendor.id == key)\
                          .one()
        except orm.exc.NoResultFound:
            pass

        # try settings, if value then recurse
        key = self.app.get_setting(session, 'rattail.vendor.{}'.format(key))
        if key is not None:
            return self.get_vendor(session, key, **kwargs)

    def render_vendor(self, vendor, **kwargs):
        return str(vendor)

    def get_all_catalog_parsers(self):
        """
        Should return *all* catalog parsers known to exist.

        Note that this returns classes and not instances.

        :returns: List of
           :class:`~rattail.vendors.catalogs.CatalogParser` classes.
        """
        Parsers = list(
            load_entry_points('rattail.vendors.catalogs.parsers').values())
        Parsers.sort(key=lambda Parser: Parser.display)
        return Parsers
        
    def get_supported_catalog_parsers(self):
        """
        Should return only those catalog parsers which are "supported"
        by the current app.  Usually "supported" just means what we
        want to expose to the user.

        Note that this returns classes and not instances.

        :returns: List of
           :class:`~rattail.vendors.catalogs.CatalogParser` classes.
        """
        Parsers = self.get_all_catalog_parsers()
        
        supported_keys = self.config.getlist(
            'rattail', 'vendors.supported_catalog_parsers')
        if supported_keys is None:
            supported_keys = self.config.getlist(
                'tailbone', 'batch.vendorcatalog.supported_parsers')
        if supported_keys:
            Parsers = [Parser for Parser in Parsers
                       if Parser.key in supported_keys]
            
        return Parsers

    def get_catalog_parser(self, key, require=False):
        """
        Retrieve the catalog parser for the given parser key.

        Note that this returns an instance, not the class.

        :param key: Unique key indicating which parser to get.

        :returns: A :class:`~rattail.vendors.catalogs.CatalogParser`
           instance.
        """
        from rattail.vendors.catalogs import CatalogParserNotFound

        for Parser in self.get_all_catalog_parsers():
            if Parser.key == key:
                return Parser(self.config)

        if require:
            raise CatalogParserNotFound(key)

    def get_all_order_parsers(self):
        """
        Should return *all* order parsers known to exist.

        Note that this returns classes and not instances.

        See also :meth:`get_supported_order_parsers()` and
        :meth:`get_order_parser()`.

        :returns: List of :class:`~rattail.vendors.orders.OrderParser`
           classes.
        """
        Parsers = list(
            load_entry_points('rattail.vendors.orders.parsers').values())
        Parsers.sort(key=lambda Parser: Parser.title)
        return Parsers

    def get_supported_order_parsers(self, vendor=None, **kwargs):
        """
        Should return a list of order file parsers which are
        *supported* and should be exposed to the user.

        See also :meth:`get_all_order_parsers()` and
        :meth:`get_order_parser()`.

        :param vendor: Vendor for whom the parser is needed, if known.
           If you specify a vendor then parsers which indicate support
           for a *different* vendor will be excluded from the list.

        :returns: List of :class:`~rattail.vendors.orders.OrderParser`
           classes.
        """
        all_parsers = self.get_all_order_parsers()

        supported = self.config.get_list('rattail.vendors.supported_order_parsers')
        if supported:
            parsers = [Parser for Parser in all_parsers
                       if Parser.key in supported]
        else:
            parsers = all_parsers

        result = []
        if vendor:
            session = self.app.get_session(vendor)
            for Parser in parsers:
                parser = Parser(self.config)
                if parser.vendor_key:
                    # parser declares a vendor, so only add if it's a match
                    pvendor = parser.get_vendor(session)
                    if pvendor and pvendor is vendor:
                        result.append(parser)
                else: # parser is vendor-neutral; always add
                    result.append(parser)

        else: # no vendor specified, so show all parsers
            result = parsers

        return result

    def get_order_parser(self, key, require=False):
        """
        Retrieve the order file parser for the given key.

        Note that this returns an instance, not the class.

        See also :meth:`get_all_order_parsers()` and
        :meth:`get_supported_order_parsers()`.

        :param key: Unique key indicating which parser to get.

        :returns: An :class:`~rattail.vendors.orders.OrderParser`
           instance.
        """
        from rattail.vendors.orders import OrderParserNotFound

        for Parser in self.get_all_order_parsers():
            if Parser.key == key:
                return Parser(self.config)

        if require:
            raise OrderParserNotFound(key)
