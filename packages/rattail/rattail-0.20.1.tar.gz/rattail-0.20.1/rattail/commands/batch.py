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
Batch-related commands
"""

import datetime
import inspect
import json
import logging
import os
import sys
from pathlib import Path

import makefun
import typer
from typing_extensions import Annotated

from .base import rattail_typer
from .typer import typer_get_runas_user
from rattail.util import simple_error


log = logging.getLogger(__name__)


def batch_action_command_template(
        batch_type: Annotated[
            str,
            typer.Option(help="Type of batch to be dealt with, e.g. 'vendor_catalog'")] = ...,
        batch_uuid: Annotated[
            str,
            typer.Argument(help="UUID of the batch to be processed.")] = ...,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Stub function which provides a common param signature; used with
    :func:`batch_action_command`.
    """


def batch_action_command(fn):
    """
    Decorator for batch handler commands.  Adds common params based on
    :func:`batch_action_command_template`.
    """
    original_sig = inspect.signature(fn)
    reference_sig = inspect.signature(batch_action_command_template)

    params = list(original_sig.parameters.values())
    for i, param in enumerate(reference_sig.parameters.values()):
        params.insert(i + 1, param)

    # remove the **kwargs param
    params.pop(-1)

    final_sig = original_sig.replace(parameters=params)
    return makefun.create_function(final_sig, fn)


