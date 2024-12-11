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
Commands to manage settings
"""

import logging
import sys

import typer
from typing_extensions import Annotated

from .base import rattail_typer


log = logging.getLogger(__name__)


@rattail_typer.command()
def config_setting(
        ctx: typer.Context,
        section: Annotated[
            str,
            typer.Option(help="Section name for the config setting.")] = None,
        option: Annotated[
            str,
            typer.Option(help="Option name for the config setting.")] = None,
        name: Annotated[
            str,
            typer.Option(help="Name of the config setting to get.  "
                         "This may be used instead of --section and --option.")] = None,
        usedb: Annotated[
            bool,
            typer.Option('--usedb',
                         help="Look for values in the DB (settings table).")] = False,
        no_usedb: Annotated[
            bool,
            typer.Option('--no-usedb',
                         help="Do not look for values in the DB (settings table).")] = False,
        preferdb: Annotated[
            bool,
            typer.Option('--preferdb',
                         help="Prefer values from DB over those from config file.")] = False,
        no_preferdb: Annotated[
            bool,
            typer.Option('--no-preferdb',
                         help="Prefer values from config file over those from DB.")] = False,
):
    """
    Get a value from config file and/or settings table
    """
    config = ctx.parent.rattail_config

    # nb. we still may be using legacy config object, so must
    # convert name to (section, option) if applicable
    if section and option:
        section = section
        option = option
    elif name:
        section, option = legacy_split_setting(name)

    usedb = None
    if usedb:
        usedb = True
    elif no_usedb:
        usedb = False

    preferdb = None
    if preferdb:
        preferdb = True
    elif no_preferdb:
        preferdb = False

    value = config.get(section, option, usedb=usedb, preferdb=preferdb)
    if value is not None:
        sys.stdout.write(f"{value}\n")


@rattail_typer.command()
def setting_get(
        ctx: typer.Context,
        name: Annotated[
            str,
            typer.Argument(help="Name of the setting to retrieve.")] = ...,
):
    """
    Get a setting value from the DB
    """
    config = ctx.parent.rattail_config
    app = config.get_app()
    session = app.make_session()
    value = app.get_setting(session, name)
    session.commit()
    session.close()
    sys.stdout.write(value or '')


@rattail_typer.command()
def setting_put(
        ctx: typer.Context,
        name: Annotated[
            str,
            typer.Argument(help="Name of the setting to save.")] = ...,
        value: Annotated[
            str,
            typer.Argument(help="String value for the setting.")] = ...,
):
    """
    Add or update a setting in the DB
    """
    config = ctx.parent.rattail_config
    app = config.get_app()
    session = app.make_session()
    app.save_setting(session, name, value)
    session.commit()
    session.close()


def legacy_split_setting(name):
    """
    Split a new-style setting ``name`` into a legacy 2-tuple of
    ``(section, option)``.
    """
    parts = name.split('.')
    if len(parts) > 2:
        log.debug("ambiguous legacy split for setting name: %s", name)
    return parts[0], '.'.join(parts[1:])
