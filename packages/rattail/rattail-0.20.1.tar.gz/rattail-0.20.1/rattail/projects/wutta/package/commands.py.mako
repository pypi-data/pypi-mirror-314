## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} commands
"""

import typer

from wuttjamaican.cli import make_typer


${pkg_name}_typer = make_typer(
    name='${pkg_name}',
    help="${name} -- ${description}"
)


@${pkg_name}_typer.command()
def install(
        ctx: typer.Context,
):
    """
    Install the ${name} app
    """
    config = ctx.parent.wutta_config
    app = config.get_app()
    install = app.get_install_handler(pkg_name='${pkg_name}',
                                      app_title="${name}",
                                      pypi_name='${pypi_name}',
                                      egg_name='${egg_name}')
    install.run()
