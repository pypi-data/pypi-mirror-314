
# Changelog
All notable changes to rattail will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.20.1 (2024-12-10)

### Fix

- use simple string instead of UUID for special role getters
- move some logic to avoid error when no sqlalchemy
- add custom `make_uuid()` function, app handler method
- add custom `uuid_column()` and `uuid_fk_column()` functions
- cleanup some code for wutta project template

## v0.20.0 (2024-11-24)

### Feat

- add project generator for 'wutta'

### Fix

- tweak generated output for new python/rattail projects
- avoid error in product autocomplete for duplicated key
- add problem report for duplicated product keys

## v0.19.2 (2024-11-18)

### Fix

- remove enum for sqlalchemy-continuum operation types
- define `str()` behavior for ProductCost
- add convenience enum for sqlalchemy-continuum operation types

## v0.19.1 (2024-11-12)

### Fix

- make vendor optional, for Vendor Sample Files

## v0.19.0 (2024-10-22)

### Feat

- add support for new ordering batch from parsed file

### Fix

- fix method call signature

## v0.18.12 (2024-09-15)

### Fix

- update project links, kallithea -> forgejo

## v0.18.11 (2024-09-03)

### Fix

- move startup workaround for trainwreck query bug

## v0.18.10 (2024-09-03)

### Fix

- add startup workaround for trainwreck query bug

## v0.18.9 (2024-08-30)

### Fix

- change import for wuttjamaican base model

## v0.18.8 (2024-08-28)

### Fix

- move "record changes" global hook to startup()
- cleanup old code for "record changes" session feature

## v0.18.7 (2024-08-27)

### Fix

- hopefully fix startup continuum bug per 'active_history' models

## v0.18.6 (2024-08-26)

### Fix

- inherit from wuttjamaican for `EmailHandler`

## v0.18.5 (2024-08-26)

### Fix

- avoid legacy config methods within `make_config()`
- tweak how versioning is configured and confirmed

## v0.18.4 (2024-08-22)

### Fix

- use app.get_title() and app.get_node_title(); avoid deprecated calls

## v0.18.3 (2024-08-20)

### Fix

- suppress warning when checking for legacy `app_package` config
- partially restore previous logic for `app.get_version()`

## v0.18.2 (2024-08-20)

### Fix

- minor tweaks to modernize etc.
- deprecate more methods for config object
- deprecate `config.rattail_engines` in favor of `appdb_engines`
- fix wrong name in deprecation warning

## v0.18.1 (2024-08-15)

### Fix

- move `get_class_hierarchy()` util function to wuttjamaican
- improve logic/fallback for `str(person)`

## v0.18.0 (2024-08-15)

### Feat

- refactor config/extension, session logic per wuttjamaican

### Fix

- let wuttjamaican configure app db engines
- use `ModelBase` from wuttjamaican, as our model base class
- cascade deletions for Customer -> CustomerShopper

## v0.17.11 (2024-08-13)

### Fix

- grow column size for `MemberEquityPayment.amount`
- stop logging config files read

## v0.17.10 (2024-08-09)

### Fix

- add `rattail.util.render_duration()` function
- stop setting falafel theme in installer

## v0.17.9 (2024-08-08)

### Fix

- remove ref to missing variable

## v0.17.8 (2024-08-06)

### Fix

- move logic upstream for `save_setting()`, `delete_setting()`

## v0.17.7 (2024-08-05)

### Fix

- `AppHandler.get_version()` should use upstream logic

## v0.17.6 (2024-08-05)

### Fix

- method for `AuthHandler.user_is_admin()` moved upstream
- invoke wuttjamaican logic for `rattail.util.prettify()`

## v0.17.5 (2024-07-18)

### Fix

- require latest wuttjamaican

## v0.17.4 (2024-07-17)

### Fix

- rename auth handler; avoid app in provider constructor

## v0.17.3 (2024-07-16)

### Fix

- fix bugs in `OrgHandler.get_subdepartment()`
- avoid deprecated calls to `administrator_role()`

## v0.17.2 (2024-07-16)

### Fix

- avoid deprecated `self.model` for people handler

## v0.17.1 (2024-07-15)

### Fix

- avoid deprecated `self.model` within the auth handler

## v0.17.0 (2024-07-14)

### Feat

- move most of auth handler logic to wuttjamaican

