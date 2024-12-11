## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} web app
"""

from wuttaweb import app as base


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # prefer ${name} templates over wuttaweb
    settings.setdefault('mako.directories', [
        '${pkg_name}.web:templates',
        'wuttaweb:templates',
    ])

    # make config objects
    wutta_config = base.make_wutta_config(settings)
    pyramid_config = base.make_pyramid_config(settings)

    # bring in the rest of ${name}
    pyramid_config.include('${pkg_name}.web.static')
    pyramid_config.include('${pkg_name}.web.subscribers')
    pyramid_config.include('${pkg_name}.web.views')

    return pyramid_config.make_wsgi_app()
