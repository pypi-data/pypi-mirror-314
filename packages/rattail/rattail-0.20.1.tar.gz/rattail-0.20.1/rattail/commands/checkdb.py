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
``rattail checkdb`` command
"""

import sys

import typer

from .base import rattail_typer


@rattail_typer.command()
def checkdb(
        ctx: typer.Context,
):
    """
    Do basic sanity checks on a Rattail DB
    """
    import sqlalchemy as sa

    config = ctx.parent.rattail_config
    try:
        with config.appdb_engine.begin() as cxn:
            cxn.execute(sa.text("select version()"))
    except sa.exc.OperationalError as e:
        sys.stderr.write("\nfailed to connect to DB!\n\n{}\n".format(e))
        sys.exit(1)

    sys.stdout.write("All checks passed.\n")
