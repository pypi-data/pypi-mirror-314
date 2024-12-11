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
Importing Commands
"""

import datetime
import sys
import logging

import typer
from typing_extensions import Annotated

from rattail.app import GenericHandler
from .base import rattail_typer
from .typer import (typer_get_runas_user, importer_command,
                    file_importer_command, file_exporter_command)


log = logging.getLogger(__name__)


class ImportCommandHandler(GenericHandler):
    """
    Responsible for handling import/export command line runs.
    """

    def __init__(self, config, import_handler_key=None, import_handler_spec=None, **kwargs):
        super().__init__(config, **kwargs)

        if not import_handler_key and not import_handler_spec:
            raise ValueError("must provide either import_handler_key or import_handler_spec")

        self.import_handler_key = import_handler_key
        self.import_handler_spec = import_handler_spec

    def run(self, params, progress=None):

        if params['list_all_models']:
            self.list_all_models(params)
            return

        if params['list_default_models']:
            self.list_default_models(params)
            return

        handler = self.get_handler(params)
        models = params['models'] or handler.get_default_keys()
        log.debug("using handler: %s", handler)
        log.debug("importing models: %s", models)
        log.debug("params are: %s", params)

        kwargs = {
            'warnings': params['warnings'],
            'fields': self.config.parse_list(params['fields']),
            'exclude_fields': self.config.parse_list(params['exclude_fields']),
            'fuzzy_fields': self.config.parse_list(params['fuzzy_fields']),
            'fuzz_factor': params['fuzz_factor'],
            'create': params['create'],
            'max_create': params['max_create'],
            'update': params['update'],
            'max_update': params['max_update'],
            'delete': params['delete'],
            'max_delete': params['max_delete'],
            'max_total': params['max_total'],
            'start_date': params['start_date'],
            'end_date': params['end_date'],
            'progress': progress,
        }

        # ensure we have dates here, not datetime
        if kwargs['start_date'] and isinstance(kwargs['start_date'], datetime.datetime):
            kwargs['start_date'] = kwargs['start_date'].date()
        if kwargs['end_date'] and isinstance(kwargs['end_date'], datetime.datetime):
            kwargs['end_date'] = kwargs['end_date'].date()

        if params['make_batches']:
            kwargs.update({
                'runas_user': params['user'],
            })
            handler.make_batches(*models, **kwargs)
        else:
            kwargs.update({
                'key_fields': self.config.parse_list(params['key']) if params['key'] else None,
                'dry_run': params['dry_run'],
            })
            handler.import_data(*models, **kwargs)

        # TODO: should this logging happen elsewhere / be customizable?
        if params['dry_run']:
            log.info("dry run, so transaction was rolled back")
        else:
            log.info("transaction was committed")

    def get_handler_factory(self, params, **kwargs):
        """
        Should return an ImportHandler factory (e.g. class) which will
        later be called to create a handler instance.
        """
        # use explicit spec if one was provided
        if self.import_handler_spec:
            return self.app.load_object(self.import_handler_spec)

        # otherwise lookup the handler based on key
        # nb. normal logic returns an instance but we want its class
        handler = self.app.get_import_handler(self.import_handler_key, require=True)
        return type(handler)

    def get_handler(self, params, **kwargs):
        """
        Returns a handler instance to be used by the command.
        """
        factory = self.get_handler_factory(params)
        user = params['user']
        if user:
            kwargs.setdefault('runas_user', user)
            kwargs.setdefault('runas_username', user.username)
        kwargs.setdefault('dry_run', params['dry_run'])
        kwargs.setdefault('collect_changes_for_processing', params['collect_changes'])
        kwargs.setdefault('batch_size', params['batch_size'])
        if params['max_diffs']:
            kwargs.setdefault('diff_max_display', params['max_diffs'])
        if params.get('handler_kwargs'):
            kwargs.update(params['handler_kwargs'])
        return factory(self.config, **kwargs)

    def list_all_models(self, params):
        handler = self.get_handler(params)
        if not handler:
            sys.stderr.write("no handler configured!\n")
            if self.import_handler_key:
                sys.stderr.write(f"handler key is: {self.import_handler_key}\n")
            sys.exit(1)
        sys.stdout.write("ALL MODELS:\n")
        sys.stdout.write("==============================\n")
        defaults = handler.get_default_keys()
        for key in handler.get_importer_keys():
            sys.stdout.write(key)
            if key in defaults:
                sys.stdout.write(" (*)")
            sys.stdout.write("\n")
        sys.stdout.write("==============================\n")
        sys.stdout.write("(*) means also default\n")

    def list_default_models(self, params):
        handler = self.get_handler(params)
        sys.stdout.write("DEFAULT MODELS:\n")
        sys.stdout.write("==============================\n")
        for key in handler.get_default_keys():
            sys.stdout.write(f"{key}\n")


@rattail_typer.command()
@file_exporter_command
def export_csv(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data from Rattail to CSV file(s)
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_csv.from_rattail.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'output_dir': kwargs['output_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def export_rattail(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the \"target\" "
                         "Rattail system, i.e. where data will be exported.  This key must "
                         "be defined in the [rattail.db] section of your config file.")] = 'host',
        **kwargs
):
    """
    Export data to another Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_rattail.export')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@file_importer_command
def import_csv(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from CSV file(s) to Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_csv.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'input_dir': kwargs['input_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@file_importer_command
def import_ifps(
        ctx: typer.Context,
        **kwargs
):
    """
    Import data from IFPS file(s) to Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_ifps.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'input_dir': kwargs['input_dir']}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_rattail(
        ctx: typer.Context,
        dbkey: Annotated[
            str,
            typer.Option(help="Config key for database engine to be used as the Rattail "
                         "\"host\", i.e. the source of the data to be imported.  This key "
                         "must be defined in the [rattail.db] section of your config file.  "
                         "Defaults to 'host'.")] = 'host',
        **kwargs
):
    """
    Import data from another Rattail database
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail.from_rattail.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'dbkey': dbkey}
    handler.run(kwargs, progress=progress)


@rattail_typer.command()
@importer_command
def import_versions(
        ctx: typer.Context,
        comment: Annotated[
            str,
            typer.Option('--comment', '-m',
                         help="Comment to be recorded with the transaction."
                         )] = "import catch-up versions",
        **kwargs
):
    """
    Make initial versioned records for data models
    """
    config = ctx.parent.rattail_config

    if not config.versioning_has_been_enabled:
        sys.stderr.write("Continuum versioning is not enabled, "
                         "per config and/or command line args\n")
        sys.exit(1)

    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_key='to_rattail_versions.from_rattail.import')
    kwargs['user'] = typer_get_runas_user(ctx)
    kwargs['handler_kwargs'] = {'comment': comment}
    handler.run(kwargs, progress=progress)
