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
Trainwreck commands
"""

import datetime
import logging

import sqlalchemy as sa
import typer
from typing_extensions import Annotated

from rattail.commands.typer import (make_typer, typer_get_runas_user,
                                    importer_command, typer_eager_imports)
from rattail.commands.importing import ImportCommandHandler
from rattail.time import date_range


log = logging.getLogger(__name__)


trainwreck_typer = make_typer(
    name='trainwreck',
    help="Trainwreck -- Transaction data warehouse")


@trainwreck_typer.command()
@importer_command
def export_trainwreck(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the \"target\" "
                         "Trainwreck DB, i.e. where data will be exported.  This key must "
                         "be defined in the [trainwreck.db] section of your config file.")] = None,
        **kwargs
):
    """
    Export data to another Trainwreck database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_trainwreck.from_trainwreck.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@trainwreck_typer.command()
@importer_command
def import_self(
        ctx: typer.Context,
        **kwargs
):
    """
    Self-update for Trainwreck data
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_trainwreck.from_self.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)


@trainwreck_typer.command()
@importer_command
def import_trainwreck(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the "
                         "Trainwreck \"host\", i.e. the source of the data to be "
                         "imported.  This key must be defined in the [trainwreck.db] "
                         "section of your config file.")] = None,
        **kwargs
):
    """
    Import data from another Trainwreck database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_trainwreck.from_trainwreck.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@trainwreck_typer.command()
def prune(
        ctx: typer.Context,
        after: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Date *after* which all data should be pruned.  If set, no data "
                         "will be pruned from this or earlier dates.  If not set, there will be "
                         "no lower boundary for the prune.")] = None,
        before: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Date *before* which all data should be pruned.  If set, no data "
                         "will be pruned from this or later dates.  If not set, will assume a "
                         "default of \"today\".")] = None,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for the Trainwreck database engine to be used, i.e. "
                         "from which data should be pruned.  This key must be defined in the "
                         "[trainwreck.db] section of your config file.")] = 'default',
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Prune some dates from a Trainwreck database
    """
    from rattail.db.util import finalize_session

    config = ctx.parent.rattail_config
    app = config.get_app()
    trainwreck = app.get_trainwreck_handler()
    progress = ctx.parent.rattail_progress

    session = trainwreck.make_session(dbkey=dbkey)
    model = trainwreck.get_model()

    if after:
        start_date = after.date() + datetime.timedelta(days=1)
    else:
        # default is earliest available date
        end_time = session.query(sa.func.min(model.Transaction.end_time)).scalar()
        start_date = app.localtime(end_time, from_utc=True).date()

    if before:
        end_date = before.date() - datetime.timedelta(days=1)
    else:
        # default is yesterday
        end_date = app.yesterday()

    dates = list(date_range(start_date, end_date))

    for date in dates:
        log.debug("pruning from '%s' Trainwreck for %s", dbkey, date)

        start_time = datetime.datetime.combine(date, datetime.time(0))
        start_time = app.localtime(start_time)

        end_time = datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.time(0))
        end_time = app.localtime(end_time)

        trainwreck.prune_date(session, date, start_time, end_time, progress=progress)

    finalize_session(session, dry_run=dry_run)


# discover more commands
typer_eager_imports(trainwreck_typer)
