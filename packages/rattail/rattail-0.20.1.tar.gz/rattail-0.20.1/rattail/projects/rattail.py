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
Generator for 'rattail' projects
"""

import os

import colander


from rattail.projects import PoserProjectGenerator


class RattailProjectGenerator(PoserProjectGenerator):
    """
    Generator for "generic" Rattail projects
    """
    key = 'rattail'

    def make_schema(self, **kwargs):
        schema = super(RattailProjectGenerator, self).make_schema(**kwargs)

        # TODO: get rid of these after templates are updated

        schema.add(colander.SchemaNode(name='integrates_catapult',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='integrates_corepos',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='integrates_locsms',
                                       typ=colander.Boolean()))

        return schema

    def generate_project(self, output, context, **kwargs):
        super(RattailProjectGenerator, self).generate_project(
            output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # fablib / machines
        ##############################

        if context['uses_fabric']:

            fablib = os.path.join(package, 'fablib')
            os.makedirs(fablib)

            self.generate('package/fablib/__init__.py.mako',
                          os.path.join(fablib, '__init__.py'),
                          context)

            self.generate('package/fablib/python.py.mako',
                          os.path.join(fablib, 'python.py'),
                          context)

            deploy = os.path.join(fablib, 'deploy')
            os.makedirs(deploy)

            python = os.path.join(deploy, 'python')
            os.makedirs(python)

            self.generate('package/fablib/deploy/python/premkvirtualenv.mako',
                          os.path.join(python, 'premkvirtualenv.mako'),
                          context)

            machines = os.path.join(output, 'machines')
            os.makedirs(machines)

            server = os.path.join(machines, 'server')
            os.makedirs(server)

            self.generate('machines/server/README.md.mako',
                          os.path.join(server, 'README.md'),
                          context)

            self.generate('machines/server/Vagrantfile.mako',
                          os.path.join(server, 'Vagrantfile'),
                          context)

            self.generate('machines/server/fabenv.py.dist.mako',
                          os.path.join(server, 'fabenv.py.dist'),
                          context)

            self.generate('machines/server/fabric.yaml.dist',
                          os.path.join(server, 'fabric.yaml.dist'))

            self.generate('machines/server/fabfile.py.mako',
                          os.path.join(server, 'fabfile.py'),
                          context)

            deploy = os.path.join(server, 'deploy')
            os.makedirs(deploy)

            poser = os.path.join(deploy, context['folder'])
            os.makedirs(poser)

            if context['integrates_catapult']:
                self.generate('machines/server/deploy/poser/freetds.conf.mako_',
                              os.path.join(poser, 'freetds.conf.mako'))
                self.generate('machines/server/deploy/poser/odbc.ini',
                              os.path.join(poser, 'odbc.ini'))

            self.generate('machines/server/deploy/poser/rattail.conf.mako',
                          os.path.join(poser, 'rattail.conf.mako'),
                          context)

            self.generate('machines/server/deploy/poser/cron.conf.mako',
                          os.path.join(poser, 'cron.conf'),
                          context)

            self.generate('machines/server/deploy/poser/web.conf.mako',
                          os.path.join(poser, 'web.conf.mako'),
                          context)

            self.generate('machines/server/deploy/poser/supervisor.conf.mako',
                          os.path.join(poser, 'supervisor.conf'),
                          context)

            self.generate('machines/server/deploy/poser/overnight.sh.mako',
                          os.path.join(poser, 'overnight.sh'),
                          context)

            self.generate('machines/server/deploy/poser/overnight-wrapper.sh.mako',
                          os.path.join(poser, 'overnight-wrapper.sh'),
                          context)

            self.generate('machines/server/deploy/poser/crontab.mako',
                          os.path.join(poser, 'crontab.mako'),
                          context)

            self.generate('machines/server/deploy/poser/upgrade.sh.mako',
                          os.path.join(poser, 'upgrade.sh'),
                          context)

            self.generate('machines/server/deploy/poser/tasks.py.mako',
                          os.path.join(poser, 'tasks.py'),
                          context)

            self.generate('machines/server/deploy/poser/upgrade-wrapper.sh.mako',
                          os.path.join(poser, 'upgrade-wrapper.sh'),
                          context)

            self.generate('machines/server/deploy/poser/sudoers.mako',
                          os.path.join(poser, 'sudoers'),
                          context)

            self.generate('machines/server/deploy/poser/logrotate.conf.mako',
                          os.path.join(poser, 'logrotate.conf'),
                          context)
