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
Backup Handler
"""

import logging
import os
import shutil
import socket
import subprocess
import sys
import warnings

from rattail.app import GenericHandler


log = logging.getLogger(__name__)


class BackupHandler(GenericHandler):
    """
    Base class and default implementation for backup handler.
    """

    def execute(self, params):
        """
        Primary method for callers to invoke.  Runs a backup according
        to params and/or config.
        """
        if params['list_dbs']:

            mysql_names = self.get_mysql_names()
            if mysql_names:
                width = max([len(name) for name in mysql_names])
                sys.stdout.write("\nmysql\n")
                sys.stdout.write("{}\n".format('-' * width))
                for name in mysql_names:
                    sys.stdout.write("{}\n".format(name))

            postgres_names = self.get_postgres_names()
            if postgres_names:
                width = max([len(name) for name in postgres_names])
                sys.stdout.write("\npostgres\n")
                sys.stdout.write("{}\n".format('-' * width))
                for name in postgres_names:
                    sys.stdout.write("{}\n".format(name))

            if mysql_names or postgres_names:
                sys.stdout.write("\n")
            else:
                sys.stdout.write("no databases found\n")

        else: # not listing dbs, so will do dbdump and/or rsync and/or borg

            if params['dbdump'] and params['no_dbdump']:
                raise RuntimeError("Must specify either --dbdump or --no-dbdump, but not both")
            if params['dump_tables'] and params['no_dump_tables']:
                raise RuntimeError("May specify either --dump-tables or --no-dump-tables, but not both")
            if params['rsync'] and params['no_rsync']:
                raise RuntimeError("May specify either --rsync or --no-rsync, but not both")
            if params['borg'] and params['no_borg']:
                raise RuntimeError("May specify either --borg or --no-borg, but not both")

            # we dump dbs by default, unless user or config file says not to
            dbdump = params['dbdump']
            if not dbdump:
                if params['no_dbdump']:
                    dbdump = False
                else:
                    dbdump = self.config.getbool('rattail.backup', 'dbdump.enabled', usedb=False)
                    if dbdump is None:
                        dbdump = self.config.getbool('rattail.backup', 'dbdump',
                                                     usedb=False, ignore_ambiguous=True)
                        if dbdump is not None:
                            warnings.warn(f"URGENT: instead of 'dbdump', "
                                          f"you should set 'dbdump.enabled'",
                                          DeprecationWarning, stacklevel=2)
                        else:
                            dbdump = True
            if dbdump:

                outdir = params['dbdump_output']
                if not outdir:
                    outdir = self.config.get('rattail.backup', 'dbdump.output', default='/root/data')
                if not os.path.exists(outdir):
                    os.mkdir(outdir)

                if params['included_dbs']:
                    include = params['included_dbs']
                else:
                    include = self.config.getlist('rattail.backup', 'dbdump.include', usedb=False)

                if params['excluded_dbs']:
                    exclude = params['excluded_dbs']
                else:
                    exclude = self.config.getlist('rattail.backup', 'dbdump.exclude', usedb=False)

                if params['dump_tables']:
                    tables = True
                elif params['no_dump_tables']:
                    tables = False
                else:
                    tables = self.config.getbool('rattail.backups', 'dbdump.dump_tables', usedb=False, default=False)

                self.dump_mysql_databases(outdir, include=include, exclude=exclude, tables=tables,
                                          verbose=params['verbose'], dry_run=params['dry_run'])
                self.dump_postgres_databases(outdir, include=include, exclude=exclude, tables=tables,
                                             verbose=params['verbose'], dry_run=params['dry_run'])

            # we do *not* run rsync by default, unless user or config file says to
            rsync = params['rsync']
            rsync_last = False
            if not rsync:
                if params['no_rsync']:
                    rsync = False
                else:
                    rsync = self.config.getbool('rattail.backup', 'rsync.enabled', usedb=False)
                    if rsync is None:
                        rsync = self.config.getbool('rattail.backup', 'rsync',
                                                    usedb=False, ignore_ambiguous=True)
                        if rsync is not None:
                            warnings.warn(f"URGENT: instead of 'rsync', "
                                          f"you should set 'rsync.enabled'",
                                          DeprecationWarning, stacklevel=2)
                        else:
                            rsync = False
            if rsync:
                if self.config.getbool('rattail.backup', 'rsync.last', usedb=False, default=False):
                    rsync_last = True

            # we do *not* run borg by default, unless user or config file says to
            borg = False
            if params['borg'] or (not params['no_borg'] and self.config.getbool('rattail.backup', 'borg.enabled', usedb=False, default=False)):
                borg = True

            # okay now run rsync and/or borg (in whichever order) depending on params
            if rsync and not rsync_last:
                self.run_rsync(params)
            if borg:
                self.run_borg(params)
            if rsync and rsync_last:
                self.run_rsync(params)

    def run_rsync(self, params):
        self.rsync_files(include=params['rsync_included_prefixes'] or None,
                         exclude=params['rsync_excluded_prefixes'] or None,
                         verbose=params['verbose'],
                         dry_run=params['dry_run'])

    def run_borg(self, params):
        remotes = (self.config.parse_list(params['borg_remotes']) or
                   self.config.getlist('rattail.backup', 'borg.remotes',
                                       usedb=False))
        self.make_borg_archives(remotes,
                                include=params['borg_included_prefixes'] or params['rsync_included_prefixes'] or None,
                                exclude=params['borg_excluded_prefixes'] or params['rsync_excluded_prefixes'] or None,
                                tag=params['borg_tag'],
                                verbose=params['verbose'],
                                dry_run=params['dry_run'])

    def get_path_includes(self, typ='rsync'):
        return self.config.getlist('rattail.backup', f'{typ}.include', usedb=False, default=[
            '/etc',
            '/home',
            '/opt',
            '/root',
            '/srv',
            '/usr/local',
            '/var',
        ])

    def get_default_excludes(self):
        return [
            '/var/cache/',
        ]

    def get_path_excludes(self, typ='rsync'):
        return self.config.getlist('rattail.backup', '{}.exclude'.format(typ), usedb=False)

    def validate_prefixes(self, prefixes):
        for prefix in prefixes:
            if not prefix.startswith('/'):
                raise RuntimeError("Prefix is not absolute path: {}".format(prefix))

        for prefix in prefixes:
            others = list(prefixes)
            others.remove(prefix)
            for other in others:
                if other.startswith(prefix):
                    raise RuntimeError("Prefix {} is redundant due to prefix {}".format(
                        other, prefix))

    def rsync_files(self, include=None, exclude=None, verbose=False, dry_run=False):
        remote_host = self.config.require('rattail.backup', 'rsync.remote_host', usedb=False)
        remote_prefix = self.config.require('rattail.backup', 'rsync.remote_prefix', usedb=False)
        if not remote_prefix.startswith('/'):
            raise RuntimeError("Remote prefix is not absolute path: {}".format(remote_prefix))
        if remote_host:
            remote_prefix = '{}:{}'.format(remote_host, remote_prefix)

        if include:
            prefixes = include
        else:
            prefixes = self.get_path_includes(typ='rsync')
        self.validate_prefixes(prefixes)

        if exclude is None:
            exclude = self.get_path_excludes(typ='rsync')
            if not exclude:
                exclude = self.get_default_excludes()

        for prefix in prefixes:
            if not os.path.exists(prefix):
                log.warning("skipping prefix which doesn't exist locally: %s", prefix)
                continue

            excluded = []
            if exclude:
                excluded = [pattern for pattern in exclude if pattern.startswith(prefix)]
            log.info("running rsync for prefix: %s", prefix)

            parent = os.path.dirname(prefix)
            if parent == '/':
                destination = remote_prefix
                excludes = ['--exclude={}'.format(pattern) for pattern in excluded]

            else: # prefix parent is not root (/) dir
                destination = '{}{}/'.format(remote_prefix, parent)

                # exclusion patterns must apparently be relative in this case,
                # i.e. to the topmost folder being synced
                excludes = []
                for pattern in excluded:
                    pattern = '/'.join(pattern.split('/')[2:])
                    excludes.append('--exclude={}'.format(pattern))

                # and must also create the parent folder on remote side
                cmd = ['rsync', '--dirs', '--perms', '--times', '--group', '--owner', parent, remote_prefix]
                log.debug("rsync command is: %s", cmd)
                if not dry_run:
                    subprocess.check_call(cmd)

            # okay let's rsync
            rsync = ['rsync', '--archive', '--delete-during', '--partial']
            if verbose:
                rsync.append('--progress')
            cmd = rsync + excludes + [prefix, destination]
            log.debug("rsync command is: %s", cmd)
            if not dry_run:
                try:
                    subprocess.check_call(cmd)
                except subprocess.CalledProcessError as error:
                    # nb. rsync exits with code 24 when scenario is
                    # "Partial transfer due to vanished source files"
                    # but that just means all that could be synced, was
                    # synced, though some could not be synced.  we do
                    # not consider that a serious issue, so want to
                    # avoid the outright error here.
                    if error.returncode != 24:
                        raise
                    log.warning("rsync command exited with code 24")

    def make_borg_archives(self, remotes, include=None, exclude=None,
                           tag=None, verbose=False, dry_run=False):

        borg = self.config.get('rattail.backup', 'borg.command', usedb=False)
        if not borg:
            borg = self.config.get('rattail.backup', 'borg', usedb=False,
                                   ignore_ambiguous=True)
            if borg:
                warnings.warn(f"URGENT: instead of 'borg', "
                              f"you should set 'borg.command'",
                              DeprecationWarning, stacklevel=2)
            else:
                borg = os.path.join(os.path.dirname(sys.executable), 'borg')
                if not os.path.exists(borg):
                    borg = subprocess.check_output('which borg')

        if include:
            prefixes = include
        else:
            prefixes = self.get_path_includes(typ='borg')
            if not prefixes:
                prefixes = self.get_path_includes(typ='rsync')
        self.validate_prefixes(prefixes)

        if exclude is None:
            exclude = self.get_path_excludes(typ='borg')
            if not exclude:
                exclude = self.get_path_excludes(typ='rsync')
                if not exclude:
                    exclude = self.get_default_excludes()

        hostname = self.config.get('rattail.backup', 'borg.archive_hostname', usedb=False)
        if not hostname:
            hostname = socket.gethostname()

        for remote in remotes:

            # borg_env
            repo = self.config.require('rattail.backup', 'borg.remote.{}.repo'.format(remote), usedb=False)
            passphrase = self.config.require('rattail.backup', 'borg.remote.{}.passphrase'.format(remote), usedb=False)
            remote_borg = self.config.get('rattail.backup', 'borg.remote.{}.borg'.format(remote), usedb=False)
            borg_env = {
                'HOME': os.environ['HOME'],
                'BORG_REPO': repo,
                'BORG_PASSPHRASE': passphrase,
                'BORG_REMOTE_PATH': remote_borg or 'borg',
            }

            # borg create
            cmd = [borg, 'create',
                   '--compression', 'lz4',
                   '--exclude-caches']
            if verbose:
                cmd.extend([
                    '--verbose',
                    '--list',
                    '--filter', 'AME',
                    '--stats',
                    '--show-rc',
                ])

            for pattern in exclude:
                cmd.extend(['--exclude', pattern])

            if tag:
                # note that in this case our hostname will be immediately
                # followed by a colon instead of hyphen.  this is what "breaks"
                # the typical pattern and ensures this tagged archive will not
                # be pruned under typical command runs.
                archive_name = '::{}:{}-{{now}}'.format(hostname, tag)
            else:
                archive_name = '::{}-{{now}}'.format(hostname)
            cmd.append(archive_name)

            for prefix in prefixes:
                cmd.append(prefix)

            # run `borg create`
            log.debug("borg create command is: %s", cmd)
            if not dry_run:
                try:
                    subprocess.check_call(cmd, env=borg_env)
                except subprocess.CalledProcessError as error:
                    # nb. borg exits with code 1 for "warning" but
                    # this is different than "error" - cf. also
                    # https://borgbackup.readthedocs.io/en/latest/man_intro.html#return-codes
                    if error.returncode != 1:
                        raise
                    log.warning("borg create command exited with code 1")

            # the only thing left is to prune, which if we're tagging, we
            # probably should just skip.  maybe let command line override?
            if tag:
                return

            # generate --keep args for prune, based on config
            keep = []
            keep_defaults = {
                'daily': '7',
                'weekly': '4',
                'monthly': '6',
            }
            for typ, default in keep_defaults.items():
                value = self.config.get('rattail.backup', 'borg.keep.{}'.format(typ))
                if value is None:
                    keep.extend(['--keep-{}'.format(typ), default])
                elif value.isdigit():
                    keep.extend(['--keep-{}'.format(typ), int(value)])
                elif self.config.parse_bool(value):
                    keep.extend(['--keep-{}'.format(typ), default])

            # borg prune
            cmd = [borg, 'prune',
                   '--glob-archives', '{}-*'.format(hostname)] + keep
            if verbose:
                cmd.extend([
                    '--list',
                    '--show-rc',
                ])

            log.debug("borg prune command is: %s", cmd)
            if not dry_run:
                subprocess.check_call(cmd, env=borg_env)

    def get_mysql_names(self, include=None, exclude=None, exclude_builtin=True):
        try:
            output = subprocess.check_output([
                'mysql', '--execute', "show databases;",
                '--batch', '--skip-column-names',
            ])
        except Exception as error:
            if isinstance(error, FileNotFoundError):
                # assuming there is no mysql binary
                return []
            raise
        output = output.decode('ascii') # TODO: how to detect this etc.?

        names = output.split('\n')
        names = [name.strip() for name in names if name.strip()]

        if exclude_builtin:
            builtins = [
                'mysql',
                'information_schema',
                'performance_schema',
                'sys',
            ]
            for name in builtins:
                if name in names:
                    names.remove(name)

        return self.filter_names(names, include, exclude)

    def get_mysql_tables(self, database):
        try:
            output = subprocess.check_output([
                'mysql', '--execute', "show tables;",
                '--batch', '--skip-column-names',
                database,
            ])
        except Exception as error:
            if isinstance(error, FileNotFoundError):
                # assuming there is no mysql binary
                return []
            raise
        output = output.decode('ascii') # TODO: how to detect this etc.?

        names = output.split('\n')
        names = [name.strip() for name in names if name.strip()]
        return names

    def get_postgres_names(self, include=None, exclude=None, exclude_builtin=True):
        """
        Returns a list of database names found in PostgreSQL, filtered
        according to the various arguments provided.
        """
        names = []

        # can only use `psql` if it's present, so check first
        with open(os.devnull, 'w') as devnull:
            psql_exists = subprocess.call(['which', 'psql'], stdout=devnull) == 0
        if psql_exists:

            output = subprocess.check_output([
                'sudo', '-u', 'postgres', 'psql', '--list', '--tuples-only',
            ])
            output = output.decode('ascii') # TODO: how to detect this etc.?

            for line in output.split('\n'):
                line = line.strip()
                if line and '|' in line and not line.startswith('|'):
                    name = line.split('|')[0].strip()
                    names.append(name)

        if names and exclude_builtin:
            builtins = [
                'postgres',
                'template0',
                'template1',
            ]
            for name in builtins:
                if name in names:
                    names.remove(name)

        return self.filter_names(names, include, exclude)

    def filter_names(self, names, include, exclude):
        if include:
            names = [name for name in names if name in include]
        elif exclude:
            names = [name for name in names if name not in exclude]
        return names

    def dump_mysql_databases(self, outdir, include=None, exclude=None, tables=False,
                             verbose=False, dry_run=False):
        names = self.get_mysql_names(include=include, exclude=exclude)
        for name in names:
            log.info("dumping mysql db: %s", name)

            # generate mysqldump command
            sql_path = os.path.join(outdir, '{}-mysql.sql'.format(name))
            mysqldump = ['mysqldump']
            if verbose:
                mysqldump.append('--verbose')
            cmd = mysqldump + [name, '--result-file={}'.format(sql_path)]
            log.debug("mysqldump command is: %s", cmd)

            # run mysqldump command
            if not dry_run:
                subprocess.check_call(cmd)
                subprocess.check_call(['gzip', '--force', sql_path])
                gz_path = "{}.gz".format(sql_path)
                log.debug("database dump completed, file is at %s", gz_path)

            if tables:

                # first, forcibly recreate 'tables' dir for this db
                if not dry_run:
                    tablesdir = os.path.join(outdir, 'tables', 'mysql-{}'.format(name))
                    if os.path.exists(tablesdir):
                        shutil.rmtree(tablesdir)
                    os.makedirs(tablesdir)

                # then make a dump of each table reported by 'show tables'
                for table in self.get_mysql_tables(name):
                    log.info("dumping mysql table: %s", table)

                    # generate mysqldump command
                    sql_path = os.path.join(tablesdir, '{}.sql'.format(table))
                    mysqldump = ['mysqldump']
                    if verbose:
                        mysqldump.append('--verbose')
                    cmd = mysqldump + [name, table, '--result-file={}'.format(sql_path)]
                    log.debug("mysqldump command is: %s", cmd)

                    # run mysqldump command
                    if not dry_run:
                        subprocess.check_call(cmd)
                        subprocess.check_call(['gzip', '--force', sql_path])
                        gz_path = "{}.gz".format(sql_path)
                        log.debug("table dump completed, file is at %s", gz_path)

    def dump_postgres_databases(self, outdir, include=None, exclude=None, tables=False,
                                verbose=False, dry_run=False):
        names = self.get_postgres_names(include=include, exclude=exclude)
        for name in names:
            log.info("dumping postgres db: %s", name)

            sql_path = os.path.join(outdir, '{}-postgres.sql'.format(name))
            gz_path = f"{sql_path}.gz"
            tmp_path = f'/tmp/{name}.sql.gz'

            pg_dump = 'sudo -u postgres pg_dump'
            if verbose:
                pg_dump += ' --verbose'
            pg_dump += f" {name} | gzip -c > {tmp_path}"
            cmd = ['bash', '-c', pg_dump]

            logger = log.info if dry_run else log.debug
            logger("pg_dump command is: %s", cmd)

            if not dry_run:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                subprocess.check_call(cmd)
                subprocess.check_call(['chown', 'root:', tmp_path])
                subprocess.check_call(['mv', tmp_path, gz_path])
                log.debug("dump completed, file is at %s", gz_path)

        if tables:
            log.info("TODO: should honor --dump-tables flag for postgres")
