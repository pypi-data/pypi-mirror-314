## -*- mode: conf; -*-

/srv/envs/${env_name}/pip.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 rattail rattail
}

/srv/envs/${env_name}/app/log/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 rattail rattail
}
