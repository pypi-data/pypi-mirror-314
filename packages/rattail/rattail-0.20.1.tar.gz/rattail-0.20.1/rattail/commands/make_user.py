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
``rattail make-user`` command
"""

import sys
from enum import Enum
from getpass import getpass

import typer
from typing_extensions import Annotated

from .base import rattail_typer


class UserSystem(str, Enum):
    rattail = 'rattail'
    windows = 'windows'


@rattail_typer.command()
def make_user(
        ctx: typer.Context,
        username: Annotated[
            str,
            typer.Argument(help="Username for the new user.")] = ...,
        system: Annotated[
            UserSystem,
            typer.Option(help="System in which to create the new user.")] = 'rattail',
        admin: Annotated[
            bool,
            typer.Option('--admin', '-A',
                         help="Whether the new user should have admin rights within "
                         "the system (if applicable).")] = False,
        password: Annotated[
            str,
            typer.Option(help="Password to set for the new user.  If not specified, "
                         "you may be prompted for one.")] = None,
        no_password: Annotated[
            bool,
            typer.Option('--no-password',
                         help="Do not ask for, or try to set, a password for the new user.")] = False,
        full_name: Annotated[
            str,
            typer.Option(help="Full (display) name for the new user (if applicable).")] = None,
        comment: Annotated[
            str,
            typer.Option(help="Comment string for the new user (if applicable).")] = None,
        groups: Annotated[
            str,
            typer.Option(help="Optional list (comma-separated string) of groups/roles "
                         "to which the new user should be assigned.")] = None,
):
    """
    Create a new user account in a given system
    """
    config = ctx.parent.rattail_config

    mkuser = None
    if system == 'rattail':
        mkuser = mkuser_rattail
    elif system == 'windows':
        mkuser = mkuser_windows

    if mkuser:
        if mkuser(config, ctx.params):
            sys.stdout.write(f"created new user in '{system}' system: {username}\n")
    else:
        sys.stderr.write(f"don't know how to make user for '{system}' system\n")
        sys.exit(1)


def mkuser_rattail(config, params):
    from sqlalchemy import orm

    app = config.get_app()
    auth = app.get_auth_handler()
    session = app.make_session()
    model = app.model

    if session.query(model.User).filter_by(username=params['username']).count():
        session.close()
        return user_exists(params)

    roles = []
    if params['groups']:
        for name in config.parse_list(params['groups']):
            try:
                role = session.query(model.Role)\
                              .filter(model.Role.name == name)\
                              .one()
            except orm.exc.NoResultFound:
                sys.stderr.write("Role not found: {}\n".format(name))
                session.close()
                sys.exit(4)
            else:
                roles.append(role)

    user = model.User(username=params['username'])
    if not params['no_password']:
        auth.set_user_password(user, obtain_password(params))

    if params['admin']:
        user.roles.append(auth.get_role_administrator(session))
    for role in roles:
        user.roles.append(role)

    if params['full_name']:
        kwargs = {'display_name': params['full_name']}
        words = params['full_name'].split()
        if len(words) == 2:
            kwargs.update({'first_name': words[0], 'last_name': words[1]})
        user.person = model.Person(**kwargs)

    session.add(user)
    session.commit()
    session.close()
    return True


def mkuser_windows(config, params, args):
    if sys.platform != 'win32':
        sys.stderr.write("sorry, only win32 platform is supported\n")
        sys.exit(1)

    from rattail.win32 import users
    from rattail.win32 import require_elevation

    if params['no_password']:
        sys.stderr.write("sorry, a password is required when making a 'win32' user\n")
        sys.exit(1)

    require_elevation()

    if users.user_exists(params['username']):
        return user_exists(params)

    return users.create_user(params['username'], obtain_password(params),
                             full_name=params['full_name'], comment=params['comment'])


def obtain_password(params):
    if params['password']:
        return params['password']
    try:
        password = None
        while not password:
            password = getpass(str("enter password for new user: ")).strip()
    except KeyboardInterrupt:
        sys.stderr.write("\noperation canceled by user\n")
        sys.exit(2)
    return password


def user_exists(params):
    sys.stdout.write(f"user already exists in '{params['system']}' system: {params['username']}\n")
    sys.exit(1)
