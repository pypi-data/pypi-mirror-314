## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8 -*-
"""
Views for ${integration_name} product exports
"""

from rattail_${integration_pkgname}.db.model import ${integration_studly_prefix}ProductExport

from tailbone.views.exports import ExportMasterView


class ${integration_studly_prefix}ProductExportView(ExportMasterView):
    """
    Master view for ${integration_name} product exports.
    """
    model_class = ${integration_studly_prefix}ProductExport
    route_prefix = '${integration_pkgname}.product_exports'
    url_prefix = '/${integration_pkgname}/exports/product'
    downloadable = True
    editable = True
    delete_export_files = True

    grid_columns = [
        'id',
        'created',
        'created_by',
        'record_count',
        'filename',
        'uploaded',
    ]

    form_fields = [
        'id',
        'created',
        'created_by',
        'record_count',
        'filename',
        'uploaded',
    ]


def defaults(config, **kwargs):
    base = globals()

    ${integration_studly_prefix}ProductExportView = kwargs.get('${integration_studly_prefix}ProductExportView', base['${integration_studly_prefix}ProductExportView'])
    ${integration_studly_prefix}ProductExportView.defaults(config)


def includeme(config):
    defaults(config)
