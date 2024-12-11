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
Generator for 'rattail-integration' projects
"""

import os

import colander

from rattail.projects import RattailAdjacentProjectGenerator
from rattail.util import get_studly_prefix, get_package_name


class RattailIntegrationProjectGenerator(RattailAdjacentProjectGenerator):
    """
    Generator for projects which integrate Rattail with some other
    system.  This is for generating projects such as rattail-corepos
    and rattail-mailchimp etc.
    """
    key = 'rattail_integration'

    def make_schema(self, **kwargs):
        schema = super(RattailIntegrationProjectGenerator, self).make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='integration_name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='integration_url',
                                       typ=colander.String()))

        return schema

    def normalize_context(self, context):
        context = super(RattailIntegrationProjectGenerator, self).normalize_context(context)

        if not context.get('description'):
            context['description'] = "Rattail integration package for {}".format(
                context['integration_name'])

        context['classifiers'].update(set([
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]))

        if 'integration_studly_prefix' not in context:
            context['integration_studly_prefix'] = get_studly_prefix(
                context['integration_name'])

        if 'integration_pkgname' not in context:
            context['integration_pkgname'] = get_package_name(
                context['integration_name'])

        if 'year' not in context:
            context['year'] = self.app.today().year

        return context
