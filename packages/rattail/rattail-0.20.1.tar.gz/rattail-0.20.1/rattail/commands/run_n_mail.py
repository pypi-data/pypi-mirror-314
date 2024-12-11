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
``rattail run-n-mail`` command
"""

import logging
import subprocess
import sys

import humanize
import typer
from typing_extensions import Annotated

from .base import rattail_typer


log = logging.getLogger(__name__)


@rattail_typer.command()
def run_n_mail(
        ctx: typer.Context,
        skip_if_empty: Annotated[
            bool,
            typer.Option('--skip-if-empty',
                         help="Skip sending the email if the command generates no output.")] = False,
        key: Annotated[
            str,
            typer.Option(help="Config key for email settings")] = 'run_n_mail',

        # TODO: these all seem like good ideas, but not needed yet?
        # parser.add_argument('--from', '-F', metavar='ADDRESS',
        #                     help="Override value of From: header")
        # parser.add_argument('--to', '-T', metavar='ADDRESS',
        #                     help="Override value of To: header (may specify more than once)")
        # parser.add_argument('--cc', metavar='ADDRESS',
        #                     help="Override value of Cc: header (may specify more than once)")
        # parser.add_argument('--bcc', metavar='ADDRESS',
        #                     help="Override value of Bcc: header (may specify more than once)")

        subject: Annotated[
            str,
            typer.Option('--subject', '-S',
                         help="Override value of Subject: header (i.e. value after prefix)")] = None,
        command: Annotated[
            str,
            typer.Argument(help="Command which should be ran, and result of which will be emailed")] = ...,
        keep_exit_code: Annotated[
            bool,
            typer.Option('--keep-exit-code',
                         help="Exit with same return code as subprocess.  If "
                         "this is not specified, `run-n-mail` will normally "
                         "exit with code 0 regardless of what happens with "
                         "the subprocess.")] = False,
):
    """
    Run a command as subprocess, and email the result/output
    """
    config = ctx.parent.rattail_config
    app = config.get_app()

    cmd = config.parse_list(command)
    log.info("will run command as subprocess: %s", cmd)
    run_began = app.make_utc()

    try:
        # TODO: must we allow for shell=True in some situations? (clearly not yet)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        retcode = 0
        log.info("command completed successfully")
    except subprocess.CalledProcessError as error:
        output = error.output
        retcode = error.returncode
        log.warning("command exited with code: %s", retcode)

    output = output.decode(errors='replace')

    run_ended = app.make_utc()
    runtime = run_ended - run_began
    runtime_pretty = humanize.naturaldelta(runtime)

    if skip_if_empty and not output:
        log.info("command had no output, so will skip sending email")
        # return

    else: # send email
        kwargs = {}
        if subject:
            kwargs['subject_template'] = subject
        app.send_email(key, {
            'cmd': cmd,
            'run_began': run_began,
            'run_ended': run_ended,
            'runtime': runtime,
            'runtime_pretty': runtime_pretty,
            'retcode': retcode,
            'output': output,
        }, **kwargs)

    if retcode and keep_exit_code:
        sys.exit(retcode)
