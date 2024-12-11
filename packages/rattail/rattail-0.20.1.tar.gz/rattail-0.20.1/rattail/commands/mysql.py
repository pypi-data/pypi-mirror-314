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
MySQL-related commands
"""

import sys

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def mysql_chars(
        ctx: typer.Context,
        dbtype: Annotated[
            str,
            typer.Option(help="Type of DB to inspect.  This must correspond to "
                         "a config section.")] = 'rattail.db',
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for DB to inspect.  This must "
                         "correspond to one of the keys within the config "
                         "section identified by --dbtype.")] = 'default',
        dburl: Annotated[
            str,
            typer.Option(help="Explicit URL for DB to inspect.  If possible "
                         "you should use --dbtype and --dbkey instead.  If you "
                         "do use --dburl, this value must be in the format "
                         "supported by SQLAlchemy.")] = None,
        charset: Annotated[
            str,
            typer.Option(help="Desired character set for the DB.")] = None,
        collation: Annotated[
            str,
            typer.Option(help="Desired collation for the DB.")] = None,
        table: Annotated[
            str,
            typer.Option(help="Show column info for the specified table.")] = None,
        all_tables: Annotated[
            bool,
            typer.Option('--all-tables',
                         help="Show column info for all tables in the DB.")] = False,
        offenders: Annotated[
            bool,
            typer.Option('--offenders',
                         help="Show only \"offenders\" which do not match "
                         "the desired charset and/or collation.  If this is "
                         "not specified, all info will be shown for the "
                         "object(s) regardless of their charset/collation.")] = False,
        supported: Annotated[
            bool,
            typer.Option('--supported',
                         help="Instead of showing current DB/table info, show "
                         "what's actually supported by underlying DB engine.")] = False,
        fix: Annotated[
            bool,
            typer.Option('--fix',
                         help="Execute SQL to convert charset and/or collation "
                         "for relevant objects.  Note, this will affect \"all\" "
                         "objects in scope unless --offenders is specified, in "
                         "which case only those are affected.")] = False,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Emit the SQL statements to fix/convert entities "
                         "to STDOUT instead of executing the SQL directly.  Note "
                         "that this is only used if --fix is specified.")] = False,
):
    """
    View or update character set / collation info for a MySQL DB
    """
    import sqlalchemy as sa
    from wuttjamaican.db import get_engines

    config = ctx.parent.rattail_config

    if dburl:
        engine = sa.create_engine(args.dburl)

    else:
        engines = get_engines(config, dbtype)
        if not engines:
            sys.stderr.write(f"No DB engines found for type: {dbtype}\n")
            sys.exit(1)
        if dbkey not in engines:
            sys.stderr.write(f"DB key {dbkey} not found for type: {dbtype}\n")
            sys.exit(1)
        engine = engines[dbkey]

    if engine.dialect.name != 'mysql':
        sys.stderr.write(f"dialect '{engine.dialect.name}' not supported: {engine}\n")
        sys.exit(1)

    params = dict(args._get_kwargs())
    if supported:
        do_view_supported(config, engine)
    elif fix:
        do_fix_db(config, engine, params)
    else:
        do_view_db(config, engine, params)


def do_view_supported(config, engine):
    import sqlalchemy as sa

    COLLATIONS = sa.sql.table(
        'COLLATIONS',
        sa.sql.column('COLLATION_NAME'),
        sa.sql.column('CHARACTER_SET_NAME'),
        sa.sql.column('IS_DEFAULT'),
        schema='information_schema')

    query = sa.sql.select(COLLATIONS.c.COLLATION_NAME,
                          COLLATIONS.c.CHARACTER_SET_NAME,
                          COLLATIONS.c.IS_DEFAULT)\
                  .order_by(COLLATIONS.c.COLLATION_NAME)

    with engine.begin() as cxn:
        result = cxn.execute(query)
        show_results(config, result.fetchall())


def do_view_db(config, engine, params):
    import sqlalchemy as sa

    sys.stdout.write("\n  {}\n".format(repr(engine.url)))
    sys.stdout.write("\n  desired charset:   {}\n".format(params['charset']))
    sys.stdout.write("  desired collation: {}\n".format(params['collation']))
    sys.stdout.write("\n  showing db info:  {}\n".format(
        'offenders' if params['offenders'] else 'all'))
    tables = ['(none)']
    if params['all_tables']:
        tables = ['(all)']
    elif params['table']:
        tables = [params['table']]
    sys.stdout.write("  showing table(s): {}\n\n".format(','.join(tables)))

    dbinfo = fetch_dbinfo(engine, params)
    if dbinfo:
        show_results(config, dbinfo)
        sys.stdout.write("\n")

    tablesinfo = fetch_tablesinfo(engine, params, offenders_only=params['offenders'])
    if tablesinfo:
        show_results(config, tablesinfo)
        sys.stdout.write("\n")

    tables = []
    if params['all_tables']:
        tables = [info.TABLE_NAME for info in fetch_tablesinfo(
            engine, params, offenders_only=False)]
    elif params['table']:
        tables = [params['table']]
    for table in tables:
        colsinfo = fetch_colsinfo(engine, params, table)
        if colsinfo:
            sys.stdout.write("  Table: {}\n\n".format(table))
            show_results(config, colsinfo)
            sys.stdout.write("\n")


def do_fix_db(config, engine, params):
    import sqlalchemy as sa

    if not params['charset'] or not params['collation']:
        sys.stderr.write("must specify --charset and --collation\n")
        sys.exit(1)

    if params['dry_run']:
        sys.stdout.write("\n")

    dbinfo = fetch_dbinfo(engine, params)
    if dbinfo:

        sql = f"""
        ALTER DATABASE `{engine.url.database}` CHARACTER SET :charset COLLATE :collation;
        """.strip()
        stmt = sa.text(sql).bindparams(charset=params['charset'],
                                       collation=params['collation'])

        if params['dry_run']:
            sys.stdout.write("-- fix database\n")
            sys.stdout.write("{}\n".format(stmt.compile(
                dialect=engine.dialect,
                compile_kwargs={'literal_binds': True})))
            sys.stdout.write("\n")

        else:
            with engine.begin() as cxn:
                cxn.execute(stmt)

    tablesinfo = fetch_tablesinfo(engine, params, offenders_only=params['offenders'])
    if tablesinfo:
        if params['dry_run']:
            sys.stdout.write("-- fix tables\n")

        sql = """
        ALTER TABLE `{}` CONVERT TO CHARACTER SET :charset COLLATE :collation;
        """.strip()

        for tableinfo in tablesinfo:
            tabsql = sql.format(tableinfo.TABLE_NAME)
            stmt = sa.text(tabsql).bindparams(charset=params['charset'],
                                              collation=params['collation'])

            if params['dry_run']:
                sys.stdout.write("{}\n".format(stmt.compile(
                    dialect=engine.dialect,
                    compile_kwargs={'literal_binds': True})))

            else:
                with engine.begin() as cxn:
                    cxn.execute(stmt)

        if params['dry_run']:
            sys.stdout.write("\n")

    tables = []
    if params['all_tables']:
        tables = [info.TABLE_NAME for info in fetch_tablesinfo(
            engine, params, offenders_only=False)]
    elif params['table']:
        tables = [params['table']]
    unknown_data_types = set()
    for table in tables:
        colsinfo = fetch_colsinfo(engine, params, table)
        if colsinfo:
            if params['dry_run']:
                printed_header = False

            sql = f"""
            ALTER TABLE `{tableinfo.TABLE_NAME}` MODIFY `{colinfo.COLUMN_NAME}` {{}}({{}}) CHARACTER SET :charset COLLATE :collation;
            """.strip()

            for colinfo in colsinfo:
                colsql = sql.format(colinfo.DATA_TYPE,
                                    colinfo.CHARACTER_MAXIMUM_LENGTH)
                stmt = sa.text(colsql).bindparams(charset=params['charset'],
                                                  collation=params['collation'])

                if params['dry_run']:
                    if not printed_header:
                        sys.stdout.write("-- fix columns for: {}\n".format(table))
                        printed_header = True
                    sys.stdout.write("{}\n".format(stmt.compile(
                        dialect=engine.dialect,
                        compile_kwargs={'literal_binds': True})))

                else:
                    with engine.begin() as cxn:
                        cxn.execute(stmt)

            if params['dry_run'] and printed_header:
                sys.stdout.write("\n")


def fetch_dbinfo(engine, params):
    import sqlalchemy as sa

    SCHEMATA = sa.sql.table(
        'SCHEMATA',
        sa.sql.column('SCHEMA_NAME'),
        sa.sql.column('DEFAULT_CHARACTER_SET_NAME'),
        sa.sql.column('DEFAULT_COLLATION_NAME'),
        schema='information_schema')

    query = sa.sql.select(SCHEMATA.c.SCHEMA_NAME,
                          SCHEMATA.c.DEFAULT_CHARACTER_SET_NAME,
                          SCHEMATA.c.DEFAULT_COLLATION_NAME)\
                  .where(SCHEMATA.c.SCHEMA_NAME == engine.url.database)\
                  .order_by(SCHEMATA.c.SCHEMA_NAME)

    if params['offenders']:
        query = query.where(sa.or_(
            SCHEMATA.c.DEFAULT_CHARACTER_SET_NAME != params['charset'],
            SCHEMATA.c.DEFAULT_COLLATION_NAME != params['collation']))

    with engine.begin() as cxn:
        result = cxn.execute(query)
        return result.fetchall()


def fetch_tablesinfo(engine, params, offenders_only=False):
    import sqlalchemy as sa

    TABLES = sa.sql.table(
        'TABLES',
        sa.sql.column('TABLE_SCHEMA'),
        sa.sql.column('TABLE_NAME'),
        sa.sql.column('TABLE_TYPE'),
        sa.sql.column('TABLE_COLLATION'),
        schema='information_schema')

    # nb. used to filter by TABLE_TYPE LIKE 'BASE_TABLE' here, but
    # stopped that in order to include VIEW, although it doesn't
    # seem like anything really behaved differenty.  presumably a
    # VIEW does not have its own charset/collation.  anyway not
    # sure what needs to happen here but that is the background.
    query = sa.sql.select(TABLES.c.TABLE_NAME,
                          TABLES.c.TABLE_COLLATION)\
                  .where(TABLES.c.TABLE_SCHEMA == engine.url.database)\
                  .order_by(TABLES.c.TABLE_NAME)

    if params['table']:
        query = query.where(TABLES.c.TABLE_NAME == params['table'])

    if offenders_only:
        query = query.where(TABLES.c.TABLE_COLLATION != params['collation'])

    with engine.begin() as cxn:
        result = cxn.execute(query)
        return result.fetchall()


def fetch_colsinfo(engine, params, table):
    import sqlalchemy as sa

    COLUMNS = sa.sql.table(
        'COLUMNS',
        sa.sql.column('TABLE_SCHEMA'),
        sa.sql.column('TABLE_NAME'),
        sa.sql.column('COLUMN_NAME'),
        sa.sql.column('CHARACTER_SET_NAME'),
        sa.sql.column('COLLATION_NAME'),
        sa.sql.column('DATA_TYPE'),
        sa.sql.column('CHARACTER_MAXIMUM_LENGTH'),
        schema='information_schema')

    query = sa.sql.select(COLUMNS.c.COLUMN_NAME,
                          COLUMNS.c.DATA_TYPE,
                          COLUMNS.c.CHARACTER_MAXIMUM_LENGTH,
                          COLUMNS.c.CHARACTER_SET_NAME,
                          COLUMNS.c.COLLATION_NAME)\
                  .where(COLUMNS.c.TABLE_SCHEMA == engine.url.database)\
                  .where(COLUMNS.c.TABLE_NAME == table)\
                  .where(COLUMNS.c.DATA_TYPE == 'varchar')\
                  .order_by(COLUMNS.c.COLUMN_NAME)

    if params['offenders']:
        query = query.where(sa.or_(
            COLUMNS.c.CHARACTER_SET_NAME != params['charset'],
            COLUMNS.c.COLLATION_NAME != params['collation']))

    with engine.begin() as cxn:
        result = cxn.execute(query)
        return result.fetchall()


def show_results(config, rows):
    import texttable

    table = texttable.Texttable()

    # add a header row, plus all data rows
    table.add_rows([rows[0]._mapping.keys()] + rows)

    sys.stdout.write("{}\n".format(table.draw()))
