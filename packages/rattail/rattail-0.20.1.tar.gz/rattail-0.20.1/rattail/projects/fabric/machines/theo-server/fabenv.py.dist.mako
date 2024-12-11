## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; mode: python; -*-
"""
Fabric environment tweaks
"""

from fabfile import env


<%text>##############################</%text>
# volatile
<%text>##############################</%text>

# this should be True only when targeting the truly *live* machine, but False
# otherwise, e.g. when building a new "live" machine, or using Vagrant
env.machine_is_live = False


<%text>##############################</%text>
# stable
<%text>##############################</%text>

# for a list of possible time zone values, see
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
env.timezone = 'America/Chicago'

# default sender and recipients for all emails
env.email_default_sender = 'rattail@localhost'
env.email_default_recipients = ['root@localhost']

# default admin user credentials for Theo web app
env.theo_admin_username = 'username'
env.theo_admin_password = 'password'

# this is for the 'rattail' user within PostgreSQL
env.password_postgresql_rattail = 'password'

# this is used to secure the user session and/or cookie for the web app
env.theo_beaker_secret = 'ABCDEFGHIJKLMNOPQRST'

# these credentials are used to access the Rattail Project source code
# on Forgejo.  they are only needed if you are integrating with a
# proprietary POS system, and running from source
env.forgejo_username = 'username'
env.forgejo_password = 'password'

# these credentials are used to access the "restricted" Rattail Project PyPI.
# they are only needed if you are integrating with a proprietary POS system,
# and installing released packages instead of running from source
env.restricted_pypi_username = 'username'
env.restricted_pypi_password = 'password'

## begin catapult
% if integrates_with == 'catapult':

<%text>##############################</%text>
# Catapult
<%text>##############################</%text>

# this is the hostname for your Catapult WebOffice
env.catapult_host = 'INSTANCE.catapultweboffice.com'

# these credentials are used to access the ODBC DSN for ECRS Catapult
env.catapult_odbc_username = 'username'
env.catapult_odbc_password = 'password'

## end catapult
% endif

## begin corepos
% if integrates_with == 'corepos':

<%text>##############################</%text>
# CORE-POS
<%text>##############################</%text>

# URL of your CORE Office (Fannie) website
env.corepos_office_url = 'http://localhost/'

# URL of your CORE Office API
env.corepos_api_url = 'http://localhost/ws/'

# MySQL info for CORE operational DB
env.corepos_db_host = 'localhost'
env.corepos_db_username = 'username'
env.corepos_db_password = 'password'
env.corepos_db_name_office_op = 'core_op'

## end corepos
% endif
