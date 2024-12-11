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
    settings.setdefault('mako.directories', ['${pkg_name}.web:templates',
                                             'tailbone:templates'])

    # make config objects
    rattail_config = app.make_rattail_config(settings)
    pyramid_config = app.make_pyramid_config(settings)

    # maybe configure integration db connections
    % if integrates_catapult:
    from tailbone_onager.db import CatapultSession
    CatapultSession.configure(bind=rattail_config.catapult_engine)
    % elif integrates_locsms:
    from tailbone_locsms.db import SmsSession
    SmsSession.configure(bind=rattail_config.locsms_engine)
    % endif

    # bring in the rest of ${name}
    pyramid_config.include('${pkg_name}.web.static')
    pyramid_config.include('${pkg_name}.web.subscribers')
    pyramid_config.include('${pkg_name}.web.views')

    return pyramid_config.make_wsgi_app()
