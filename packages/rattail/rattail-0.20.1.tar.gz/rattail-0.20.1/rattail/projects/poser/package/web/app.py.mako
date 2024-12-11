## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} web app
"""

from tailbone import app


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # prefer ${name} templates over Tailbone
    settings.setdefault('mako.directories', [
        % for path in mako_directories:
        '${path}',
        % endfor
    ])

    # make config objects
    rattail_config = app.make_rattail_config(settings)
    pyramid_config = app.make_pyramid_config(settings)

    # bring in the rest of ${name}
    pyramid_config.include('${pkg_name}.web.static')
    pyramid_config.include('${pkg_name}.web.subscribers')
    pyramid_config.include('${pkg_name}.web.views')

    return pyramid_config.make_wsgi_app()


def asgi_main():
    """
    This function returns an ASGI application.
    """
    from tailbone.asgi import make_asgi_app

    return make_asgi_app(main)
