#!/bin/sh -e

# NOTE: this script is meant be ran by the 'rattail' user!

if [ "$1" = "--verbose" ]; then
    VERBOSE='--verbose'
    QUIET=
else
    VERBOSE=
    QUIET='--quiet'
fi

SRC=/srv/envs/${env_name}/src
PIP=/srv/envs/${env_name}/bin/pip
export PIP_CONFIG_FILE=/srv/envs/${env_name}/pip.conf

# upgrade pip
$PIP install $QUIET --disable-pip-version-check --upgrade pip
# $PIP install $QUIET --upgrade --upgrade-strategy eager setuptools wheel ndg-httpsclient

# upgrade app software...

# how you need to upgrade your app will depend on whether you are running any
# packages "from source" as opposed to only using built/released packages

# if running ${name} from source, you should first fetch/install latest code:
#cd $SRC/${folder}
#git pull $QUIET
#find . -name '*.pyc' -delete
#$PIP install $QUIET --editable .

# in any case the last step is always the same.  note that this will ensure the
# "latest" ${name} is used, but also will upgrade any dependencies
$PIP install $QUIET --upgrade --upgrade-strategy eager '${pypi_name}'

# migrate database schema
cd /srv/envs/${env_name}
bin/alembic --config app/rattail.conf upgrade heads
