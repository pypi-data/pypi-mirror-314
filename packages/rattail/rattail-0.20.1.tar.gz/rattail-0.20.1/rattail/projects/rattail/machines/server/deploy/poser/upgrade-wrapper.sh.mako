#!/bin/sh -e

if [ "$1" = "--verbose" ]; then
    VERBOSE='--verbose'
    INVOKE_ARGS='--echo'
else
    VERBOSE=
    INVOKE_ARGS=
fi

cd /srv/envs/${env_name}

INVOKE="sudo -H -u rattail bin/invoke --collection=app/tasks $INVOKE_ARGS"

# run upgrade task, as rattail user
$INVOKE upgrade

# restart web app
sh -c 'sleep 10; supervisorctl restart ${pkg_name}:${pkg_name}_webmain' &
