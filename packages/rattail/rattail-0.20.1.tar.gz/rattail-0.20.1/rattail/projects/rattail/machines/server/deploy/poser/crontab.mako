## -*- mode: conf; -*-

<%text>${'#'}###########################################################</%text>
#
# crontab for ${name}
#
<%text>${'#'}###########################################################</%text>

MAILTO="root@localhost,fred@mailinator.com"

# overnight automation starts at 1:00am
<%text>${'' if env.machine_is_live else '#'}</%text>00 01 * * *  rattail  /srv/envs/${env_name}/app/overnight-wrapper.sh