@rattail_typer.command()
def make_batch(
        ctx: typer.Context,
        batch_type: Annotated[
            str,
            typer.Argument(help="Type of batch to be created, e.g. 'vendor_catalog'")] = ...,
        input_file: Annotated[
            Path,
            typer.Option(help="Path to single input file, to be used as data "
                         "source for the new batch.  (File format will vary "
                         "depending on batch type.)")] = ...,
        create_kwargs: Annotated[
            str,
            typer.Option('--kwargs',
                         parser=json.loads,
                         help="Optional JSON-encoded string containing extra "
                         "keyword arguments to be passed to the handler's batch "
                         "creation logic.")] = None,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Make a new batch, from a data file
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    params = dict(ctx.params)

    user = typer_get_runas_user(ctx)
    do_run(config, params['batch_type'], do_make_batch, user, params, progress=progress)


@rattail_typer.command()
@batch_action_command
def auto_receive(
        ctx: typer.Context,
        **kwargs
):
    """
    Auto-receive all items in a receiving batch
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    params = dict(kwargs)
    params.update(ctx.params)

    user = typer_get_runas_user(ctx)
    do_run(config, params['batch_type'], do_auto_receive, user, params, progress=progress)


@rattail_typer.command()
@batch_action_command
def execute_batch(
        ctx: typer.Context,
        execute_kwargs: Annotated[
            str,
            typer.Option('--kwargs',
                         parser=json.loads,
                         help="Optional JSON-encoded string containing extra "
                         "keyword arguments to be passed to the handler's batch "
                         "execution function.")] = None,
        **kwargs
):
    """
    Execute a batch
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    params = dict(kwargs)
    params.update(ctx.params)

    user = typer_get_runas_user(ctx)
    do_run(config, params['batch_type'], do_execute_batch, user, params, progress=progress)


@rattail_typer.command()
@batch_action_command
def populate_batch(
        ctx: typer.Context,
        **kwargs
):
    """
    Populate initial data for a batch
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    params = dict(kwargs)
    params.update(ctx.params)

    user = typer_get_runas_user(ctx)
    do_run(config, params['batch_type'], do_populate_batch, user, params, progress=progress)


@rattail_typer.command()
@batch_action_command
def refresh_batch(
        ctx: typer.Context,
        **kwargs
):
    """
    Refresh data for a batch
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress

    params = dict(kwargs)
    params.update(ctx.params)

    user = typer_get_runas_user(ctx)
    do_run(config, params['batch_type'], do_refresh_batch, user, params, progress=progress)


@rattail_typer.command()
def purge_batches(
        ctx: typer.Context,
        list_types: Annotated[
            bool,
            typer.Option('--list-types',
                         help="If set, list available batch types instead of trying "
                         "to purge anything.")] = False,
        batch_type: Annotated[
            str,
            typer.Option(help="Type of batch to be purged, e.g. 'vendor_catalog'")] = ...,
        before: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Purge all batches executed prior to this date.  If not "
                         "specified, will use --before-days to calculate instead.")] = None,
        before_days: Annotated[
            int,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Number of days before the current date, to be used "
                         "as the cutoff date if --before is not specified.  Default "
                         "is 90 days before current date.")] = 90,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Purge old batches from the database
    """
    from rattail.batch.handlers import get_batch_types
    from rattail.db.util import finalize_session

    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    app = config.get_app()

    if list_types:
        keys = get_batch_types(config)
        for key in keys:
            sys.stdout.write(f"{key}\n")
        return

    handler = app.get_batch_handler(batch_type)
    session = app.make_session()

    kwargs = {'dry_run': dry_run,
              'progress': progress}
    if before:
        kwargs['before'] = app.localtime(before)
    else:
        kwargs['before_days'] = before_days

    handler.purge_batches(session, **kwargs)
    finalize_session(session, dry_run=dry_run)


def do_run(config, batch_type, action_func, user, params, progress=None):
    from rattail.db.util import finalize_session

    app = config.get_app()
    handler = app.get_batch_handler(batch_type)
    session = app.make_session()
    model = app.model
    user = session.get(model.User, user.uuid)

    try:
        success = action_func(config, params, handler, session, user, progress=progress)
    except Exception as error:
        log.warning("handler action failed", exc_info=True)
        # nb. only write "simple" error string to stdout, in case
        # caller (e.g. web app) is capturing that for display to
        # user.  admin can consult logs if more info is needed.
        # we do *not* write to stderr, because logging probably
        # is already doing that; we want to avoid mixing them.
        # TODO: this admittedly seems brittle, maybe caller should
        # pass command line flags to control this?
        sys.stdout.write(simple_error(error))
        session.rollback()
        session.close()
        sys.exit(42)

    finalize_session(session, dry_run=params['dry_run'], success=success)


def do_make_batch(config, params, handler, session, user, progress=None):
    """
    This will create a new batch of the specified type, then populate it
    with the given data file.
    """
    if not os.path.exists(params['input_file']):
        raise RuntimeError("input file path does not exist: {}".format(params['input_file']))

    app = config.get_app()
    kwargs = dict(params['create_kwargs'])
    delete_if_empty = kwargs.pop('delete_if_empty', False)
    auto_execute_allowed = kwargs.pop('auto_execute_allowed', True)

    batch = handler.make_batch(session, created_by=user, **kwargs)
    handler.set_input_file(batch, params['input_file'])
    handler.do_populate(batch, user)

    if delete_if_empty:
        session.flush()
        if not batch.data_rows:
            log.debug("auto-deleting empty '%s' batch: %s", handler.batch_key, batch)
            handler.do_delete(batch, dry_run=params['dry_run'],
                              progress=progress)
            batch = None

    if batch and auto_execute_allowed and handler.auto_executable(batch):
        handler.execute(batch, user=user)
        batch.executed = app.make_utc()
        batch.executed_by = user

    return True


def do_auto_receive(config, params, handler, session, user, progress=None):
    batch = session.get(handler.batch_model_class, params['batch_uuid'])
    if not batch:
        raise RuntimeError(f"Batch of type '{params['batch_type']}' "
                           "not found: {params['batch_uuid']}")

    return handler.auto_receive_all_items(batch, progress=progress)


def do_execute_batch(config, params, handler, session, user, progress=None):
    batch = session.get(handler.batch_model_class, params['batch_uuid'])
    if not batch:
        raise RuntimeError(f"Batch of type '{params['batch_type']}' "
                           "not found: {params['batch_uuid']}")

    return handler.do_execute(batch, user, progress=progress, **params['execute_kwargs'])


def do_populate_batch(config, params, handler, session, user, progress=None):
    batch = session.get(handler.batch_model_class, params['batch_uuid'])
    if not batch:
        raise RuntimeError(f"Batch of type '{params['batch_type']}' "
                           "not found: {params['batch_uuid']}")

    return handler.do_populate(batch, user, progress=progress)


def do_refresh_batch(config, params, handler, session, user, progress=None):
    batch = session.get(handler.batch_model_class, params['batch_uuid'])
    if not batch:
        raise RuntimeError(f"Batch of type '{params['batch_type']}' "
                           "not found: {params['batch_uuid']}")

    return handler.do_refresh(batch, user, progress=progress)
