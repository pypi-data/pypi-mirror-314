## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Fabric script for a generic server

Please see the accompanying README for full instructions.
"""

from fabric2 import task

from rattail.core import Object
from rattail_fabric2 import apt, postfix #, exists, make_system_user, mkdir

from ${pkg_name} import make_deploy


env = Object()
deploy = make_deploy(__file__)


<%text>##############################</%text>
# bootstrap
<%text>##############################</%text>

@task
def bootstrap_all(c):
    """
    Bootstrap all aspects of the machine
    """
    bootstrap_base(c)
    bootstrap_other(c)


@task
def bootstrap_base(c):
    """
    Bootstrap the base system
    """
    apt.dist_upgrade(c)

    # postfix
    postfix.install(c)

    # uncomment this if you prefer to use emacs
    #apt.install_emacs(c)


@task
def bootstrap_other(c):
    """
    Bootstrap some other thing
    """
    c.run("echo 'other thing is bootstrapped'")


<%text>##############################</%text>
# fabenv
<%text>##############################</%text>

try:
    import fabenv
except ImportError as error:
    print("\ncouldn't import fabenv: {}".format(error))

env.setdefault('machine_is_live', False)
