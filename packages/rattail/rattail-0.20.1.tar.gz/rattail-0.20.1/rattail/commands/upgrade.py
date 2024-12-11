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
``rattail upgrade`` command
"""

import logging
import sys

import typer
from typing_extensions import Annotated

from .base import rattail_typer
from .typer import typer_get_runas_user


log = logging.getLogger(__name__)


@rattail_typer.command()
def upgrade(
        ctx: typer.Context,
        system: Annotated[
            str,
            typer.Option(help="System to which the upgrade applies.")] = 'rattail',
        description: Annotated[
            str,
            typer.Option(help="Description for the new/matched upgrade.")] = None,
        enabled: Annotated[
            bool,
            typer.Option(help="Desired enabled flag for the new/matched upgrade.")] = True,
        create: Annotated[
            bool,
            typer.Option('--create',
                         help="Create a new upgrade with the given attributes.")] = False,
        execute: Annotated[
            bool,
            typer.Option('--execute',
                         help="Execute the upgrade.  Note that if you do not specify "
                         "--create then the upgrade matching the given attributes "
                         "will be read from the database.  If such an upgrade is not "
                         "found or is otherwise invalid (e.g. already executed), "
                         "the command will fail.")] = False,
        keep_exit_code: Annotated[
            bool,
            typer.Option('--keep-exit-code',
                         help="Exit with same return code as subprocess.  If "
                         "this is not specified, this command will normally "
                         "exit with code 0 regardless of what happens with "
                         "the subprocess.  (only applicable with --execute)")] = False,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Upgrade the local Rattail app
    """
    from sqlalchemy import orm
    from rattail.db.util import finalize_session

    if not create and not execute:
        sys.stderr.write("Must specify --create and/or --execute\n")
        sys.exit(1)

    config = ctx.parent.rattail_config
    app = config.get_app()
    progress = ctx.parent.rattail_progress

    session = app.make_session()
    model = app.model
    user = typer_get_runas_user(ctx, session=session)

    if create:
        upgrade = model.Upgrade()
        upgrade.system = system or 'rattail'
        upgrade.description = description
        upgrade.created = app.make_utc()
        upgrade.created_by = user
        upgrade.enabled = enabled
        session.add(upgrade)
        session.flush()
        log.info("user '%s' created new upgrade: %s", user.username, upgrade)

    else:
        upgrades = session.query(model.Upgrade)\
                          .filter(model.Upgrade.enabled == enabled)
        if description:
            upgrades = upgrades.filter(model.Upgrade.description == description)
        try:
            upgrade = upgrades.one()
        except orm.exc.NoResultFound:
            sys.stderr.write("no matching upgrade found\n")
            session.rollback()
            session.close()
            sys.exit(1)
        except orm.exc.MultipleResultsFound:
            sys.stderr.write("found {} matching upgrades\n".format(upgrades.count()))
            session.rollback()
            session.close()
            sys.exit(1)

    if execute:
        if upgrade.executed:
            sys.stderr.write("upgrade has already been executed: {}\n".format(upgrade))
            session.rollback()
            session.close()
            sys.exit(1)
        if not upgrade.enabled:
            sys.stderr.write("upgrade is not enabled for execution: {}\n".format(upgrade))
            session.rollback()
            session.close()
            sys.exit(1)

        # execute upgrade
        handler = app.get_upgrade_handler()
        log.info("will now execute upgrade: %s", upgrade)
        if not dry_run:
            handler.mark_executing(upgrade)
            session.commit()
            handler.do_execute(upgrade, user, progress=progress)
        log.info("user '%s' executed upgrade: %s", user.username, upgrade)

    finalize_session(session, dry_run=dry_run)

    if (execute and not dry_run
        and keep_exit_code and upgrade.exit_code):
        sys.exit(upgrade.exit_code)
