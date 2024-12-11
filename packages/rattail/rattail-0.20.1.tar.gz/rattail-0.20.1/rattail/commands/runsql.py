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
``rattail runsql`` command
"""

import sys

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def runsql(
        ctx: typer.Context,
        engine: Annotated[
            str,
            typer.Argument(help="SQLAlchemy engine URL for the database.")] = ...,
        script: Annotated[
            typer.FileText,
            typer.Argument(help="File which contains a SQL script.")] = ...,
        max_width: Annotated[
            int,
            typer.Option(help="Max table width when displaying results.")] = 80,
):
    """
    Run (first statement of) a SQL script against a database
    """
    import sqlalchemy as sa
    import texttable

    sql = []
    for line in script:
        line = line.strip()
        if line and not line.startswith('--'):
            sql.append(line)
            if line.endswith(';'):
                break

    sql = ' '.join(sql)
    engine = sa.create_engine(engine)

    with engine.begin() as cxn:
        result = cxn.execute(sa.text(sql))
        rows = result.fetchall()
        if rows:
            table = texttable.Texttable(max_width=max_width)

            # force all columns to be treated as text.  that seems a bit
            # heavy-handed but is definitely the simplest way to deal with
            # issues such as a UPC being displayed in scientific notation
            table.set_cols_dtype(['t' for col in rows[0]])

            # add a header row, plus all data rows
            table.add_rows([rows[0].keys()] + rows)

            sys.stdout.write("{}\n".format(table.draw()))
