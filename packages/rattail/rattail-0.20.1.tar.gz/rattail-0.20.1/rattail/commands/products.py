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
Product-related commands
"""

import logging

import typer
from typing_extensions import Annotated

from .base import rattail_typer
from .typer import typer_get_runas_user


log = logging.getLogger(__name__)


@rattail_typer.command()
def update_costs(
        ctx: typer.Context,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                            "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Update (move future to current) costs for all products
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    user = typer_get_runas_user(ctx)
    do_update_costs(config, user, dry_run=dry_run, progress=progress)


def do_update_costs(config, user, dry_run=False, progress=None):
    from rattail.db.continuum import versioning_manager
    from rattail.db.util import finalize_session

    app = config.get_app()
    model = app.model
    session = app.make_session()
    user = session.get(model.User, user.uuid)
    session.set_continuum_user(user)
    products_handler = app.get_products_handler()

    # TODO: even if this works, it seems heavy-handed...
    # (also it *doesn't* work if ran before setting continuum user)
    uow = versioning_manager.unit_of_work(session)
    transaction = uow.create_transaction(session)
    transaction.meta = {'comment': "make future costs become current"}

    now = app.make_utc()
    future_costs = session.query(model.ProductFutureCost)\
                          .filter(model.ProductFutureCost.starts <= now)\
                          .all()
    log.info("found %s future costs which should become current", len(future_costs))

    def move(future, i):
        products_handler.make_future_cost_current(future)

    app.progress_loop(move, future_costs, progress,
                      message="Making future costs become current")

    finalize_session(session, dry_run=dry_run)
