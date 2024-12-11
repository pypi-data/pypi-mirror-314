## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} config extensions
"""

from wuttjamaican.conf import WuttaConfigExtension


class ${studly_prefix}Config(WuttaConfigExtension):
    """
    Config extension for ${name}
    """
    key = '${pkg_name}'

    def configure(self, config):

        # app info
        config.setdefault(f'{config.appname}.app_title', "${name.replace('"', '\\"')}")
        config.setdefault(f'{config.appname}.app_dist', "${pypi_name}")

        # app model
        config.setdefault(f'{config.appname}.model_spec', '${pkg_name}.db.model')

        # web app menu
        config.setdefault(f'{config.appname}.web.menus.handler_spec',
                          '${pkg_name}.web.menus:${studly_prefix}MenuHandler')

        # web app libcache
        #config.setdefault('tailbone.static_libcache.module', '${pkg_name}.web.static')
