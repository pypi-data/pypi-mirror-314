## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Fabric library for Python
"""

from rattail_fabric2 import python as base

from ${pkg_name}.fablib import make_deploy


deploy = make_deploy(__file__)


def bootstrap_python(c, workon_home='/srv/envs', user='rattail', **kwargs):
    """
    Bootstrap a "complete" Python install.
    """
    env = kwargs.pop('env')

    # first do normal bootstrapping
    kwargs['workon_home'] = workon_home
    kwargs['user'] = user
    base.bootstrap_python(c, **kwargs)

    # customize the `premkvirtualenv` hook
    deploy(c, 'python/premkvirtualenv.mako', '{}/premkvirtualenv'.format(workon_home),
           owner=user, mode='0700', use_sudo=True, context={'env': env})
