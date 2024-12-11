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
Generator for 'rattail-shopfoo' integration projects
"""

import os

from rattail.projects.rattail_integration import RattailIntegrationProjectGenerator


class RattailShopfooProjectGenerator(RattailIntegrationProjectGenerator):
    """
    Generator for projects which integrate Rattail with some type of
    e-commerce system.  This is for generating projects such as
    rattail-instacart, rattail-mercato etc. which involve a nightly
    export/upload of product data to external server.
    """
    key = 'rattail_shopfoo'

    def normalize_context(self, context):

        # nb. auto-set some flags
        context['extends_db'] = True
        context['has_model'] = True

        # then do normal logic
        context = super().normalize_context(context)

        # add command entry point
        context['entry_points'].setdefault('rattail.typer_imports', []).extend([
            "{0} = {0}.commands".format(context['pkg_name'])])

        return context

    def generate_project(self, output, context, **kwargs):
        super().generate_project(output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # db/model
        ##############################

        db = os.path.join(package, 'db')
        model = os.path.join(db, 'model')

        self.generate('package/db/model/shopfoo.py.mako',
                      os.path.join(model, '{}.py'.format(context['integration_pkgname'])),
                      context)

        ##############################
        # shopfoo -> rattail importing
        ##############################

        importing = os.path.join(package, 'importing')
        os.makedirs(importing)

        self.generate('package/importing/__init__.py',
                      os.path.join(importing, '__init__.py'))

        self.generate('package/importing/model.py.mako',
                      os.path.join(importing, 'model.py'),
                      context)

        self.generate('package/importing/local.py.mako',
                      os.path.join(importing, 'local.py'),
                      context)

        self.generate('package/importing/versions.py.mako',
                      os.path.join(importing, 'versions.py'),
                      context)
