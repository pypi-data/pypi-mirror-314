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
#env.email_default_sender = 'rattail@example.com'
#env.email_default_recipients = ['root@example.com']

# this is for the 'rattail' user within PostgreSQL
#env.password_postgresql_rattail = 'password'
