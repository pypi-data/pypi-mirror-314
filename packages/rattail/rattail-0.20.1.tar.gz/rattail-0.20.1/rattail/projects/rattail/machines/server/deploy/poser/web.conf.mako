## -*- mode: conf; -*-
<%text>##</%text> -*- mode: conf; -*-

<%text>${'#'}###########################################################</%text>
#
# config for ${name} web app
#
<%text>${'#'}###########################################################</%text>


<%text>${'#'}#############################</%text>
# rattail
<%text>${'#'}#############################</%text>

[rattail.config]
include = %(here)s/rattail.conf


<%text>${'#'}#############################</%text>
# pyramid
<%text>${'#'}#############################</%text>

[app:main]
use = egg:${egg_name}

pyramid.reload_templates = false
pyramid.debug_all = false
pyramid.default_locale_name = en
pyramid.includes = pyramid_exclog

beaker.session.type = file
beaker.session.data_dir = %(here)s/sessions/data
beaker.session.lock_dir = %(here)s/sessions/lock
beaker.session.secret = <%text>${env.tailbone_beaker_secret}</%text>
beaker.session.key = ${folder}

pyramid_deform.tempdir = %(here)s/data/uploads

exclog.extra_info = true

# required for tailbone
rattail.config = %(__file__)s

[server:main]
use = egg:waitress#main
# TODO: should ideally use 127.0.0.1 as host address, e.g. with reverse proxy
host = 0.0.0.0
port = 9761

# NOTE: this is needed for local reverse proxy stuff to work with HTTPS
# https://docs.pylonsproject.org/projects/waitress/en/latest/reverse-proxy.html
# https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html
# trusted_proxy = 127.0.0.1

# TODO: leave this empty if proxy serves as root site, e.g. http://rattail.example.com/
# url_prefix =

# TODO: or, if proxy serves as subpath of root site, e.g. http://rattail.example.com/backend/
# url_prefix = /backend


<%text>${'#'}#############################</%text>
# logging
<%text>${'#'}#############################</%text>

[logger_root]
handlers = file, console

[handler_console]
level = INFO

[handler_file]
args = ('/srv/envs/${env_name}/app/log/web.log', 'a', 'utf_8')
