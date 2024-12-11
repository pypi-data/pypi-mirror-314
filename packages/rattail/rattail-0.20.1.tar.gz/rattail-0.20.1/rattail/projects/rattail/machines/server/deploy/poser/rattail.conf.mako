## -*- mode: conf; -*-
<%text>##</%text> -*- mode: conf; -*-

<%text>${'#'}###########################################################</%text>
#
# base config for ${name}
#
<%text>${'#'}###########################################################</%text>


% if integrates_catapult:
[catapult.db]
default.url = catapult://<%text>${env.catapult_odbc_username}:${env.catapult_odbc_password}</%text>@catapult-default
% endif


<%text>${'#'}#############################</%text>
# rattail
<%text>${'#'}#############################</%text>

[rattail]
production = <%text>${'true' if env.machine_is_live else 'false'}</%text>

# TODO: this will of course depend on your location
timezone.default = America/Chicago

# TODO: set this to a valid user within your DB
#runas.default = ${pkg_name}

appdir = /srv/envs/${env_name}/app
datadir = /srv/envs/${env_name}/app/data
workdir = /srv/envs/${env_name}/app/work
batch.files = /srv/envs/${env_name}/app/batch
export.files = /srv/envs/${env_name}/app/data/exports

[rattail.config]
#include = /etc/rattail/rattail.conf
configure_logging = true
usedb = true
preferdb = true

[rattail.db]
default.url = postgresql://rattail:<%text>${env.password_postgresql_rattail}</%text>@localhost/${db_name}
versioning.enabled = true

[rattail.mail]
# this is the master switch, *no* emails are sent if false
send_emails = true

smtp.server = localhost

templates =
    ${pkg_name}:templates/mail
    rattail:templates/mail

default.prefix = [${name}]
default.from = <%text>${env.email_default_sender}</%text>
default.to = <%text>${', '.join(env.email_default_recipients)}</%text>
#default.enabled = false

[rattail.upgrades]
command = sudo /srv/envs/${env_name}/app/upgrade-wrapper.sh --verbose
files = /srv/envs/${env_name}/app/data/upgrades


<%text>${'#'}#############################</%text>
# alembic
<%text>${'#'}#############################</%text>

[alembic]
script_location = ${alembic_script_location}
version_locations = ${alembic_version_locations}


<%text>${'#'}#############################</%text>
# logging
<%text>${'#'}#############################</%text>

[loggers]
keys = root, exc_logger, beaker, txn, sqlalchemy, django_db, flufl_bounce, requests

[handlers]
keys = file, console, email

[formatters]
keys = generic, console

[logger_root]
handlers = file, console, email
level = DEBUG

[logger_exc_logger]
qualname = exc_logger
handlers = email
level = ERROR

[logger_beaker]
qualname = beaker
handlers =
level = INFO

[logger_txn]
qualname = txn
handlers =
level = INFO

[logger_sqlalchemy]
qualname = sqlalchemy.engine
handlers =
# handlers = file
# level = INFO

[logger_django_db]
qualname = django.db.backends
handlers =
level = INFO
# level = DEBUG

[logger_flufl_bounce]
qualname = flufl.bounce
handlers =
level = WARNING

[logger_requests]
qualname = requests
handlers =
# level = WARNING

[handler_file]
class = handlers.WatchedFileHandler
args = ('/srv/envs/${env_name}/app/log/rattail.log', 'a', 'utf_8')
formatter = generic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
formatter = console
# formatter = generic
# level = INFO
# level = WARNING

[handler_email]
class = handlers.SMTPHandler
args = ('localhost', '<%text>${env.email_default_sender}</%text>', <%text>${env.email_default_recipients}</%text>, "[${name}] Logging")
formatter = generic
level = ERROR

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(funcName)s: %(message)s
datefmt = %Y-%m-%d %H:%M:%S

[formatter_console]
format = %(levelname)-5.5s [%(name)s] %(funcName)s: %(message)s
