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
Luigi task commands
"""

import datetime
import sys

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def overnight(
        ctx: typer.Context,
        task_key: Annotated[
            str,
            typer.Option('--task-key', '-k',
                         help="Config key for the overnight task to be launched.")] = None,
        date: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Date for which overnight task should be "
                         "launched.  Defaults to yesterday.")] = None,
        wait: Annotated[
            bool,
            typer.Option(help="Whether to run the task in-process and wait until "
                         "it completes (--wait), or schedule an async run via "
                         "`at` (--no-wait).")] = True,
        email_key: Annotated[
            str,
            typer.Option(help="Config key for email settings, to be used in "
                         "determining recipients etc.")] = None,
        email_if_empty: Annotated[
            bool,
            typer.Option(help="Whether to send email when task produces no output.")] = True,
        purge_settings: Annotated[
            bool,
            typer.Option('--purge-settings',
                         help="Instead of running a task, remove all settings "
                         "from the DB, for all overnight tasks.")] = False,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Log the final command for the task, but do not "
                         "actually run it.")] = False,
):
    """
    Launch an overnight task for Luigi
    """
    config = ctx.parent.rattail_config

    if purge_settings:
        do_purge_settings(config, dry_run=dry_run)
    else:
        do_launch_task(config, ctx.params)


def do_launch_task(config, params):
    app = config.get_app()
    luigi = app.get_luigi_handler()
    key = params['task_key']
    task = luigi.get_overnight_task(key)
    if not task:
        sys.stderr.write("overnight task not found for key: {}\n".format(key))
        sys.exit(1)

    date = params['date'] or app.yesterday()
    if isinstance(date, datetime.datetime):
        date = date.date()
    luigi.launch_overnight_task(task, date,
                                email_if_empty=params['email_if_empty'],
                                email_key=params['email_key'],
                                wait=params['wait'],
                                dry_run=params['dry_run'])


def do_purge_settings(config, dry_run=False):
    from rattail.db.util import finalize_session

    app = config.get_app()
    luigi = app.get_luigi_handler()
    session = app.make_session()
    luigi.purge_overnight_settings(session)
    finalize_session(session, dry_run=dry_run)
