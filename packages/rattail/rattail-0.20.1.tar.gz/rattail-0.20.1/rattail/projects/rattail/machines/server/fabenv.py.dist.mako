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

# default sender and recipients for all emails
env.email_default_sender = 'rattail@example.com'
env.email_default_recipients = ['root@example.com']

# this is for the 'rattail' user within PostgreSQL, running on the server.
# this rattail user owns the '${db_name}' database and is used by the
# ${name} app to access the db
env.password_postgresql_rattail = 'password'

# this is the hostname for your Catapult WebOffice
env.catapult_host = 'INSTANCE.catapultweboffice.com'

# these credentials are used to access the ODBC DSN for ECRS Catapult
env.catapult_odbc_username = 'username'
env.catapult_odbc_password = 'password'

# this is used for protecting user session data for the web app, which lives in
# the server's file system.  should probably be at least 20 random characters
env.tailbone_beaker_secret = 'password'

# these credentials are used to access the "restricted" Rattail Project PyPI
env.restricted_pypi_username = 'username'
env.restricted_pypi_password = 'password'
