## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Rattail -> Rattail "versions" data import
"""

from rattail.importing import versions as base
from ${pkg_name}.db.model import ${integration_studly_prefix}ProductCache


class ${integration_studly_prefix}VersionMixin(object):
    """
    Add default registration of custom importers
    """

    def add_${integration_pkgname}_importers(self, importers):
        importers['${integration_studly_prefix}ProductCache'] = ${integration_studly_prefix}ProductCacheImporter
        return importers


class ${integration_studly_prefix}ProductCacheImporter(base.VersionImporter):
    host_model_class = ${integration_studly_prefix}ProductCache
