## -*- mode: conf; -*-

[group:${pkg_name}]
programs=${pkg_name}_webmain

[program:${pkg_name}_webmain]
command=/srv/envs/${env_name}/bin/pserve pastedeploy+ini:/srv/envs/${env_name}/app/web.conf
directory=/srv/envs/${env_name}/app/work
user=rattail
