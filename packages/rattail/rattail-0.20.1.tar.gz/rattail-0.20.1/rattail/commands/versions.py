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
Versioning Commands
"""

import sys
import logging
from typing import List

import typer
from typing_extensions import Annotated

from .base import rattail_typer


log = logging.getLogger(__name__)


@rattail_typer.command()
def purge_versions(
        ctx: typer.Context,
        list_models: Annotated[
            bool,
            typer.Option('--list', '-l',
                         help="Show list of all model names, for which version tables exist.")] = False,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Purge version data for some or all tables
    """
    from rattail.db.util import finalize_session

    config = ctx.parent.rattail_config
    app = config.get_app()

    if not config.versioning_enabled():
        sys.stderr.write("Continuum versioning is not enabled, per config\n")
        sys.exit(1)

    if list_models:
        do_list_models(config)

    else:
        session = app.make_session()
        do_purge_models(config, session)
        finalize_session(session, dry_run=dry_run)


@rattail_typer.command()
def version_check(
        ctx: typer.Context,
        models: Annotated[
            List[str],
            typer.Argument(help="Which data models to check.  If you specify any, then only "
                           "data for those models will be checked.  If you do not specify "
                           "any, then all supported models will be checked.")] = None,
        list_models: Annotated[
            bool,
            typer.Option('--list', '-l',
                         help="Show list of all model names, for which version tables exist.")] = False,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                           help="Go through the full motions and allow logging etc. to "
                           "occur, but rollback (abort) the transaction at the end.")] = False,
):
    """
    Run consistency checks for version data tables
    """
    from rattail.db.util import finalize_session

    config = ctx.parent.rattail_config
    app = config.get_app()

    if not config.versioning_enabled():
        sys.stderr.write("Continuum versioning is not enabled, per config\n")
        sys.exit(1)

    if list_models:
        do_list_models(config)

    else:
        session = app.make_session()
        do_version_checks(config, session, models)
        finalize_session(session, dry_run=dry_run)


def collect_models(config):
    """
    Gather and return a dict of data model classes, for which version
    tables exist.
    """
    import sqlalchemy_continuum as continuum

    app = config.get_app()
    model = app.model

    # first we collect names of "potential" model classes
    names = []
    for name in dir(model):
        obj = getattr(model, name)
        if isinstance(obj, type):
            if issubclass(obj, model.Base):
                names.append(name)

    # next we find out if each has a version class
    models = {}
    for name in sorted(names):
        cls = getattr(model, name)
        try:
            vcls = continuum.version_class(cls)
        except continuum.ClassNotVersioned:
            pass
        else:
            models[name] = cls

    return models


def do_list_models(config):
    """
    Display a list of all version tables in the DB.
    """
    models = collect_models(config)
    if models:
        for name in sorted(models):
            sys.stdout.write(f"{name}\n")
    else:
        log.warning("hm, no version classes found; is versioning enabled?")


def do_purge_models(config, session):
    """
    Purge version data for all given models.
    """
    import sqlalchemy as sa

    models = collect_models(config)
    if not models:
        log.warning("i have no models to purge!")
        return

    for name, cls in sorted(models.items()):
        purge_version_data(config, session, cls)

    sys.stdout.write("purged all data for {} version tables\n".format(len(models)))

    log.debug("will now purge data for transaction_meta table")
    session.execute(sa.text('truncate "transaction_meta"'))
    log.debug("will now purge data for transaction table")
    session.execute(sa.text('truncate "transaction"'))
    sys.stdout.write("purged all data for 2 transaction tables\n")


def purge_version_data(config, session, cls):
    """
    Purge version data for the given model class.
    """
    import sqlalchemy as sa
    import sqlalchemy_continuum as continuum

    vcls = continuum.version_class(cls)
    vtable = vcls.__table__

    log.debug("will now purge data for version table: %s", vtable.name)
    session.execute(sa.text('truncate "{}"'.format(vtable.name)))
    sys.stdout.write("purged data for: {}\n".format(vtable.name))


def do_version_checks(config, session, models):
    """
    Run version data checks for all given models.
    """
    requested = models
    all_models = collect_models(config)
    if requested:
        models = dict([(k, v)
                       for k, v in all_models.items()
                       if k in requested])
    else:
        models = all_models
    if not models:
        log.warning("i have no models to check!")
        return

    for name, cls in sorted(models.items()):
        check_versions(config, session, cls)

    log.info("checked version data for %s models", len(models))


def check_versions(config, session, cls, progress=None):
    """
    Check version data for the given model class.
    """
    import sqlalchemy_continuum as continuum

    app = config.get_app()
    model_name = cls.__name__
    log.debug("will now check version data for model: %s", model_name)

    vcls = continuum.version_class(cls)
    versions = session.query(vcls)\
                      .order_by(vcls.transaction_id)\
                      .all()
    versions_by_uuid = {}
    result = app.make_object(problems=0)

    def organize(version, i):
        versions_by_uuid.setdefault(version.uuid, []).append(version)

    app.progress_loop(organize, versions, progress,
                      message=f"Organizing version data for {model_name}")

    def check(uuid, i):
        versions = versions_by_uuid[uuid]

        # sanity check the sequence of operations
        lastop = None
        for version in versions:
            if lastop is None:
                if version.operation_type != continuum.Operation.INSERT:
                    log.warning("first version should be INSERT for %s %s",
                                model_name, uuid)
                    result.problems += 1
            elif version.operation_type == continuum.Operation.INSERT:
                if lastop == continuum.Operation.UPDATE:
                    log.warning("INSERT following UPDATE for %s %s",
                                model_name, uuid)
                    result.problems += 1
            elif version.operation_type == continuum.Operation.UPDATE:
                if lastop == continuum.Operation.DELETE:
                    log.warning("UPDATE following DELETE for %s %s",
                                model_name, uuid)
                    result.problems += 1
            lastop = version.operation_type

    app.progress_loop(check, list(versions_by_uuid.keys()), progress,
                      message=f"Checking version data for {model_name}")

    log.info("found %s problems for model: %s", result.problems, model_name)

