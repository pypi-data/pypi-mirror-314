## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} config extensions
"""

from rattail.config import ConfigExtension


class ${studly_prefix}Config(ConfigExtension):
    """
    Rattail config extension for ${name}
    """
    key = '${pkg_name}'

    def configure(self, config):

        # app info
        config.setdefault('rattail.app_title', "${name.replace('"', '\\"')}")
        config.setdefault('rattail.app_dist', "${pypi_name}")

        % if has_model:
        # primary data model
        config.setdefault('rattail.model', '${pkg_name}.db.model')
        % endif

        # custom menu for web app
        #config.setdefault('tailbone.menus.handler', '${pkg_name}.web.menus:${studly_prefix}MenuHandler')

        # web app libcache
        #config.setdefault('tailbone.static_libcache.module', '${pkg_name}.web.static')
