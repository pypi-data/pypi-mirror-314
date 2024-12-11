# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Generator for 'tailbone-shopfoo' integration projects
"""

import os

from rattail.projects.tailbone_integration import TailboneIntegrationProjectGenerator


class TailboneShopfooProjectGenerator(TailboneIntegrationProjectGenerator):
    """
    Generator for projects which integrate Tailbone with some type of
    e-commerce system.  This is for generating projects such as
    tailbone-instacart, tailbone-mercato etc. which involve a nightly
    export/upload of product data to external server.
    """
    key = 'tailbone_shopfoo'

    def normalize_context(self, context):

        # nb. auto-set some flags
        context['has_web'] = False

        # then do normal logic
        context = super(TailboneShopfooProjectGenerator, self).normalize_context(context)

        return context

    def generate_project(self, output, context, **kwargs):
        super(TailboneShopfooProjectGenerator, self).generate_project(
            output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # web views
        ##############################

        views = os.path.join(package, 'views')

        shopfoo = os.path.join(views, context['integration_pkgname'])
        os.makedirs(shopfoo)

        self.generate('package/views/shopfoo/__init__.py.mako',
                      os.path.join(shopfoo, '__init__.py'),
                      context)

        self.generate('package/views/shopfoo/products.py.mako',
                      os.path.join(shopfoo, 'products.py'),
                      context)

        self.generate('package/views/shopfoo/exports.py.mako',
                      os.path.join(shopfoo, 'exports.py'),
                      context)
