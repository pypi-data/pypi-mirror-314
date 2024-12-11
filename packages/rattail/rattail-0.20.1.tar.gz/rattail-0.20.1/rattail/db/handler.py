# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Handler
"""

import alembic.util
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext
from mako.lookup import TemplateLookup

from rattail.app import GenericHandler
from rattail.files import resource_path


class DatabaseHandler(GenericHandler):
    """
    Base class and default implementation for the DB handler.
    """

    def __init__(self, *args, **kwargs):
        super(DatabaseHandler, self).__init__(*args, **kwargs)

        # TODO: make templates dir configurable?
        templates = [resource_path('rattail:templates/db')]
        self.templates = TemplateLookup(directories=templates)

    def make_alembic_config(self, **kwargs):
        """
        Make a new Alembic config instance, based on config present in
        the current app.
        """
        alembic_config = AlembicConfig()

        # TODO: this seems pretty hacky.  we need (for some commands)
        # to have config path available within the alembic `env.py`
        # script.  to my knowledge alembic itself does not need the
        # file path, but rattail gets it from alembic config, so...
        alembic_config.config_file_name = self.config.files_read[-1]

        alembic_config.set_main_option(
            'script_location',
            self.config.get('alembic', 'script_location', usedb=False))

        alembic_config.set_main_option(
            'version_locations',
            self.config.get('alembic', 'version_locations', usedb=False))

        return alembic_config

    def check_alembic_current_head(self, **kwargs):
        """
        Checks to see if the DB is current with respect to alembic
        head(s).  Returns ``True`` if DB is current, else ``False``.
        """
        # cf. https://alembic.sqlalchemy.org/en/latest/cookbook.html#test-current-database-revision-is-at-head-s
        alembic_config = self.make_alembic_config()
        script = ScriptDirectory.from_config(alembic_config)
        with self.config.appdb_engine.begin() as connection:
            context = MigrationContext.configure(connection)
            return set(context.get_current_heads()) == set(script.get_heads())

    def get_alembic_branch_names(self, **kwargs):
        """
        Returns a list of Alembic branch names present in the default
        database schema.
        """
        alembic_config = self.make_alembic_config()
        script = ScriptDirectory.from_config(alembic_config)

        branches = set()
        for rev in script.get_revisions(script.get_heads()):
            branches.update(rev.branch_labels)

        return sorted(branches)

    def write_table_model(self, data, path, **kwargs):
        """
        Write code for a new table model, based on the given data
        dict, to the given path.
        """
        template = self.templates.get_template('/new-table.mako')
        content = template.render(**data)
        with open(path, 'wt') as f:
            f.write(content)

    def generate_revision_script(self, branch, message=None, **kwargs):
        """
        Auto-generate a revision (schema migration) script via Alembic.
        """
        alembic_config = self.make_alembic_config()
        script = alembic_command.revision(alembic_config,
                                          autogenerate=True,
                                          head='{}@head'.format(branch),
                                          message=message)
        return script

    def upgrade_db(self, **kwargs):
        """
        Upgrade the schema for default database.
        """
        alembic_config = self.make_alembic_config()
        alembic_command.upgrade(alembic_config, 'heads')

    def get_model_classes(self, **kwargs):
        """
        Return a list of all primary data model classes.
        """
        model = self.model
        classes = []
        for name in dir(model):
            obj = getattr(model, name)

            if (isinstance(obj, type)
                and issubclass(obj, model.Base)
                and obj is not model.Base):

                classes.append(obj)

        return classes
