## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# cron config for ${name}
#
<%text>############################################################</%text>


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail.config]
include = %(here)s/rattail.conf


<%text>##############################</%text>
# alembic
<%text>##############################</%text>

[alembic]
script_location = ${alembic_script_location}
version_locations = ${alembic_version_locations}


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[handler_console]
level = WARNING

[handler_file]
args = ('/srv/envs/${env_name}/app/log/cron.log', 'a', 'utf_8')