### Fix

- rename some constraints per wutta model

## v0.16.1 (2024-07-12)

### Fix

- remove duplicate method for `AppHandler.load_object()`
- remove duplicate method for `RattailConfig.production()`

## v0.16.0 (2024-07-11)

### Feat

- move some app model logic to wuttjamaican

## v0.15.0 (2024-07-09)

### Feat

- drop python 3.6 support, use pyproject.toml (again)

## v0.14.8 (2024-07-05)

### Fix

- fix model reference in reporting handler

## v0.14.7 (2024-07-04)

### Fix

- add `get_cmd()` method for import handlers

- specify default list for rattail mail templates

- add `get_role()` method for auth handler

## v0.14.6 (2024-07-04)

### Fix

- refactor code so most things work without sqlalchemy

- avoid command line errors if sqlalchemy not installed

- bump version for wuttjamaican

## v0.14.5 (2024-07-04)

### Fix

- change how we override default app handler, engine maker

## v0.14.4 (2024-07-02)

### Fix

- avoid `pkg_resources` for `files.resource_path()`

## v0.14.3 (2024-07-02)

### Fix

- include importing subcommands for discovery

## v0.14.2 (2024-07-02)

### Fix

- delay imports from `wuttjamaican.db`

## v0.14.1 (2024-07-01)

### Fix

- remove references, dependency for `six` package

- remove some unused imports

- remove duplicated / unused code for `rattail.db.config`

- deprecate `parse_bool()` and `parse_list()` in `rattail.config`

## v0.14.0 (2024-07-01)

### Feat

- remove legacy command system

### Fix

- make pyproject.toml instead of setup.cfg for generated project

## v0.13.5 (2024-06-28)

### Fix

- read logs from journald by default, for postfix-summary

- allow config override of "problems" for postfix-summary

## v0.13.4 (2024-06-27)

### Fix

- fix missing module import

## v0.13.3 (2024-06-24)

### Fix

- merge associated shopper records when merging 2 people

- truncate invoice item description for receiving, if needed

## v0.13.2 (2024-06-14)

### Fix

- revert back to setup.py + setup.cfg

## v0.13.1 (2024-06-10)

### Fix

- move canonical app version to pyproject.toml

## v0.13.0 (2024-06-10)

### Feat

- switch from setup.cfg to pyproject.toml / hatchling

## v0.12.9 (2024-06-10)

### Feat

- add config snippet for new projects, to define static libcache
- define the `app_package` setting for new projects
- add `get_pkg_version()` convenience function

## v0.12.8 (2024-06-06)

### Feat

- project generator should make typer commands, not old-style
- remove old/unused project scaffold template
- add snippet for fanstatic/libcache when generating web project

### Fix

- fix missing import for `rattail make-config` command
- define the `-n` command flag as alias for `--no-init`

## v0.12.7 (2024-06-02)

### Fix

- fix datasync command args, per typer

## v0.12.6 (2024-06-01)

### Feat

- add setting to allow decimal quantities for ordering/receiving

### Fix

- fix `rattail datasync remove-settings` command line, per typer
- fix `--progress-socket` arg handling for typer commands

## v0.12.5 (2024-05-31)

### Fix

- fix args for `rattail populate-batch` command, per typer

## v0.12.4 (2024-05-31)

### Fix

- fix params for generic "run purge" command logic, per typer

## v0.12.3 (2024-05-31)

### Fix

- fix args for `rattail purge-batches` command, per typer

## v0.12.2 (2024-05-30)

### Feat

- log the `pflogsumm` command before running it

### Fix

- fix some commands/arguments, per typer

## v0.12.1 (2024-05-29)

### Feat

- include organic flag when normalizing product

## v0.12.0 (2024-05-29)

This release begins the migration to use `typer` for all commands,
instead of the "traditional" (now WuttJamaican-based) commands.

### Feat

- add `get_runas_user()` method for AppHandler
- move rich and prompt_toolkit things to separate module
- move `finalize_session()` function to `db.util` module
- move "install" command logic to separate handler/module
- move "import command runner" logic to separate handler
- add basic support for `typer` command system
- migrate all commands to use typer
- add command logic functions for running reports, purging things

### Fix

- fix subcommand runas user when caller provides username


## Older Releases

Please see `docs/OLDCHANGES.rst` for older release notes.
