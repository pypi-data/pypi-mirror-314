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
Generator for 'tailbone-integration' projects
"""

import os

import colander

from rattail.projects import PythonProjectGenerator
from rattail.util import get_studly_prefix, get_package_name


class TailboneIntegrationProjectGenerator(PythonProjectGenerator):
    """
    Generator for projects which integrate Tailbone with some other
    system.  This is for generating projects such as tailbone-corepos
    and tailbone-mailchimp etc.
    """
    key = 'tailbone_integration'

    def make_schema(self, **kwargs):
        schema = super(TailboneIntegrationProjectGenerator, self).make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='integration_name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='integration_url',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='has_static_files',
                                       typ=colander.Boolean()))

        return schema

    def normalize_context(self, context):
        context = super(TailboneIntegrationProjectGenerator, self).normalize_context(context)

        if not context.get('description'):
            context['description'] = "Tailbone integration package for {}".format(
                context['integration_name'])

        context['classifiers'].update(set([
            'Environment :: Web Environment',
            'Framework :: Pyramid',
            'Operating System :: POSIX :: Linux',
            'Topic :: Office/Business',
        ]))

        context['requires']['Tailbone'] = True

        if 'integration_studly_prefix' not in context:
            context['integration_studly_prefix'] = get_studly_prefix(
                context['integration_name'])

        if 'integration_pkgname' not in context:
            context['integration_pkgname'] = get_package_name(
                context['integration_name'])

        if 'year' not in context:
            context['year'] = self.app.today().year

        return context

    def generate_project(self, output, context, **kwargs):
        super(TailboneIntegrationProjectGenerator, self).generate_project(
            output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # views
        ##############################

        views = os.path.join(package, 'views')
        os.makedirs(views)

        self.generate('package/views/__init__.py',
                      os.path.join(views, '__init__.py'))

        ##############################
        # static
        ##############################

        if context['has_static_files']:

            static = os.path.join(package, 'static')
            os.makedirs(static)

            self.generate('package/static/__init__.py.mako',
                          os.path.join(static, '__init__.py'),
                          context)

        ##############################
        # templates
        ##############################

        templates = os.path.join(package, 'templates')
        os.makedirs(templates)

        self.generate('package/templates/.keepme',
                      os.path.join(templates, '.keepme'))
