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
Installer utilities
"""

import os
import stat
import subprocess
import sys

from rattail.app import GenericHandler
from rattail.files import resource_path
from rattail.mako import ResourceTemplateLookup
from rattail.commands.util import require_prompt_toolkit, require_rich, rprint, basic_prompt


class InstallHandler(GenericHandler):
    """
    Base class and default implementation for ``poser install``
    commands.  Note that there is no ``rattail install`` command.
    """
    # nb. these must be explicitly set b/c config is not available
    # when running normally, e.g. `poser -n install`
    #app_title = "Poser"
    #app_package = 'poser'
    #app_eggname = 'Poser'
    #app_pypiname = 'Poser'

    def __init__(self, config,
                 app_title=None, app_package=None, app_eggname=None, app_pypiname=None,
                 main_image_url=None, header_image_url=None, favicon_url=None,
                 **kwargs):
        super().__init__(config, **kwargs)

        if app_title:
            self.app_title = app_title
        if app_package:
            self.app_package = app_package
        if app_eggname:
            self.app_eggname = app_eggname
        if app_pypiname:
            self.app_pypiname = app_pypiname

        self.main_image_url = main_image_url or '/tailbone/img/home_logo.png'
        self.header_image_url = header_image_url or '/tailbone/img/rattail.ico'
        self.favicon_url = favicon_url or '/tailbone/img/rattail.ico'

    def run(self):

        # nb. technically these would be required and auto-installed
        # as needed (later), but seems better to do this explicitly
        # up-front before any other command output
        require_prompt_toolkit()
        require_rich()

        self.templates = ResourceTemplateLookup(directories=[
            resource_path('{}:templates/installer'.format(self.app_package)),
            resource_path('rattail:templates/installer'),
        ])

        self.schema_installed = False
        self.do_install_steps()

        rprint("\n\t[bold green]initial setup is complete![/bold green]")

        self.show_goodbye()
        rprint()

    def do_install_steps(self):
        self.show_welcome()
        self.sanity_check()

        # prompt user for db info
        dbinfo = self.get_dbinfo()

        # get context for generated app files
        context = self.make_template_context(dbinfo)

        # make the appdir
        self.make_appdir(context)

        # install db schema if user likes
        self.schema_installed = self.install_db_schema(dbinfo)

    def show_welcome(self, **kwargs):

        rprint("\n\t[blue]Welcome to {}![/blue]".format(self.app_title))
        rprint("\n\tThis tool will install and configure a new app.")
        rprint("\n\t[italic]NB. You should already have created a new database in PostgreSQL or MySQL.[/italic]")

        # continue?
        if not basic_prompt("continue?", True, is_bool=True):
            rprint()
            sys.exit(0)

    def sanity_check(self, **kwargs):

        # appdir must not yet exist
        appdir = os.path.join(sys.prefix, 'app')
        if os.path.exists(appdir):
            rprint("\n\t[bold red]appdir already exists:[/bold red]  {}\n".format(appdir))
            sys.exit(1)

    def get_dbinfo(self, **kwargs):
        dbinfo = {}

        # get db info
        dbinfo['dbtype'] = basic_prompt('db type', 'postgresql')
        dbinfo['dbhost'] = basic_prompt('db host', 'localhost')
        default_port = '3306' if dbinfo['dbtype'] == 'mysql' else '5432'
        dbinfo['dbport'] = basic_prompt('db port', default_port)
        dbinfo['dbname'] = basic_prompt('db name', self.app_package)
        dbinfo['dbuser'] = basic_prompt('db user', 'rattail')

        # get db password
        dbinfo['dbpass'] = None
        while not dbinfo['dbpass']:
            dbinfo['dbpass'] = basic_prompt('db pass', is_password=True)

        # test db connection
        rprint("\n\ttesting db connection... ", end='')
        dbinfo['dburl'] = self.make_db_url(dbinfo['dbtype'],
                                           dbinfo['dbhost'],
                                           dbinfo['dbport'],
                                           dbinfo['dbname'],
                                           dbinfo['dbuser'],
                                           dbinfo['dbpass'])
        error = self.test_db_connection(dbinfo['dburl'])
        if error:
            rprint("[bold red]cannot connect![/bold red] ..error was:")
            rprint("\n{}".format(error))
            rprint("\n\t[bold yellow]aborting mission[/bold yellow]\n")
            sys.exit(1)
        rprint("[bold green]good[/bold green]")

        return dbinfo

    def make_db_url(self, dbtype, dbhost, dbport, dbname, dbuser, dbpass):
        try:
            # newer style
            from sqlalchemy.engine import URL
            factory = URL.create
        except ImportError:
            # older style
            from sqlalchemy.engine.url import URL
            factory = URL

        if dbtype == 'mysql':
            drivername = 'mysql+mysqlconnector'
        else:
            drivername = 'postgresql+psycopg2'

        return factory(drivername=drivername,
                       username=dbuser,
                       password=dbpass,
                       host=dbhost,
                       port=dbport,
                       database=dbname)

    def test_db_connection(self, url):
        from sqlalchemy import create_engine, inspect

        engine = create_engine(url)

        # check for random table; does not matter if it exists, we
        # just need to test interaction and this is a neutral way
        try:
            inspect(engine).has_table('whatever')
        except Exception as error:
            return str(error)

    def make_template_context(self, dbinfo, **kwargs):
        envname = os.path.basename(sys.prefix)
        appdir = os.path.join(sys.prefix, 'app')
        return {
            'envdir': sys.prefix,
            'envname': envname,
            'app_package': self.app_package,
            'app_title': self.app_title,
            'pypi_name': self.app_pypiname,
            'appdir': appdir,
            'db_url': dbinfo['dburl'],
            'pyramid_egg': self.app_eggname,
            'beaker_key': envname,
        }

    def make_appdir(self, context, **kwargs):
        rootpkg = self.app_package

        # appdir
        appdir = os.path.join(sys.prefix, 'app')
        self.app.make_appdir(appdir)

        # rattail.conf
        template = self.templates.get_template('rattail.conf.mako')
        self.app.make_config_file(
            'rattail', os.path.join(appdir, 'rattail.conf'),
            template=template, **context)

        # quiet.conf, silent.conf
        self.app.make_config_file('quiet', appdir)
        self.app.make_config_file('silent', appdir)

        # web.conf
        self.app.make_config_file(
            'web-complete', os.path.join(appdir, 'web.conf'),
            **context)

        # upgrade.sh
        template = self.templates.get_template('upgrade.sh.mako')
        path = os.path.join(appdir, 'upgrade.sh')
        self.app.render_mako_template(None, context, template=template,
                                      output_path=path)
        os.chmod(path, stat.S_IRWXU
                 | stat.S_IRGRP
                 | stat.S_IXGRP
                 | stat.S_IROTH
                 | stat.S_IXOTH)

        rprint("\n\tappdir created at:  [bold green]{}[/bold green]".format(appdir))

    def install_db_schema(self, dbinfo, **kwargs):
        from alembic.util.messaging import obfuscate_url_pw

        if not basic_prompt("install db schema?", True, is_bool=True):
            return False

        rprint()

        # install db schema
        cmd = [os.path.join(sys.prefix, 'bin', 'alembic'),
               '-c', os.path.join(sys.prefix, 'app', 'rattail.conf'),
               'upgrade', 'heads']
        subprocess.check_call(cmd)

        # put initial settings
        self.put_settings()

        rprint("\n\tdb schema installed to:  [bold green]{}[/bold green]".format(
            obfuscate_url_pw(dbinfo['dburl'])))

        # make admin, if user likes
        self.make_admin_user()

        return True

    def put_settings(self, **kwargs):

        # hide theme picker
        self.put_setting('tailbone.themes.expose_picker', 'false')

        # set main image
        self.put_setting('tailbone.main_image_url', self.main_image_url)

        # set header image
        self.put_setting('tailbone.header_image_url', self.header_image_url)

        # set favicon image
        self.put_setting('tailbone.favicon_url', self.favicon_url)

        # set default grid page size
        self.put_setting('tailbone.grid.default_pagesize', '20')

    def put_setting(self, name, value):
        cmd = [os.path.join(sys.prefix, 'bin', 'rattail'),
               '-c', os.path.join(sys.prefix, 'app', 'silent.conf'),
               'setting-put', name, value]
        subprocess.check_call(cmd)

    def make_admin_user(self, **kwargs):

        if not basic_prompt("create admin user?", True, is_bool=True):
            return False

        # get admin credentials
        username = basic_prompt('admin username', 'admin')
        password = None
        while not password:
            password = basic_prompt('admin password', is_password=True)
            if password:
                confirm = basic_prompt('confirm password', is_password=True)
                if not confirm or confirm != password:
                    rprint("[bold yellow]passwords did not match[/bold yellow]")
                    password = None
        fullname = basic_prompt('full name')

        rprint()

        # make admin user
        cmd = [os.path.join(sys.prefix, 'bin', 'rattail'),
               '-c', os.path.join(sys.prefix, 'app', 'quiet.conf'),
               'make-user', '--admin', username, '--password', password]
        if fullname:
            cmd.extend(['--full-name', fullname])
        subprocess.check_call(cmd)

        rprint("\n\tadmin user created:  [bold green]{}[/bold green]".format(
            username))
        return True

    def show_goodbye(self):
        if self.schema_installed:
            rprint("\n\tyou can run the web app with:")
            rprint("\n\t[blue]cd {}[/blue]".format(sys.prefix))
            rprint("\t[blue]bin/pserve file+ini:app/web.conf[/blue]")
