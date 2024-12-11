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
Backup commands
"""

from pathlib import Path
from typing import List

import typer
from typing_extensions import Annotated

from .base import rattail_typer
from rattail.backup import BackupHandler


@rattail_typer.command()
def backup(
        ctx: typer.Context,

        # db
        list_dbs: Annotated[
            bool,
            typer.Option('--list-dbs',
                         help="List all databases which may be backed up, then exit.")] = False,
        dbdump: Annotated[
            bool,
            typer.Option('--dbdump',
                         help="Dump some or all databases during the backup run.  Exactly "
                            "which databases are dumped, will depend on other parameters.")] = False,
        no_dbdump: Annotated[
            bool,
            typer.Option('--no-dbdump',
                         help="Do NOT dump any databases during the backup run.")] = False,
        included_dbs: Annotated[
            List[str],
            typer.Option('--dbdump-include',
                         help="Name of database to include in the dump.  May be specified "
                         "more than once.  Note that if this parameter is used, then ONLY "
                         "those databases specified will be backed up; the --dbdump-exclude "
                         "parameter(s) will be ignored.")] = None,
        excluded_dbs: Annotated[
            List[str],
            typer.Option('--dbdump-exclude',
                         help="Name of database to exclude from the dump.  May be specified "
                         "more than once.  Note that if the --dbdump-include parameter is "
                         "specified, then this parameter will be ignored.")] = None,
        dump_tables: Annotated[
            bool,
            typer.Option('--dump-tables',
                         help="Dump each table for specified databases, in addition to "
                         "the database as a whole.")] = False,
        no_dump_tables: Annotated[
            bool,
            typer.Option('--no-dump-tables',
                         help="Do *not* dump each table for each  database.")] = False,
        dbdump_output: Annotated[
            Path,
            typer.Option(help="Location of output folder for db dumps.")] = '/root/data',

        # rsync
        rsync: Annotated[
            bool,
            typer.Option('--rsync',
                         help="Push all files to remote location via rsync.")] = False,
        no_rsync: Annotated[
            bool,
            typer.Option('--no-rsync',
                         help="Do NOT push files to remote location via rsync.")] = False,
        rsync_included_prefixes: Annotated[
            List[str],
            typer.Option('--rsync-include',
                         help="File prefix which should be included in the rsync run.  "
                         "Actually, a separate rsync call is made for each prefix.  May "
                         "be specified more than once.  Note that if this parameter is "
                         "used, then ONLY those prefixes specified will be rsync'ed.  "
                         "Also, the --rsync-exclude parameter(s) will still apply.")] = None,
        rsync_excluded_prefixes: Annotated[
            List[str],
            typer.Option('--rsync-exclude',
                         help="File prefix which should be excluded from the rsync run.  "
                         "May be specified more than once.  Note that if the "
                         "--rsync-include parameter is specified, then this parameter(s) "
                         "will still apply also.")] = None,
        rsync_remote_host: Annotated[
            str,
            typer.Option(help="Assuming the rsync destination is another server, this should "
                         "be the hostname or IP address of that server.  Or you could set it "
                         "to an empty string, which signifies that the rsync remote "
                         "destination is another folder on localhost.")] = None,
        rsync_remote_prefix: Annotated[
            str,
            typer.Option(help="File prefix for the rsync destination.  If "
                         "--rsync-remote-host is an empty string, this prefix must exist "
                         "on localhost.  Otherwise the prefix must exist on the rsync "
                         "remote host.")] = None,

        # borg
        borg: Annotated[
            bool,
            typer.Option('--borg',
                         help="Create backup archive(s) via Borg.")] = False,
        no_borg: Annotated[
            bool,
            typer.Option('--no-borg',
                         help="Do NOT create backup archive(s) via Borg.")] = False,
        borg_remotes: Annotated[
            str,
            typer.Option(help="List (comma-separated string) of named \"remotes\" for "
                         "Borg, where archives should be created.")] = None,
        borg_included_prefixes: Annotated[
            List[str],
            typer.Option('--borg-include',
                         help="File prefix which should be included in the borg run.  "
                         "May be specified more than once.  If this is *not* specified "
                         "then --rsync-include will be used, if it is specified.  Note "
                         "that if this parameter is used, then ONLY those prefixes "
                         "specified will be included.  Also, the --borg-exclude "
                         "parameter(s) will still apply.")] = None,
        borg_excluded_prefixes: Annotated[
            List[str],
            typer.Option('--borg-exclude',
                         help="File prefix which should be excluded from the borg run.  "
                         "May be specified more than once.  If this is *not* specified "
                         "then --rsync-exclude will be used, if it is specified.  Note "
                         "that if the --borg-include parameter is specified, then this "
                         "parameter(s) will still apply also.")] = None,
        borg_tag: Annotated[
            str,
            typer.Option(help="Extra \"tag\" to embed within the name of the "
                         "Borg archive which is created.  Note that an archive "
                         "which is \"tagged\" in this way will never be pruned "
                         "by this `rattail backup` command!")] = None,

        # misc.
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through the motions as much as possible, to get an idea "
                         "of what the full backup would do, but don't actually do anything.")] = False,
):
    """
    Backup the database(s) and/or files for this machine
    """
    config = ctx.parent.rattail_config

    params = dict(ctx.params)
    params['verbose'] = ctx.parent.params['verbose']

    handler = BackupHandler(config)
    handler.execute(params)
