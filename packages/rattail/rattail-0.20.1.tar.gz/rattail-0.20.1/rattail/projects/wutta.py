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
Project Generators
"""

import os
import re

from rattail.projects.base import PythonProjectGenerator


class WuttaProjectGenerator(PythonProjectGenerator):
    """
    Wutta project generator.
    """
    key = 'wutta'

    def normalize_context(self, context):
        """ """
        context = super().normalize_context(context)

        # TODO
        context['has_cli'] = True

        # classifiers
        context['classifiers'].update(set([
            'Environment :: Web Environment',
            'Framework :: Pyramid',
        ]))

        # dependencies
        context['requires'].setdefault('psycopg2', True)
        context['requires'].setdefault('WuttaWeb[continuum]', True)

        # entry point for config extension
        context['entry_points'].setdefault('wutta.config.extensions', []).extend([
            f"{context['pkg_name']} = {context['pkg_name']}.config:{context['studly_prefix']}Config"])

        # entry point for paste (web app)
        context['entry_points'].setdefault('paste.app_factory', []).extend([
            f"main = {context['pkg_name']}.web.app:main"])

        return context

    def generate_project(self, output, context, **kwargs):
        """ """
        from alembic.config import Config as AlembicConfig
        from alembic.command import revision as alembic_revision

        super().generate_project(output, context, **kwargs)

        ##############################
        # root package dir
        ##############################

        package = os.path.join(output, context['pkg_name'])

        self.generate('package/config.py.mako',
                      os.path.join(package, 'config.py'),
                      context)

        self.generate('package/commands.py.mako',
                      os.path.join(package, 'commands.py'),
                      context)

        ##############################
        # db package dir
        ##############################

        db = os.path.join(package, 'db')
        os.makedirs(db)

        self.generate('package/db/__init__.py',
                      os.path.join(db, '__init__.py'))

        ####################
        # model
        ####################

        model = os.path.join(db, 'model')
        os.makedirs(model)

        self.generate('package/db/model/__init__.py.mako',
                      os.path.join(model, '__init__.py'),
                      context)

        ####################
        # alembic
        ####################

        alembic = os.path.join(db, 'alembic')
        os.makedirs(alembic)

        versions = os.path.join(alembic, 'versions')
        os.makedirs(versions)

        # make alembic config, aware of new project versions folder
        alembic_config = AlembicConfig()
        alembic_config.set_main_option('script_location',
                                       'wuttjamaican.db:alembic')
        alembic_config.set_main_option('version_locations',
                                       ' '.join([
                                           versions,
                                           'wuttjamaican.db:alembic/versions',
                                       ]))

        # generate first revision script for new project
        script = alembic_revision(alembic_config,
                                  version_path=versions,
                                  head='wutta@head',
                                  splice=True,
                                  branch_label=context['pkg_name'],
                                  message=f"add {context['pkg_name']} branch")

        # declare `down_revision = None` ..no way to tell alembic
        # to do that apparently, so we must rewrite file
        with open(script.path, 'rt') as f:
            old_contents = f.read()
        new_contents = []
        for line in old_contents.split('\n'):
            if line.startswith('down_revision ='):
                line = re.sub(r"'\w+'", 'None', line)
            new_contents.append(line)
        with open(script.path, 'wt') as f:
            f.write('\n'.join(new_contents))

        ##############################
        # web package dir
        ##############################

        web = os.path.join(package, 'web')
        os.makedirs(web)

        self.generate('package/web/__init__.py',
                      os.path.join(web, '__init__.py'))

        self.generate('package/web/app.py.mako',
                      os.path.join(web, 'app.py'),
                      context)

        self.generate('package/web/menus.py.mako',
                      os.path.join(web, 'menus.py'),
                      context)

        self.generate('package/web/subscribers.py.mako',
                      os.path.join(web, 'subscribers.py'),
                      context)

        static = os.path.join(web, 'static')
        os.makedirs(static)

        self.generate('package/web/static/__init__.py.mako',
                      os.path.join(static, '__init__.py'),
                      context)

        libcache = os.path.join(static, 'libcache')
        os.makedirs(libcache)

        self.generate('package/web/static/libcache/README.mako',
                      os.path.join(libcache, 'README'),
                      context)

        web_templates = os.path.join(web, 'templates')
        os.makedirs(web_templates)

        self.generate('package/web/templates/base_meta.mako_tmpl',
                      os.path.join(web_templates, 'base_meta.mako'),
                      context)

        views = os.path.join(web, 'views')
        os.makedirs(views)

        self.generate('package/web/views/__init__.py.mako',
                      os.path.join(views, '__init__.py'),
                      context)
