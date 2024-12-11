## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Fabric script for 'server' machine

Please see the accompanying README for full instructions.
"""

from fabric2 import task

from rattail.core import Object
from rattail_fabric2 import apt, postfix, postgresql, python, exists, make_system_user, mkdir
% if integrates_catapult:
from rattail_fabric2 import freetds
% endif

from ${pkg_name}.fablib import make_deploy
from ${pkg_name}.fablib.python import bootstrap_python


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
    bootstrap_${pkg_name}(c)


@task
def bootstrap_base(c):
    """
    Bootstrap the base system
    """
    apt.dist_upgrade(c)

    # postfix
    postfix.install(c)

    # rattail user
    make_system_user(c, 'rattail', home='/var/lib/rattail', shell='/bin/bash')
    postfix.alias(c, 'rattail', 'root')

    # python
    bootstrap_python(c, user='rattail', env=env,
                     virtualenvwrapper_from_apt=True,
                     python3=True)

    # postgres
    apt.install(c, 'postgresql')
    postgresql.create_user(c, 'rattail', password=env.password_postgresql_rattail)

    % if integrates_catapult:
    # freetds / odbc
    apt.install(c, 'unixodbc', 'unixodbc-dev')
    # we must install FreeTDS from source, b/c the version APT makes available
    # is too old.  however the *latest* source seems to have some issue(s)
    # which cause it to use too much memory, so we use a more stable branch
    freetds.install_from_source(c, user='rattail', branch='Branch-1_2')
    deploy(c, '${folder}/freetds.conf.mako', '/usr/local/etc/freetds.conf',
           use_sudo=True, context={'env': env})
    deploy(c, '${folder}/odbc.ini', '/etc/odbc.ini', use_sudo=True)
    % endif

    # misc.
    apt.install(
        c,
        'git',
        'libpq-dev',
        'supervisor',
    )

    # uncomment this if you prefer to use emacs
    #apt.install_emacs(c)


@task
def bootstrap_${pkg_name}(c):
    """
    Bootstrap the ${name} app
    """
    user = 'rattail'

    c.sudo('supervisorctl stop ${pkg_name}:', warn=True)

    # virtualenv
    if not exists(c, '/srv/envs/${env_name}'):
        python.mkvirtualenv(c, '${env_name}', python='/usr/bin/python3', runas_user=user)
    c.sudo('chmod 0600 /srv/envs/${env_name}/pip.conf')
    mkdir(c, '/srv/envs/${env_name}/src', owner=user, use_sudo=True)

    # ${name}
    if env.machine_is_live:
        c.sudo("bash -lc 'workon ${env_name} && pip install ${pypi_name}'",
               user=user)
    else:
        # TODO: this really only works for vagrant
        c.sudo("bash -lc 'workon ${env_name} && pip install /vagrant/${pypi_name}-*.tar.gz'",
               user=user)

    # app dir
    if not exists(c, '/srv/envs/${env_name}/app'):
        c.sudo("bash -lc 'workon ${env_name} && cdvirtualenv && rattail make-appdir'", user=user)
    c.sudo('chmod 0750 /srv/envs/${env_name}/app/log')
    mkdir(c, '/srv/envs/${env_name}/app/data', use_sudo=True, owner=user)

    # config / scripts
    deploy(c, '${folder}/rattail.conf.mako', '/srv/envs/${env_name}/app/rattail.conf',
           owner=user, mode='0600', use_sudo=True, context={'env': env})
    if not exists(c, '/srv/envs/${env_name}/app/quiet.conf'):
        c.sudo("bash -lc 'workon ${env_name} && cdvirtualenv app && rattail make-config -T quiet'",
               user=user)
    deploy(c, '${folder}/cron.conf', '/srv/envs/${env_name}/app/cron.conf',
           owner=user, use_sudo=True)
    deploy(c, '${folder}/web.conf.mako', '/srv/envs/${env_name}/app/web.conf',
           owner=user, mode='0600', use_sudo=True, context={'env': env})
    deploy(c, '${folder}/upgrade.sh', '/srv/envs/${env_name}/app/upgrade.sh',
           owner=user, mode='0755', use_sudo=True)
    deploy(c, '${folder}/tasks.py', '/srv/envs/${env_name}/app/tasks.py',
           owner=user, use_sudo=True)
    deploy(c, '${folder}/upgrade-wrapper.sh', '/srv/envs/${env_name}/app/upgrade-wrapper.sh',
           owner=user, mode='0755', use_sudo=True)
    deploy(c, '${folder}/overnight.sh', '/srv/envs/${env_name}/app/overnight.sh',
           owner=user, mode='0755', use_sudo=True)
    deploy(c, '${folder}/overnight-wrapper.sh', '/srv/envs/${env_name}/app/overnight-wrapper.sh',
           owner=user, mode='0755', use_sudo=True)

    # database
    if not postgresql.db_exists(c, '${db_name}'):
        postgresql.create_db(c, '${db_name}', owner='rattail', checkfirst=False)
        c.sudo("bash -lc 'workon ${env_name} && cdvirtualenv && bin/alembic --config app/rattail.conf upgrade heads'",
               user=user)
        postgresql.sql(c, "insert into setting values ('rattail.app_title', '${name}')",
                       database='${db_name}')
        postgresql.sql(c, "insert into setting values ('tailbone.theme', 'falafel')",
                       database='${db_name}')
        postgresql.sql(c, "insert into setting values ('tailbone.themes.expose_picker', 'false')",
                       database='${db_name}')

    # supervisor
    deploy(c, '${folder}/supervisor.conf', '/etc/supervisor/conf.d/${pkg_name}.conf',
           use_sudo=True)
    c.sudo('supervisorctl update')
    c.sudo('supervisorctl start ${pkg_name}:')

    # cron etc.
    deploy.sudoers(c, '${folder}/sudoers', '/etc/sudoers.d/${pkg_name}')
    deploy(c, '${folder}/crontab.mako', '/etc/cron.d/${pkg_name}',
           use_sudo=True, context={'env': env})
    deploy(c, '${folder}/logrotate.conf', '/etc/logrotate.d/${pkg_name}',
           use_sudo=True)


<%text>##############################</%text>
# fabenv
<%text>##############################</%text>

try:
    import fabenv
except ImportError as error:
    print("\ncouldn't import fabenv: {}".format(error))

env.setdefault('machine_is_live', False)
