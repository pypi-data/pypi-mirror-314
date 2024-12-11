#!/bin/sh -e

# NOTE: this script is meant to be ran by the 'rattail' user!

if [ "$1" = "--verbose" ]; then
    VERBOSE='--verbose'
    QUIET=
else
    VERBOSE=
    QUIET='--quiet'
fi

<%text>% if not production:</%text>
SRC=<%text>${envroot}</%text>/src
<%text>% endif</%text>
PIP=<%text>${envroot}</%text>/bin/pip
export PIP_CONFIG_FILE=<%text>${envroot}</%text>/pip.conf

# upgrade pip
$PIP install $QUIET --disable-pip-version-check --upgrade pip wheel

<%text>% if not production:</%text>
# now we fetch latest source code and install any "new" dependencies...

# rattail
cd $SRC/rattail
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

# tailbone
cd $SRC/tailbone
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

## begin catapult
% if integrates_with == 'catapult':

# onager
cd $SRC/onager
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

# rattail-onager
cd $SRC/rattail-onager
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

# tailbone-onager
cd $SRC/tailbone-onager
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

## end catapult
% endif

## begin corepos
% if integrates_with == 'corepos':

# pycorepos
cd $SRC/pycorepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

# rattail-corepos
cd $SRC/rattail-corepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

# tailbone-corepos
cd $SRC/tailbone-corepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

## end corepos
% endif

# theo
cd $SRC/theo
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

## end !production
<%text>% endif</%text>

# now upgrade *all* dependencies
% if integrates_with == 'catapult':
$PIP install $QUIET --upgrade --upgrade-strategy eager tailbone-theo[catapult]
% elif integrates_with == 'corepos':
$PIP install $QUIET --upgrade --upgrade-strategy eager tailbone-theo[corepos]
% else:
$PIP install $QUIET --upgrade --upgrade-strategy eager tailbone-theo
% endif

# migrate database schema
cd <%text>${envroot}</%text>
bin/alembic --config app/rattail.conf upgrade heads
