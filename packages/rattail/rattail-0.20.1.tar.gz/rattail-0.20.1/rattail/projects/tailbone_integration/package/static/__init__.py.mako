## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Static assets for ${name}
"""


def includeme(config):
    config.add_static_view('${pkg_name}', '${pkg_name}:static',
                           cache_max_age=3600)
