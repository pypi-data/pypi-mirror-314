#!/bin/sh -e
<%text>############################################################</%text>
#
# overnight automation for ${name}
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


<%text>##############################</%text>
# data sync
<%text>##############################</%text>

# import latest data from Catapult
$RATTAIL --runas catapult import-catapult --delete --warnings

# make sure version data is correct
$RATTAIL import-versions --delete --dry-run --warnings


<%text>##############################</%text>
# problem reports
<%text>##############################</%text>

$RATTAIL problems
