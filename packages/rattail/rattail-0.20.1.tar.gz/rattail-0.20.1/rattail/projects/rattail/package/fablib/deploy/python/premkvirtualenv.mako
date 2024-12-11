#!/bin/bash
# This hook is run after a new virtualenv is created and before it is activated.

cat >$1/pip.conf <<EOF
[global]
extra-index-url =
    https://pypi.rattailproject.org/simple/
    % if integrates_catapult:
    https://<%text>${env.restricted_pypi_username}:${env.restricted_pypi_password}</%text>@pypi-restricted.rattailproject.org/catapult/
    % endif
log-file = $WORKON_HOME/$1/pip.log
exists-action = i
EOF

cat >$1/bin/postactivate <<EOF
export PIP_CONFIG_FILE=$WORKON_HOME/$1/pip.conf
EOF

cat >$1/bin/postdeactivate <<EOF
unset PIP_CONFIG_FILE
EOF
