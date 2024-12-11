## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Fabric script for a server running Theo, the order system

Please see the accompanying README for full instructions.
"""

from fabric2 import task

from rattail.core import Object
from rattail_fabric2 import apt, postfix, postgresql, exists, make_system_user, mkdir

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
    bootstrap_theo(c)
    bootstrap_theo_stage(c)


@task
def bootstrap_base(c):
    """
    Bootstrap the base system
    """
    # this does `apt update && apt dist-upgrade` every time the task runs.
    # comment out if you don't want that to happen.
    apt.dist_upgrade(c)

    # mail
    # we use postfix by default.  while the basic config "works" any mail sent
    # may be considered spam by various email providers.  please add your own
    # configuration here; cf. the `rattail_fabric2.postfix` module
    postfix.install(c)

    # rattail user + common config
    make_system_user(c, 'rattail', home='/var/lib/rattail', shell='/bin/bash')
    postfix.alias(c, 'rattail', 'root')
    mkdir(c, '/etc/rattail', use_sudo=True)
    deploy(c, 'rattail/rattail.conf.mako', '/etc/rattail/rattail.conf',
           use_sudo=True, context={'env': env})

    # postgresql
    apt.install(c, 'postgresql')
    postgresql.create_user(c, 'rattail', password=env.password_postgresql_rattail)

    # python
    mkdir(c, '/srv/envs', use_sudo=True, owner='rattail:')
    apt.install(
        c,
        'build-essential',
        'git',
        'libpq-dev',
        'python3-dev',
        'python3-venv',
        'supervisor',
    )

    ## catapult extras
    % if integrates_with == 'catapult':
    # freetds / odbc
    apt.install(c, 'unixodbc', 'unixodbc-dev')
    # we must install FreeTDS from source, b/c the version APT makes available
    # is too old.  however the *latest* source seems to have some issue(s)
    # which cause it to use too much memory, so we use a more stable branch
    from rattail_fabric2 import freetds
    freetds.install_from_source(c, user='rattail', branch='Branch-1_2')
    deploy(c, 'rattail/freetds.conf.mako', '/usr/local/etc/freetds.conf',
           use_sudo=True, context={'env': env})
    deploy(c, 'rattail/odbc.ini', '/etc/odbc.ini', use_sudo=True)
    % endif

    # uncomment this if you prefer to use emacs
    #apt.install_emacs(c)


@task
def bootstrap_theo(c):
    """
    Bootstrap Theo, the order system
    """
    install_theo_app(c, 'theo', True, 7000)


@task
def bootstrap_theo_stage(c):
    """
    Bootstrap "stage" for Theo, the order system
    """
    install_theo_app(c, 'theo-stage', False, 7010, from_source=True)


<%text>##############################</%text>
# support functions
<%text>##############################</%text>

def install_theo_app(c, envname, production, port, from_source=False):
    """
    Install a Theo app, per the given parameters
    """
    dbname = envname
    safename = envname.replace('-', '_')
    envroot = '/srv/envs/{}'.format(envname)

    c.sudo('supervisorctl stop {}:'.format(safename), warn=True)

    # virtualenv
    if not exists(c, envroot):
        c.sudo('python3 -m venv {}'.format(envroot), user='rattail')
        c.sudo('{}/bin/pip install --upgrade pip wheel'.format(envroot), user='rattail')
    deploy(c, 'python/pip.conf.mako', '{}/pip.conf'.format(envroot),
           use_sudo=True, owner='rattail:', mode='0600',
           context={'env': env, 'envroot': envroot})

    # theo
    if from_source:
        install_theo_source(c, envroot)
    else:
        % if integrates_with == 'catapult':
        pkgname = 'tailbone-theo[catapult]'
        % elif integrates_with == 'corepos':
        pkgname = 'tailbone-theo[corepos]'
        % else:
        pkgname = 'tailbone-theo'
        % endif
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install {1}'".format(envroot, pkgname),
               user='rattail')

    # app dir
    if not exists(c, '{}/app'.format(envroot)):
        c.sudo("bash -c 'cd {} && bin/rattail make-appdir'".format(envroot),
               user='rattail')
    c.sudo('chmod 0750 {}/app/log'.format(envroot))

    # config
    deploy(c, 'theo-common/rattail.conf.mako', '{}/app/rattail.conf'.format(envroot),
           use_sudo=True, owner='rattail:', mode='0600',
           context={'env': env, 'envroot': envroot, 'dbname': dbname, 'production': production})
    if not exists(c, '{}/app/quiet.conf'.format(envroot)):
        c.sudo("bash -c 'cd {} && bin/rattail make-config -T quiet -O app/'".format(envroot),
               user='rattail')
    deploy(c, 'theo-common/web.conf.mako', '{}/app/web.conf'.format(envroot),
           use_sudo=True, owner='rattail:', mode='0600',
           context={'env': env, 'envroot': envroot, 'dbname': dbname, 'port': port})

    # scripts
    deploy(c, 'theo-common/upgrade.sh.mako', '{}/app/upgrade.sh'.format(envroot),
           use_sudo=True, owner='rattail:', mode='0755',
           context={'envroot': envroot, 'production': production})
    deploy(c, 'theo-common/tasks.py.mako', '{}/app/tasks.py'.format(envroot),
           use_sudo=True, owner='rattail:',
           context={'envroot': envroot})
    deploy(c, 'theo-common/upgrade-wrapper.sh.mako', '{}/app/upgrade-wrapper.sh'.format(envroot),
           use_sudo=True, owner='rattail:', mode='0755',
           context={'envroot': envroot, 'safename': safename})

    # # TODO
    # deploy(c, 'theo/cron.conf', '/srv/envs/theo/app/cron.conf', use_sudo=True)
    # # deploy(c, 'theo/overnight.sh', '/srv/envs/theo/app/overnight.sh',
    # #        use_sudo=True)

    # theo db
    if not postgresql.db_exists(c, dbname):
        postgresql.create_db(c, dbname, owner='rattail', checkfirst=False)
        c.sudo("bash -c 'cd {} && bin/alembic -c app/rattail.conf upgrade heads'".format(envroot),
               user='rattail')
        postgresql.sql(c, "insert into setting values ('tailbone.theme', 'falafel')",
                       database=dbname)
        postgresql.sql(c, "insert into setting values ('tailbone.themes.expose_picker', 'false')",
                       database=dbname)
        postgresql.sql(c, "insert into setting values ('tailbone.global_help_url', 'https://rattailproject.org/moin/Documentation')",
                       database=dbname)
        c.sudo("bash -c 'cd {} && bin/rattail -c app/quiet.conf make-user --admin {} --password {}'".format(
            envroot, env.theo_admin_username, env.theo_admin_password),
               user='rattail', echo=False)

    # supervisor
    deploy(c, 'theo-common/supervisor.conf.mako', '/etc/supervisor/conf.d/{}.conf'.format(safename),
           use_sudo=True, context={'envroot': envroot, 'safename': safename})
    c.sudo('supervisorctl update')
    c.sudo('supervisorctl start {}:'.format(safename))

    # cron, sudo etc.
    deploy.sudoers(c, 'theo-common/sudoers.mako', '/etc/sudoers.d/{}'.format(safename),
                   context={'envroot': envroot})

    # # TODO
    # # deploy(c, 'theo/crontab', '/etc/cron.d/theo', use_sudo=True)
    # deploy(c, 'theo/logrotate.conf', '/etc/logrotate.d/theo', use_sudo=True)


def install_theo_source(c, envroot):
    """
    Install source code for Theo
    """
    # rattail
    if not exists(c, '{}/src/rattail'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/rattail.git {envroot}/src/rattail',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/rattail'".format(envroot),
               user='rattail')

    # tailbone
    if not exists(c, '{}/src/tailbone'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/tailbone.git {envroot}/src/tailbone',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/tailbone'".format(envroot),
               user='rattail')

    ## begin catapult
    % if integrates_with == 'catapult':

    # onager
    if not exists(c, '{}/src/onager'.format(envroot)):
        c.sudo(f'git clone https://{env.forgejo_username}:{env.forgejo_password}@forgejo.wuttaproject.org/rattail/onager.git {envroot}/src/onager',
               user='rattail', echo=False)
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/onager'".format(envroot),
               user='rattail')

    # rattail-onager
    if not exists(c, '{}/src/rattail-onager'.format(envroot)):
        c.sudo(f'git clone https://{env.forgejo_username}:{env.forgejo_password}@forgejo.wuttaproject.org/rattail/rattail-onager.git {envroot}/src/rattail-onager',
               user='rattail', echo=False)
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/rattail-onager'".format(envroot),
               user='rattail')

    # tailbone-onager
    if not exists(c, '{}/src/tailbone-onager'.format(envroot)):
        c.sudo(f'git clone https://{env.forgejo_username}:{env.forgejo_password}@forgejo.wuttaproject.org/rattail/tailbone-onager.git {envroot}/src/tailbone-onager',
               user='rattail', echo=False)
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/tailbone-onager'".format(envroot),
               user='rattail')

    ## end catapult
    % endif

    ## begin corepos
    % if integrates_with == 'corepos':

    # pycorepos
    if not exists(c, '{}/src/pycorepos'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/pycorepos.git {envroot}/src/pycorepos',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/pycorepos'".format(envroot),
               user='rattail')

    # rattail-corepos
    if not exists(c, '{}/src/rattail-corepos'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/rattail-corepos.git {envroot}/src/rattail-corepos',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/rattail-corepos'".format(envroot),
               user='rattail')

    # tailbone-corepos
    if not exists(c, '{}/src/tailbone-corepos'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/tailbone-corepos.git {envroot}/src/tailbone-corepos',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/tailbone-corepos'".format(envroot),
               user='rattail')

    ## end corepos
    % endif

    # theo
    if not exists(c, '{}/src/theo'.format(envroot)):
        c.sudo(f'git clone https://forgejo.wuttaproject.org/rattail/theo.git {envroot}/src/theo',
               user='rattail')
        c.sudo("bash -c 'PIP_CONFIG_FILE={0}/pip.conf cd {0} && bin/pip install -e src/theo'".format(envroot),
               user='rattail')


<%text>##############################</%text>
# fabenv
<%text>##############################</%text>

try:
    import fabenv
except ImportError as error:
    print("\ncouldn't import fabenv: {}".format(error))

env.setdefault('machine_is_live', False)
