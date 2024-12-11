## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Pyramid event subscribers
"""

import ${pkg_name}


def add_${pkg_name}_to_context(event):
    renderer_globals = event
    renderer_globals['${pkg_name}'] = ${pkg_name}


def includeme(config):
    config.include('tailbone.subscribers')
    config.add_subscriber(add_${pkg_name}_to_context, 'pyramid.events.BeforeRender')
