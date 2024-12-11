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
Telemetry Commands
"""

import logging
import pprint

import typer
from typing_extensions import Annotated

from .base import rattail_typer


log = logging.getLogger(__name__)


@rattail_typer.command()
def telemetry(
        ctx: typer.Context,
        profile: Annotated[
            str,
            typer.Option('--profile', '-p',
                         help="Profile (type) of telemetry data to collect.  "
                         "This also determines where/how data is submitted.  "
                         "If not specified, default logic is assumed.")] = None,
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run',
                         help="Go through all the motions but do not submit "
                         "the data to server.")] = False,
):
    """
    Submit telemetry data to a server
    """
    config = ctx.parent.rattail_config
    do_telemetry(config, profile, dry_run=dry_run, verbose=ctx.parent.params['verbose'])


def do_telemetry(config, profile, dry_run=False, verbose=False):
    app = config.get_app()
    telemetry = app.get_telemetry_handler()

    data = telemetry.collect_all_data(profile=profile)
    log.info("data collected okay: %s", ', '.join(sorted(data)))
    log.debug("%s", data)

    if verbose:
        print("COLLECTED DATA:")
        pprint.pprint(data)

    if dry_run:
        log.info("dry run, so will not submit data to server")
    else:
        telemetry.submit_all_data(data, profile=profile)
        log.info("data submitted okay")
