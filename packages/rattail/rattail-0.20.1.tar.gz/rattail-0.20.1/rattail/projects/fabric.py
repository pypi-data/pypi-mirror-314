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
Generator for 'fabric' projects
"""

import os

import colander

from rattail.projects import PythonProjectGenerator


class FabricProjectGenerator(PythonProjectGenerator):
    """
    Generator for projects meant only to manage Fabric machine
    deployment logic, i.e. no Rattail app.
    """
    key = 'fabric'

    def make_schema(self, **kwargs):
        schema = super(FabricProjectGenerator, self).make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='organization',
                                       typ=colander.String()))

        # TODO: add validation for this?
        schema.add(colander.SchemaNode(name='integrates_with',
                                       typ=colander.String(),
                                       missing=''))

        return schema

    def normalize_context(self, context):
        context = super(FabricProjectGenerator, self).normalize_context(context)

        if not context.get('description'):
            context['description'] = "Fabric project for {}".format(
                context['organization'])

        context['requires']['rattail-fabric2'] = True

        if context['integrates_with'] == 'catapult':
            context['requires']['tailbone-onager'] = True

        return context

    def generate_project(self, output, context, **kwargs):
        super(FabricProjectGenerator, self).generate_project(
            output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # machines
        ##############################

        machines = os.path.join(output, 'machines')
        os.makedirs(machines)

        ##############################
        # generic-server
        ##############################

        generic_server = os.path.join(machines, 'generic-server')
        os.makedirs(generic_server)

        self.generate('machines/generic-server/README.md.mako',
                      os.path.join(generic_server, 'README.md'),
                      context)

        self.generate('machines/generic-server/Vagrantfile.mako',
                      os.path.join(generic_server, 'Vagrantfile'),
                      context)

        self.generate('machines/generic-server/fabenv.py.dist.mako',
                      os.path.join(generic_server, 'fabenv.py.dist'),
                      context)

        self.generate('machines/generic-server/fabric.yaml.dist',
                      os.path.join(generic_server, 'fabric.yaml.dist'))

        self.generate('machines/generic-server/fabfile.py.mako',
                      os.path.join(generic_server, 'fabfile.py'),
                      context)

        ##############################
        # theo-server
        ##############################

        theo_server = os.path.join(machines, 'theo-server')
        os.makedirs(theo_server)

        self.generate('machines/theo-server/README.md',
                      os.path.join(theo_server, 'README.md'))

        self.generate('machines/theo-server/Vagrantfile',
                      os.path.join(theo_server, 'Vagrantfile'))

        self.generate('machines/theo-server/fabenv.py.dist.mako',
                      os.path.join(theo_server, 'fabenv.py.dist'),
                      context)

        self.generate('machines/theo-server/fabric.yaml.dist',
                      os.path.join(theo_server, 'fabric.yaml.dist'))

        self.generate('machines/theo-server/fabfile.py.mako',
                      os.path.join(theo_server, 'fabfile.py'),
                      context)

        theo_deploy = os.path.join(theo_server, 'deploy')
        os.makedirs(theo_deploy)

        theo_python = os.path.join(theo_deploy, 'python')
        os.makedirs(theo_python)

        self.generate('machines/theo-server/deploy/python/pip.conf.mako',
                      os.path.join(theo_python, 'pip.conf.mako'),
                      context)

        theo_rattail = os.path.join(theo_deploy, 'rattail')
        os.makedirs(theo_rattail)

        self.generate('machines/theo-server/deploy/rattail/rattail.conf.mako',
                      os.path.join(theo_rattail, 'rattail.conf.mako'),
                      context)

        self.generate('machines/theo-server/deploy/rattail/freetds.conf.mako_',
                      os.path.join(theo_rattail, 'freetds.conf.mako'))

        self.generate('machines/theo-server/deploy/rattail/odbc.ini',
                      os.path.join(theo_rattail, 'odbc.ini'))

        theo_theo_common = os.path.join(theo_deploy, 'theo-common')
        os.makedirs(theo_theo_common)

        self.generate('machines/theo-server/deploy/theo-common/rattail.conf.mako',
                      os.path.join(theo_theo_common, 'rattail.conf.mako'),
                      context)

        self.generate('machines/theo-server/deploy/theo-common/web.conf.mako',
                      os.path.join(theo_theo_common, 'web.conf.mako'),
                      context)

        self.generate('machines/theo-server/deploy/theo-common/upgrade.sh.mako',
                      os.path.join(theo_theo_common, 'upgrade.sh.mako'),
                      context)

        self.generate('machines/theo-server/deploy/theo-common/tasks.py.mako_',
                      os.path.join(theo_theo_common, 'tasks.py.mako'))

        self.generate('machines/theo-server/deploy/theo-common/upgrade-wrapper.sh.mako_',
                      os.path.join(theo_theo_common, 'upgrade-wrapper.sh.mako'))

        self.generate('machines/theo-server/deploy/theo-common/supervisor.conf.mako_',
                      os.path.join(theo_theo_common, 'supervisor.conf.mako'))

        self.generate('machines/theo-server/deploy/theo-common/sudoers.mako_',
                      os.path.join(theo_theo_common, 'sudoers.mako'))
