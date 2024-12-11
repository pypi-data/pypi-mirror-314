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
Typer-based command utilities
"""

import datetime
import inspect
import logging
from pathlib import Path
from typing import List, Optional

import makefun
import typer
from typing_extensions import Annotated
from wuttjamaican.util import load_entry_points

from rattail.config import make_config
from rattail.progress import ConsoleProgress, SocketProgress


def make_typer(**kwargs):
    """
    Create a Typer command instance, per Rattail conventions.

    This function is used to create the top-level ``rattail`` command,
    :data:`~rattail.commands.base.rattail_typer`.  You can use it to
    create additional top-level commands for your app, as needed.

    :returns: ``typer.Typer`` instance
    """
    kwargs.setdefault('callback', typer_callback)
    return typer.Typer(**kwargs)


def typer_eager_imports(
        group: [typer.Typer, str]):
    """
    Eagerly import all modules which are registered as having
    subcommands belonging to the given group.

    This is used to locate subcommands which may be defined by
    multiple different packages.  It is mostly needed for the main
    ``rattail`` command, since e.g. various POS integration packages
    may define additional subcommands for it.

    Most custom apps will define their own top-level command and some
    subcommands, but will have no need to "discover" additional
    subcommands defined elsewhere.  Hence you normally would not need
    to call this function.

    However if you wish to define a ``rattail`` subcommand(s), you
    *would* need to register the entry point for your module(s)
    containing the subcommand(s) like so (in ``pyproject.toml``):

    .. code-block:: ini

       [project.entry-points."rattail.typer_imports"]
       poser = "poser.commands"

    Note that ``rattail.typer_imports`` indicates you are registering
    a module which defines ``rattail`` subcommands.  The ``poser``
    name is arbitrary but should match your package name.

    :param group: Typer group command, or the name of one.
    """
    if isinstance(group, typer.Typer):
        group = group.info.name
    load_entry_points(f'{group}.typer_imports')


def typer_callback(
        ctx: typer.Context,

        ##############################

        # nb. these first args are defined in wuttjamaican

        config_paths: Annotated[
            Optional[List[Path]],
            typer.Option('--config', '-c',
                         exists=True,
                         help="Config path (may be specified more than once)")] = None,

        plus_config_paths: Annotated[
            Optional[List[Path]],
            typer.Option('--plus-config',
                         exists=True,
                         help="Extra configs to load in addition to normal config")] = None,

        progress: Annotated[
            bool,
            typer.Option('--progress', '-P',
                          help="Report progress when relevant")] = False,

        # # fn = click.option('-V', '--version',
        # #                   is_flag=True,
        # #                   help="Show program version"
        # #                   )(fn)

        # fn = click.option('--stdout',
        #                   type=click.File('wb'),
        #                   help="Optional file to which STDOUT should be written"
        #                   )(fn)

        # fn = click.option('--stderr',
        #                   type=click.File('wb'),
        #                   help="Optional file to which STDERR should be written"
        #                   )(fn)

        ##############################

        # nb. the rest of these args are defined in rattail

        no_init: Annotated[
            bool,
            typer.Option('--no-init', '-n')] = False,

        no_extend_config: Annotated[
            bool,
            typer.Option('--no-extend-config')] = False,

        verbose: Annotated[
            bool,
            typer.Option('--verbose')] = False,

        progress_socket: Annotated[
            str,
            typer.Option(help="Optional socket (e.g. localhost:8487) to which progress "
                         "info should be written.")] = None,

        runas_username: Annotated[
            str,
            typer.Option('--runas', '-R',
                         help="Optional username to impersonate when running the command.  "
                         "This is only relevant for / used by certain commands.")] = None,

        versioning: Annotated[
            bool,
            typer.Option('--versioning',
                         help="Force *enable* of data versioning.  If set, then --no-versioning "
                         "cannot also be set.  If neither is set, config will determine whether "
                         "or not data versioning should be enabled.")] = False,

        no_versioning: Annotated[
            bool,
            typer.Option('--no-versioning',
                         help="Force *disable* of data versioning.  If set, then --versioning "
                         "cannot also be set.  If neither is set, config will determine whether "
                         "or not data versioning should be enabled.")] = False,

):
    """
    Generic callback for use with top-level commands.
    """
    config = make_cli_config(ctx)

    ctx.rattail_config = config

    ctx.rattail_progress = None
    if progress:
        if progress_socket:
            host, port = progress_socket.split(':')
            ctx.rattail_progress = SocketProgress(host, int(port))
        else:
            ctx.rattail_progress = ConsoleProgress


def make_cli_config(ctx):
    """
    Make a config object according to the command-line context
    (params).

    :param ctx: ``typer.Context`` instance

    :returns: :class:`~rattail.config.RattailConfig` instance
    """
    kwargs = ctx.params

    # if args say not to "init" then we make a sort of empty config
    if kwargs.get('no_init'):
        config = make_config([], extend=False, versioning=False)

    else: # otherwise we make a proper config, and maybe turn on versioning
        logging.basicConfig()
        config = make_config(files=kwargs.get('config_paths') or None,
                             plus_files=kwargs.get('plus_config_paths') or None,
                             extend=not kwargs.get('no_extend_config'),
                             versioning=False)
        if kwargs.get('versioning'):
            from rattail.db.config import configure_versioning
            configure_versioning(config, force=True)
        elif not kwargs.get('no_versioning'):
            try:
                from rattail.db.config import configure_versioning
            except ImportError:
                pass
            else:
                configure_versioning(config)

    # import our primary data model now, just in case it hasn't fully been
    # imported yet.  this it to be sure association proxies and the like
    # are fully wired up in the case of extensions
    # TODO: what about web apps etc.? i guess i was only having the problem
    # for some importers, e.g. basic CORE API -> Rattail w/ the schema
    # extensions in place from rattail-corepos
    app = config.get_app()
    try:
        app.model
    except ImportError:
        pass

    return config


def typer_get_runas_user(ctx, session=None):
    """
    Convenience function to get the "runas" User object for the
    current command.

    Uses :meth:`rattail.app.AppHandler.get_runas_user()` under the
    hood, but the ``--runas`` command line param provides the default
    username.
    """
    config = ctx.parent.rattail_config
    app = config.get_app()
    return app.get_runas_user(session=session,
                              username=ctx.parent.params['runas_username'])


def importer_command_template(

        # model names (aka importer keys)
        models: Annotated[
            Optional[List[str]],
            typer.Argument(help="Which data models to import.  If you specify any, then only "
                           "data for those models will be imported.  If you do not specify "
                           "any, then all *default* models will be imported.")] = None,

        # list models
        list_all_models: Annotated[
            bool,
            typer.Option('--list-all-models', '-l',
                         help="List all available models and exit.")] = False,
        list_default_models: Annotated[
            bool,
            typer.Option('--list-default-models',
                         help="List the default models and exit.")] = False,

        # make batches
        make_batches: Annotated[
            bool,
            typer.Option('--make-batches',
                         help="If specified, make new Import / Export Batches instead of "
                         "performing an actual (possibly dry-run) import.")] = False,

        # key / fields / exclude
        key: Annotated[
            str,
            typer.Option('--key',
                         help="List of fields (comma-separated string) which should be "
                         "used as \"primary key\" for the import.")] = None,
        fields: Annotated[
            str,
            typer.Option('--fields',
                         help="List of fields (comma-separated string) which should be "
                         "included in the import.  If this parameter is specified, then "
                         "any field not listed here, would be *excluded* regardless of "
                         "the --exclude-fields parameter.")] = None,
        exclude_fields: Annotated[
            str,
            typer.Option('--exclude-fields',
                         help="List of fields (comma-separated string) which should be "
                         "excluded from the import.  Any field not listed here, would be "
                         "included (or not) depending on the --fields parameter and/or "
                         "default importer behavior.")] = None,

        # fuzzy fields
        fuzzy_fields: Annotated[
            str,
            typer.Option(help="List of fields (comma-separated string) for which diff "
                         "comparison should be \"fuzzy\".  This is intended for "
                         "timestamps and similar values which vary in granularity "
                         "between systems.")] = None,
        fuzz_factor: Annotated[
            int,
            typer.Option(help="Numeric value for use with --fuzzy-fields.  For "
                         "timestamp fields, this refers to the number of seconds "
                         "by which values are allowed to differ and still be "
                         "considered a match.")] = 1,

        # allow create?
        create: Annotated[
            bool,
            typer.Option(help="Allow new records to be created during the import.")] = True,
        max_create: Annotated[
            int,
            typer.Option(help="Maximum number of records which may be created, after which a "
                         "given import task should stop.  Note that this applies on a per-model "
                         "basis and not overall.")] = None,

        # allow update?
        update: Annotated[
            bool,
            typer.Option(help="Allow existing records to be updated during the import.")] = True,
        max_update: Annotated[
            int,
            typer.Option(help="Maximum number of records which may be updated, after which a "
                         "given import task should stop.  Note that this applies on a per-model "
                         "basis and not overall.")] = None,

        # allow delete?
        delete: Annotated[
            bool,
            typer.Option(help="Allow records to be deleted during the import.")] = False,
        max_delete: Annotated[
            int,
            typer.Option(help="Maximum number of records which may be deleted, after which a "
                         "given import task should stop.  Note that this applies on a per-model "
                         "basis and not overall.")] = None,

        # max total changes, per model
        max_total: Annotated[
            int,
            typer.Option(help="Maximum number of *any* record changes which may occur, after which "
                         "a given import task should stop.  Note that this applies on a per-model "
                         "basis and not overall.")] = None,

        # date ranges
        start_date: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Optional (inclusive) starting point for date range, by which host "
                         "data should be filtered.  Only used by certain importers.")] = None,
        end_date: Annotated[
            datetime.datetime,
            typer.Option(formats=['%Y-%m-%d'],
                         help="Optional (inclusive) ending point for date range, by which host "
                         "data should be filtered.  Only used by certain importers.")] = None,
        year: Annotated[
            int,
            typer.Option(help="Optional year, by which data should be filtered.  Only used "
                         "by certain importers.")] = None,

        # TODO: deprecate --batch, replace with --batch-size ?
        # batch size
        batch_size: Annotated[
            int,
            typer.Option('--batch',
                         help="Split work to be done into batches, with the specified number of "
                         "records in each batch.  Or, set this to 0 (zero) to disable batching. "
                         "Implementation for this may vary somewhat between importers.")] = 200,

        # collect changes for processing
        collect_changes: Annotated[
            bool,
            typer.Option(help="Collect changes for processing at the end of the run.  "
                         "This is required for warning diff emails, but disabling it "
                         "can help to cut down on memory usage during the run.")] = True,

        # email diff warnings
        warnings: Annotated[
            bool,
            typer.Option('--warnings', '-W',
                         help="Set this flag if you expect a \"clean\" import, and wish for any "
                         "changes which do occur to be processed further and/or specially.  The "
                         "behavior of this flag is ultimately up to the import handler, but the "
                         "default is to send an email notification.")] = False,
        max_diffs: Annotated[
            int,
            typer.Option(help="Maximum number of \"diffs\" to display per warning type, in a "
                         "warning email.  Only used if --warnings is in effect.")] = None,

        # dry run?
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the full motions and allow logging etc. to "
                         "occur, but rollback (abort) the transaction at the end.  "
                         "Note that this flag is ignored if --make-batches is specified.")] = False,
):
    """
    Stub function which provides a common param signature; used with
    :func:`importer_command`.
    """


def importer_command(fn):
    """
    Decorator for import/export commands.  Adds common params based on
    :func:`importer_command_template`.
    """
    original_sig = inspect.signature(fn)
    reference_sig = inspect.signature(importer_command_template)

    params = list(original_sig.parameters.values())
    for i, param in enumerate(reference_sig.parameters.values()):
        params.insert(i + 1, param)

    # remove the **kwargs param
    params.pop(-1)

    final_sig = original_sig.replace(parameters=params)
    return makefun.create_function(final_sig, fn)


def file_exporter_command_template(
        output_dir: Annotated[
            Path,
            typer.Option(help="Directory to which output files should be written.  "
                         "Note that this is a *required* parameter.")] = ...,
):
    """
    Stub function to provide signature for exporter commands which
    produce data file(s) as output.  Used with
    :func:`file_exporter_command`.
    """


def file_exporter_command(fn):
    """
    Decorator for file export commands.  Adds common params based on
    :func:`file_exporter_command_template`.
    """
    original_sig = inspect.signature(fn)
    plain_import_sig = inspect.signature(importer_command_template)
    file_export_sig = inspect.signature(file_exporter_command_template)
    desired_params = (
        list(plain_import_sig.parameters.values())
        + list(file_export_sig.parameters.values()))

    params = list(original_sig.parameters.values())
    for i, param in enumerate(desired_params):
        params.insert(i + 1, param)

    # remove the **kwargs param
    params.pop(-1)

    final_sig = original_sig.replace(parameters=params)
    return makefun.create_function(final_sig, fn)


def file_importer_command_template(
        input_dir: Annotated[
            Path,
            typer.Option(exists=True,
                         help="Directory from which input files should be read.  "
                         "Note that this is a *required* parameter.")] = ...,
):
    """
    Stub function to provide signature for importer commands which
    require data file(s) as input.  Used with
    :func:`file_importer_command`.
    """


def file_importer_command(fn):
    """
    Decorator for file import commands.  Adds common params based on
    :func:`file_importer_command_template`.
    """
    original_sig = inspect.signature(fn)
    plain_import_sig = inspect.signature(importer_command_template)
    file_import_sig = inspect.signature(file_importer_command_template)
    desired_params = (
        list(plain_import_sig.parameters.values())
        + list(file_import_sig.parameters.values()))

    params = list(original_sig.parameters.values())
    for i, param in enumerate(desired_params):
        params.insert(i + 1, param)

    # remove the **kwargs param
    params.pop(-1)

    final_sig = original_sig.replace(parameters=params)
    return makefun.create_function(final_sig, fn)
