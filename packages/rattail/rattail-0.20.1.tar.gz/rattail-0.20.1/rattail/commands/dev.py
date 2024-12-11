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
Development Commands
"""

import os
import re
from pathlib import Path

import typer
from typing_extensions import Annotated
from mako.template import Template

from rattail.commands.typer import typer_callback
from rattail.files import resource_path


rattail_dev_typer = typer.Typer(
    callback=typer_callback,
    help="Rattail - development commands"
)


@rattail_dev_typer.command()
def new_batch(
        ctx: typer.Context,
        model: Annotated[
            str,
            typer.Argument(help="Name of primary model for new batch, e.g. "
                           "'VendorCatalog' or 'PrintLabels'.")],
        output_dir: Annotated[
            Path,
            typer.Option('--output-dir', '-O',
                         help="Path to which generated files should be written; "
                         "defaults to current directory.")] = '.',
):
    """
    Generate some code for a new batch type.
    """
    model_title = re.sub(r'([a-z])([A-Z])', r'\g<1> \g<2>', model)
    table_name = model_title.lower().replace(' ', '_')
    context = {
        'model_name': model,
        'model_title': model_title,
        'table_name': table_name,
    }
    template_dir = resource_path('rattail:data/new-batch')
    for name in ('model', 'handler', 'webview'):
        template_path = os.path.join(template_dir, f'{name}.py')
        template = Template(filename=template_path)
        output_path = os.path.join(output_dir, f'{name}.py')
        with open(output_path, 'wt') as output_file:
            output_file.write(template.render(**context))
