## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Rattail/${integration_name} model importers
"""

from rattail.importing.model import ToRattail
from ${pkg_name}.db import model


<%text>##############################</%text>
# custom models
<%text>##############################</%text>

class ${integration_studly_prefix}ProductCacheImporter(ToRattail):
    """
    Importer for ${integration_name} product cache
    """
    model_class = model.${integration_studly_prefix}ProductCache
