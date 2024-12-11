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
``rattail make-config`` command
"""

import os
import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from .base import rattail_typer


@rattail_typer.command()
def make_config(
        ctx: typer.Context,
        list_types: Annotated[
            bool,
            typer.Option('--list-types', '-l',
                         help="List the types of config files this tool can generate.")] = False,
        config_type: Annotated[
            str,
            typer.Option('--type', '-T',
                         help="Type of config file to create; defaults to 'rattail' "
                         "which will generate 'rattail.conf'")] = 'rattail',
        output: Annotated[
            Path,
            typer.Option('--output', '-O',
                         help="Path where the config file is to be generated.  This can "
                         "be the full path including filename, or just the folder, in which "
                         "case the filename is inferred from 'type'.  Default is to current "
                         "working folder.")] = '.',
):
    """
    Generate stub config file(s) where you want them
    """
    config = ctx.parent.rattail_config
    app = config.get_app()

    if list_types:
        list_config_types(config)
        return

    template_path = app.find_config_template(config_type)
    if not template_path:
        sys.stderr.write(f"config template not found for type: {config_type}\n")
        sys.exit(1)

    output_path = os.path.abspath(output)
    if os.path.isdir(output_path):
        output_path = os.path.join(output_path, f'{config_type}.conf'.format(config_type))
    if os.path.exists(output_path):
        sys.stderr.write(f"ERROR! output file already exists: {output_path}\n")
        sys.exit(2)

    config_path = app.make_config_file(config_type, output_path,
                                       template_path=template_path)
    sys.stdout.write(f"Config file generated at: {config_path}\n")


def list_config_types(config):
    app = config.get_app()
    templates = app.get_all_config_templates()
    sys.stdout.write("CONFIG TEMPLATES:\n")
    sys.stdout.write("=========================\n")
    for name, path in templates.items():
        sys.stdout.write("{:25s} {}\n".format(name, path))
    sys.stdout.write("=========================\n")
