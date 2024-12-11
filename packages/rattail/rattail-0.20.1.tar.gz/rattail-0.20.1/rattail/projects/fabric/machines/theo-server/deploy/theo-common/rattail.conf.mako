## -*- mode: conf; -*-

<%text>${'#'}###########################################################</%text>
#
# core config for Theo
#
<%text>${'#'}###########################################################</%text>


[theo]
% if integrates_with == 'catapult':
integrate_catapult = true
% elif integrates_with == 'corepos':
integrate_corepos = true
% endif


## begin catapult
% if integrates_with == 'catapult':

<%text>${'#'}#############################</%text>
# Catapult
<%text>${'#'}#############################</%text>

[catapult.db]
default.url = catapult://<%text>${env.catapult_odbc_username}:${env.catapult_odbc_password}</%text>@catapult-default

## end catapult
% endif


## begin corepos
% if integrates_with == 'corepos':

<%text>${'#'}#############################</%text>
# CORE-POS
<%text>${'#'}#############################</%text>

[corepos]
office.url = <%text>${env.corepos_office_url}</%text>

[corepos.api]
url = <%text>${env.corepos_api_url}</%text>

[corepos.db.office_op]
default.url = mysql+mysqlconnector://<%text>${env.corepos_db_username}:${env.corepos_db_password}@${env.corepos_db_host}/${env.corepos_db_name_office_op}</%text>
default.pool_recycle = 3600

## end corepos
% endif


<%text>${'#'}#############################</%text>
# rattail
<%text>${'#'}#############################</%text>

[rattail]
production = <%text>${'true' if production else 'false'}</%text>
appdir = <%text>${envroot}</%text>/app
datadir = <%text>${envroot}</%text>/app/data
batch.files = <%text>${envroot}</%text>/app/batch
workdir = <%text>${envroot}</%text>/app/work

[rattail.config]
include = /etc/rattail/rattail.conf
usedb = true
preferdb = true

[rattail.db]
default.url = postgresql://rattail:<%text>${env.password_postgresql_rattail}@localhost/${dbname}</%text>
versioning.enabled = true

[rattail.mail]
send_emails = true
default.prefix = [Theo]

[rattail.upgrades]
command = sudo <%text>${envroot}</%text>/app/upgrade-wrapper.sh --verbose
files = <%text>${envroot}</%text>/app/data/upgrades


<%text>${'#'}#############################</%text>
# alembic
<%text>${'#'}#############################</%text>

[alembic]
script_location = rattail.db:alembic
% if integrates_with == 'catapult':
version_locations = rattail_onager.db:alembic/versions rattail.db:alembic/versions
% elif integrates_with == 'corepos':
version_locations = rattail_corepos.db:alembic/versions rattail.db:alembic/versions
% else:
version_locations = rattail.db:alembic/versions
% endif


<%text>${'#'}#############################</%text>
# logging
<%text>${'#'}#############################</%text>

[handler_file]
args = ('<%text>${envroot}</%text>/app/log/rattail.log', 'a', 'utf_8')

[handler_email]
args = ('localhost', '<%text>${env.email_default_sender}</%text>', <%text>${env.email_default_recipients}, "[Theo${'' if production else ' (stage)'}</%text>] Logging")
