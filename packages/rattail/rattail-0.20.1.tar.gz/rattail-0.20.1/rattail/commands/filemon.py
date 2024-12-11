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
``rattail filemon`` command
"""

import sys
from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer


class ServiceAction(str, Enum):
    start = 'start'
    stop = 'stop'
    install = 'install'
    debug = 'debug'
    uninstall = 'uninstall'


@rattail_typer.command()
def filemon(
        ctx: typer.Context,
        action: Annotated[
            ServiceAction,
            typer.Argument(help="Action to perform for the service.  Note that only "
                           "start/stop are used on Linux; the rest are Windows-only.")] = ...,
        pidfile: Annotated[
            Path,
            typer.Option('--pidfile', '-p',
                         help="Path to PID file.  (Only used on Linux.)")] = None,
        daemonize: Annotated[
            bool,
            typer.Option(help="DEPRECATED")] = False,
        username: Annotated[
            str,
            typer.Option(help="User account under which the service should run.  "
                         "(Only used on Windows.)")] = None,
        auto_start: Annotated[
            bool,
            typer.Option('--auto-start', '-a',
                         help="Configure service to start automatically.  "
                         "(Only used on Windows.)")] = False,
):
    """
    Manage the file monitor daemon
    """
    config = ctx.parent.rattail_config

    if sys.platform in ('linux', 'linux2'):
        from rattail.filemon import linux as filemon

        if action == 'start':
            filemon.start_daemon(config, pidfile)

        elif action == 'stop':
            filemon.stop_daemon(config, pidfile)

    elif sys.platform == 'win32': # pragma no cover
        run_win32(ctx.params)

    else:
        sys.stderr.write(f"File monitor is not supported on platform: {sys.platform}\n")
        sys.exit(1)


def run_win32(params): # pragma no cover
    from rattail.win32 import require_elevation
    from rattail.win32 import service
    from rattail.win32 import users
    from rattail.filemon import win32 as filemon

    require_elevation()

    options = []
    if params['action'] == 'install':

        username = params['username']
        if username:
            if '\\' in username:
                server, username = username.split('\\')
            else:
                server = socket.gethostname()
            if not users.user_exists(username, server):
                sys.stderr.write("User does not exist: {0}\\{1}\n".format(server, username))
                sys.exit(1)

            password = ''
            while password == '':
                password = getpass(str("Password for service user: ")).strip()
            options.extend(['--username', r'{0}\{1}'.format(server, username)])
            options.extend(['--password', password])

        if params['auto_start']:
            options.extend(['--startup', 'auto'])

    service.execute_service_command(filemon, params['action'], *options)

    # If installing with custom user, grant "logon as service" right.
    if params['action'] == 'install' and params['username']:
        users.allow_logon_as_service(username)

    # TODO: Figure out if the following is even required, or if instead we
    # should just be passing '--startup delayed' to begin with?

    # If installing auto-start service on Windows 7, we should update
    # its startup type to be "Automatic (Delayed Start)".
    # TODO: Improve this check to include Vista?
    if params['action'] == 'install' and params['auto_start']:
        if platform.release() == '7':
            name = filemon.RattailFileMonitor._svc_name_
            service.delayed_auto_start_service(name)
