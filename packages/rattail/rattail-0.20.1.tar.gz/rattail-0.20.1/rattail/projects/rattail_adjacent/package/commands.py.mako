## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} commands
"""

import typer

from rattail.commands.typer import make_typer
from rattail.commands.util import rprint

from ${pkg_name} import __version__


${pkg_name}_typer = make_typer(
    name='${pkg_name}',
    help="${name} -- ${description}"
)


@${pkg_name}_typer.command()
def hello(
        ctx: typer.Context,
):
    """
    The requisite 'hello world' example
    """
    rprint("\n\t[blue]Welcome to ${name} {}![/blue]\n".format(__version__))


@${pkg_name}_typer.command()
def install(
        ctx: typer.Context,
):
    """
    Install the ${name} app
    """
    from rattail.install import InstallHandler

    config = ctx.parent.rattail_config
    handler = InstallHandler(config,
                             app_title="${name}",
                             app_package='${pkg_name}',
                             app_eggname='${egg_name}',
                             app_pypiname='${pypi_name}')
    handler.run()
