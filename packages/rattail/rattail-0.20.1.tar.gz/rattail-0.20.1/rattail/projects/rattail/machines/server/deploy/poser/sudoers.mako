# -*- mode: conf; -*-

# let rattail upgrade the app
rattail ALL = NOPASSWD: /srv/envs/${env_name}/app/upgrade-wrapper.sh
rattail ALL = NOPASSWD: /srv/envs/${env_name}/app/upgrade-wrapper.sh --verbose
