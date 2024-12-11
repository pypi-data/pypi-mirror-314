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
import random
import re
import shutil
import string
import sys

import colander
from mako.template import Template

from wuttjamaican.util import get_class_hierarchy
from rattail.util import get_studly_prefix
from rattail.mako import ResourceTemplateLookup


class ProjectGenerator(object):
    """
    Base class for project generators.

    .. attribute:: key

       Unique key for the project type.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.app = self.config.get_app()

        self.template_lookup = ResourceTemplateLookup()

    @property
    def key(self):
        raise NotImplementedError("Must define {}.key".format(
            self.__class__.__name__))

    @classmethod
    def get_templates_path(cls):
        """
        Return the path to templates folder for this generator.

        This is a class method for sake of inheritance, so templates
        can more easily be shared by generator subclasses.
        """
        basedir = os.path.dirname(sys.modules[cls.__module__].__file__)
        return os.path.join(basedir, cls.key)

    def make_schema(self, **kwargs):
        return colander.Schema()

    def generate_project(self, output, context, **kwargs):
        """
        Generate a new project to the given output folder, with the
        given context data.

        :param output: Path to output folder.  This path should
           already exist.

        :param context: Dictionary of template context data.
        """

    def get_template_path(self, template):
        """
        Return the full path to a template file.

        :param template: Filename of the template, e.g. ``'setup.py'``.
        """
        for cls in get_class_hierarchy(self.__class__, topfirst=False):
            templates = cls.get_templates_path()
            path = os.path.join(templates, template)
            if os.path.exists(path):
                return path

        raise RuntimeError("template not found: {}".format(template))

    def normalize_context(self, context):
        return context

    def generate(self, template, output, context=None, **kwargs):
        """
        Generate a file from the given template, and save the result
        to the given output path.

        This will do one of 3 things based on the specified template:

        * if filename ends with ``.mako`` then call
          :meth:`generate_mako()`
        * if filename ends with ``.mako_tmpl`` then call
          :meth:`generate_mako_tmpl()`
        * otherwise copy file as-is (do not "generate" output)

        :param template: Path to template file.

        :param output: Path to output file.

        :param context: Data dictionary with template context.
        """
        template = self.get_template_path(template)
        context = context or {}

        # maybe run it through our simplistic, hand-rolled template
        # engine (note, this is only for the sake of *avoiding* mako
        # logic, when generating "actual" mako templates, so we avoid
        # a mako-within-mako situation.)
        if template.endswith('.mako_tmpl'):
            return self.generate_mako_tmpl(template, output, context)

        # maybe run it through Mako template engine
        if template.endswith('.mako'):
            return self.generate_mako(template, output, context)

        # or, just copy the file as-is
        shutil.copyfile(template, output)

    def generate_mako(self, template, output, context):
        """
        Generate output from a Mako template.
        """
        template = Template(filename=template,
                            lookup=self.template_lookup)
        text = template.render(**context)
        with open(output, 'wt') as f:
            f.write(text)

    def generate_mako_tmpl(self, template, output, context):
        """
        Generate output (which is itself a Mako template) from a
        "simple" original template.

        Sometimes you want the final output to be a Mako template, but
        your original template also must be dynamic, based on context.
        It's problematic (confusing at the very least) for an original
        Mako template to produce output which is also a Mako template.
        So instead..

        If you give your original template file a ``.mako_tmpl``
        extension, then the output will still be dynamic, but instead
        of running the original template through the Mako engine, we
        leverage Python strings' printf-style formatting.

        A small example template might be ``rattail.conf.mako_tmpl``:

        .. code-block:: ini

           <%%text>##############################</%%text>
           # example config
           <%%text>##############################</%%text>

           [rattail]
           app_title = ${app_title}

           [alembic]
           script_location = rattail.db:alembic
           version_locations = %(alembic_version_locations)s

           # -- LOGGING SECTION --

           [formatter_generic]
           format = %%(asctime)s %%(levelname)-5.5s [%%(name)s][%%(threadName)s] %%(funcName)s: %%(message)s
           datefmt = %%Y-%%m-%%d %%H:%%M:%%S

        Note the Mako syntax which is *ignored* (passed through as-is)
        by this method when generating output.

        Note also this template expects ``alembic_version_locations``
        to be provided via the context.

        Finally also note the doubled-up ``%`` chars, both in
        ``<%%text>`` as well as in the logging section.  Since
        printf-style formatting uses the ``%`` char, we must escape
        those by doubling-up; the formatter will convert each back to
        single chars for the output.

        For more info on the formatting specifics see
        :ref:`python:old-string-formatting`.

        So with context like::

           {'alembic_version_locations': 'rattail.db:alembic/versions'}

        The above example would produce output ``rattail.conf.mako``:

        .. code-block:: ini

           <%text>##############################</%text>
           # example config
           <%text>##############################</%text>

           [rattail]
           app_title = ${app_title}

           [alembic]
           script_location = rattail.db:alembic
           version_locations = rattail.db:alembic/versions

           # -- LOGGING SECTION --

           [formatter_generic]
           format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(funcName)s: %(message)s
           datefmt = %Y-%m-%d %H:%M:%S
        """
        with open(template, 'rt') as f:
            template_lines = f.readlines()

        output_lines = []
        for line in template_lines:
            line = line.rstrip('\n')
            line = line % context
            output_lines.append(line)

        with open(output, 'wt') as f:
            f.write('\n'.join(output_lines))

    def random_string(self, size=20, chars=string.ascii_letters + string.digits):
        # per https://stackoverflow.com/a/2257449
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


class PythonProjectGenerator(ProjectGenerator):
    """
    Base class for Python project generators.

    All projects generated are assumed to have the following context:

    * ``name`` - human-friendly name for the project, e.g. ``"Poser Plus"``
    * ``description`` - brief (one-line) description of the project
    * ``folder`` - folder name for the project, e.g. ``"poser-plus"``
    * ``pkg_name`` - package name for use in Python, e.g. ``"poser_plus"``
    * ``pypi_name`` - package name for use with PyPI, e.g. ``"Poser-Plus"``
    * ``egg_name`` - package name used with egg files, e.g. ``"Poser_Plus"``
    * ``studly_prefix`` - prefix for class names, e.g. ``PoserPlus``
    * ``env_name`` - name of the Python virtual environment
    * ``requires`` - dict of required dependencies
    * ``classifiers`` - set of Python trove classifiers for project
    * ``entry_points`` - dict of setuptools entry points for project
    """
    # nb. subclass must override this!
    key = 'python'

    def make_schema(self, **kwargs):
        schema = super().make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='pkg_name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='pypi_name',
                                       typ=colander.String()))

        return schema

    def normalize_context(self, context):
        context = super().normalize_context(context)

        if 'description' not in context:
            context['description'] = ""

        if 'folder' not in context:
            context['folder'] = context['pkg_name'].replace('_', '-')

        if 'egg_name' not in context:
            context['egg_name'] = context['pypi_name'].replace('-', '_')

        if 'studly_prefix' not in context:
            context['studly_prefix'] = get_studly_prefix(context['name'])

        if 'env_name' not in context:
            context['env_name'] = context['folder']

        if 'requires' not in context:
            context['requires'] = {}

        if 'classifiers' not in context:
            context['classifiers'] = set([
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Natural Language :: English',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
            ])

        if 'entry_points' not in context:
            context['entry_points'] = {}

        return context

    def generate_project(self, output, context, **kwargs):

        ##############################
        # root project dir
        ##############################

        self.generate('gitignore.mako',
                      os.path.join(output, '.gitignore'),
                      context)

        self.generate('MANIFEST.in.mako',
                      os.path.join(output, 'MANIFEST.in'),
                      context)

        self.generate('README.md.mako',
                      os.path.join(output, 'README.md'),
                      context)

        self.generate('CHANGELOG.md.mako',
                      os.path.join(output, 'CHANGELOG.md'),
                      context)

        self.generate('pyproject.toml.mako',
                      os.path.join(output, 'pyproject.toml'),
                      context)

        self.generate('tasks.py.mako',
                      os.path.join(output, 'tasks.py'),
                      context)

        ##############################
        # root package dir
        ##############################

        package = os.path.join(output, context['pkg_name'])
        os.makedirs(package)

        self.generate('package/__init__.py.mako',
                      os.path.join(package, '__init__.py'),
                      context)

        self.generate('package/_version.py.mako',
                      os.path.join(package, '_version.py'),
                      context)


class RattailAdjacentProjectGenerator(PythonProjectGenerator):
    """
    Base class for "Rattail-adjacent" project generators, i.e. for
    projects which are based on Rattail, but may or may not be full
    "Poser" type apps.

    In addition to normal context for Python projects, all
    Rattail-adjacent projects are assumed to have the following
    context:

    * ``extends_config`` - whether the app extends Rattail config
    * ``has_cli`` - whether the app has its own command interface
    * ``extends_db`` - whether the app extends DB schema
    * ``has_model`` - whether the app provides top-level ORM model
    """
    # nb. subclass must override this!
    key = 'rattail_adjacent'

    def make_schema(self, **kwargs):
        schema = super().make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='extends_config',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_cli',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='extends_db',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_model',
                                       typ=colander.Boolean()))

        return schema

    def normalize_context(self, context):
        context = super().normalize_context(context)

        context['requires'].setdefault('rattail', True)

        context['classifiers'].update(set([
            'Topic :: Office/Business',
        ]))

        if context['extends_config']:
            context['entry_points'].setdefault('rattail.config.extensions', []).extend([
                "{0} = {0}.config:{1}Config".format(context['pkg_name'],
                                                    context['studly_prefix'])])

        if context['has_cli']:
            # nb. these alembic values are only needed for installer
            # template, which means only used if `has_cli=True`

            if 'alembic_script_location' not in context:
                context['alembic_script_location'] = 'rattail.db:alembic'

            if 'alembic_version_locations' not in context:
                context['alembic_version_locations'] = ['rattail.db:alembic/versions']
            if context['extends_db']:
                context['alembic_version_locations'].append(
                    '{}.db:alembic/versions'.format(context['pkg_name']))

        return context

    def generate_project(self, output, context, **kwargs):
        from alembic.config import Config as AlembicConfig
        from alembic.command import revision as alembic_revision

        super().generate_project(output, context, **kwargs)

        ##############################
        # root package dir
        ##############################

        package = os.path.join(output, context['pkg_name'])

        if context['extends_config']:
            self.generate('package/config.py.mako',
                          os.path.join(package, 'config.py'),
                          context)

        if context['has_cli']:
            self.generate('package/commands.py.mako',
                          os.path.join(package, 'commands.py'),
                          context)

        ##############################
        # db package dir
        ##############################

        if context['has_model'] or context['extends_db']:

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

            if context['extends_db']:

                alembic = os.path.join(db, 'alembic')
                os.makedirs(alembic)

                versions = os.path.join(alembic, 'versions')
                os.makedirs(versions)

                # make alembic config, aware of new project versions folder
                alembic_config = AlembicConfig()
                alembic_config.set_main_option('script_location',
                                            'rattail.db:alembic')
                alembic_config.set_main_option('version_locations',
                                            '{} rattail.db:alembic/versions'.format(
                                                versions))

                # generate first revision script for new project
                script = alembic_revision(alembic_config,
                                          version_path=versions,
                                          head='rattail@head',
                                          splice=True,
                                          branch_label=context['pkg_name'],
                                          message="add {} branch".format(context['pkg_name']))

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
        # templates
        ##############################

        if context['has_cli']:

            templates = os.path.join(package, 'templates')
            os.makedirs(templates)

            installer = os.path.join(templates, 'installer')
            os.makedirs(installer)

            self.generate('package/templates/installer/rattail.conf.mako',
                          os.path.join(installer, 'rattail.conf.mako'),
                          context)

            self.generate('package/templates/installer/upgrade.sh.mako_',
                          os.path.join(installer, 'upgrade.sh.mako'))


class PoserProjectGenerator(RattailAdjacentProjectGenerator):
    """
    Base class for Poser project generators.

    In addition to normal context for "Rattail-adjacent" projects, all
    Poser projects are assumed to have the following context:

    * ``organization`` - human-friendly name for the organization
    * ``has_db`` - whether the app has a Rattail DB
    * ``has_batch_schema`` - whether the DB needs dynamic 'batch' schema
    * ``db_name`` - name of the Rattail DB
    * ``has_datasync`` - whether the app needs a datasync service
    * ``has_web`` - whether the app has tailbone web UI
    * ``has_web_api`` - whether the app has tailbone web API
    * ``beaker_session_secret`` - secret for Beaker session storage
    * ``uses_fabric`` - whether the app is deployed via fabric
    """
    # nb. subclass must override this!
    key = 'poser'

    def make_schema(self, **kwargs):
        schema = super().make_schema(**kwargs)

        schema.add(colander.SchemaNode(name='organization',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='has_db',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_batch_schema',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_web',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_web_api',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='has_datasync',
                                       typ=colander.Boolean()))

        schema.add(colander.SchemaNode(name='uses_fabric',
                                       typ=colander.Boolean()))

        return schema

    def normalize_context(self, context):
        context = super().normalize_context(context)

        if not context.get('description'):
            context['description'] = "Rattail/Poser project for {}".format(
                context['organization'])

        context['classifiers'].update(set([
            'Environment :: Console',
            'Operating System :: POSIX :: Linux',
        ]))
        if context['has_web'] or context['has_web_api']:
            context['classifiers'].update(set([
                'Environment :: Web Environment',
                'Framework :: Pyramid',
            ]))

        if context['has_web']:
            context['entry_points'].setdefault('paste.app_factory', []).extend([
                "main = {}.web.app:main".format(context['pkg_name']),
            ])

        if 'db_name' not in context:
            context['db_name'] = context['pkg_name']

        if 'beaker_session_secret' not in context:
            context['beaker_session_secret'] = self.random_string()

        if context['has_db']:
            context['requires'].setdefault('psycopg2', True)

        if context['has_web']:
            context['requires'].setdefault('Tailbone', True)
        elif context['has_db']:
            context['requires'].setdefault('rattail', 'rattail[db]')

        if context['uses_fabric']:
            context['requires'].setdefault('rattail-fabric2', True)

        if 'mako_directories' not in context:
            context['mako_directories'] = [
                '{}.web:templates'.format(context['pkg_name']),
                'tailbone:templates',
            ]

        return context

    def generate_project(self, output, context, **kwargs):
        super().generate_project(output, context, **kwargs)

        package = os.path.join(output, context['pkg_name'])

        ##############################
        # web package dir
        ##############################

        if context['has_web']:

            web = os.path.join(package, 'web')
            os.makedirs(web)

            self.generate('package/web/__init__.py',
                          os.path.join(web, '__init__.py'))

            self.generate('package/web/app.py.mako',
                          os.path.join(web, 'app.py'),
                          context)

            self.generate('package/web/menus.py.mako', os.path.join(web, 'menus.py'),
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
