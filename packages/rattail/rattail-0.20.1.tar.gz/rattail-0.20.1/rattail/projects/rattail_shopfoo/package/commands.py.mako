## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Rattail/${integration_name} commands
"""

from rattail.commands import rattail_typer
from rattail.commands.typer import file_exporter_command, typer_get_runas_user


@rattail_typer.command()
@file_exporter_command
def export_${integration_pkgname}(
        ctx: typer.Context,
        **kwargs
):
    """
    Export data to ${integration_name}
    """
    config = ctx.parent.rattail_config
    progress = ctx.parent.rattail_progress
    handler = ImportCommandHandler(
        config, import_handler_spec='${pkg_name}.${integration_pkgname}.importing.rattail:FromRattailTo${integration_studly_prefix}')
    kwargs['user'] = typer_get_runas_user(ctx)
    handler.run(kwargs, progress=progress)
