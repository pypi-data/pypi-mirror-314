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
``rattail date-organize`` command
"""

import datetime
import os
import shutil
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def date_organize(
        ctx: typer.Context,
        folder: Annotated[
            Path,
            typer.Argument(help="Path to directory containing files which are "
                           "to be organized by date.")] = ...,
):
    """
    Organize files into subfolders according to date
    """
    config = ctx.parent.rattail_config
    app = config.get_app()
    today = app.today()
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            if mtime.date() < today:
                datedir = mtime.strftime(os.sep.join(('%Y', '%m', '%d')))
                datedir = os.path.join(folder, datedir)
                if not os.path.exists(datedir):
                    os.makedirs(datedir)
                shutil.move(path, datedir)
