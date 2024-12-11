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
Rattail - subcommand ``make-appdir``
"""

import os
import pwd
import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def make_appdir(
        ctx: typer.Context,
        path: Annotated[
            Path,
            typer.Option(help="Optional path to desired app dir.  If not specified "
                         "it will be named ``app`` and  placed in the root of the "
                         "virtual environment.")] = None,
        user: Annotated[
            str,
            typer.Option('--user', '-U',
                         help="Linux username which should be given ownership to the various "
                         "data folders which are to be created.  This is used when the app(s) "
                         "are to normally be ran as the 'rattail' user for instance.  Use "
                         "of this option probably requires 'sudo' or equivalent.")] = None,
):
    """
    Make or refresh the "app dir" for virtual environment
    """
    config = ctx.parent.rattail_config
    app = config.get_app()

    if path:
        appdir = os.path.abspath(path)
    else:
        appdir = os.path.join(sys.prefix, 'app')

    app.make_appdir(appdir)

    # TODO: this bit should probably be part of app method
    if user:
        pwdata = pwd.getpwnam(args.user)
        folders = [
            'data',
            os.path.join('data', 'uploads'),
            'log',
            'sessions',
            'work',
        ]
        for name in folders:
            path = os.path.join(app_path, name)
            os.chown(path, pwdata.pw_uid, pwdata.pw_gid)

    sys.stdout.write(f"established appdir: {appdir}\n")
