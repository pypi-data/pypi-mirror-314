#!/bin/sh -e
<%text>############################################################</%text>
#
# wrapper script for ${name} overnight automation
#
<%text>############################################################</%text>


if [ "$1" = "--verbose" ]; then
    VERBOSE='--verbose'
    PROGRESS='--progress'
else
    VERBOSE=
    PROGRESS=
fi

cd /srv/envs/${env_name}

RATTAIL="bin/rattail --config=app/cron.conf $PROGRESS"

$RATTAIL run-n-mail --no-versioning --skip-if-empty --subject 'Overnight automation' /srv/envs/${env_name}/app/overnight.sh
