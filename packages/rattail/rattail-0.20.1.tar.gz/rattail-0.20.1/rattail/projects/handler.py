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
Handler for Generating Projects
"""

import os
import shutil
import warnings
import zipfile
from collections import OrderedDict

from rattail.util import load_entry_points


class ProjectHandler(object):
    """
    Base class for project handlers.
    """

    def __init__(self, config):
        self.config = config
        self.app = self.config.get_app()

    def get_all_project_generators(self):
        """
        Returns an ``OrderedDict`` with all available project
        generators.
        """
        generators = load_entry_points('rattail.projects')
        generators = sorted(generators.items(),
                            key=lambda itm: itm[0])
        return OrderedDict(generators)

    def get_all_project_types(self):
        """
        Returns the list of keys for *all* possible project types.
        """
        warnings.warn("get_all_project_types() is deprecated; "
                      "please use get_all_project_generators() instead",
                      DeprecationWarning, stacklevel=2)

        return list(self.get_all_project_generators())

    def get_supported_project_generators(self):
        """
        Returns the list of "supported" project generators.
        """
        return self.get_all_project_generators()

    def get_supported_project_types(self):
        """
        Returns the list of keys for "supported" project types.
        """
        warnings.warn("get_supported_project_types() is deprecated; "
                      "please use get_supported_project_generators() instead",
                      DeprecationWarning, stacklevel=2)

        return list(self.get_supported_project_generators())

    def get_project_generator(self, key, require=False):
        """
        Returns a ``ProjectGenerator`` instance for the given key.

        If the key is not valid, returns ``None`` unless
        ``require=True`` in which case an error is raised.
        """
        generators = self.get_all_project_generators()
        if key in generators:
            return generators[key](self.config)
        if require:
            raise RuntimeError("Project generator not found for: {}".format(key))

    def get_storage_dir(self):
        """
        Returns the path to root storage (output) dir for all generated
        projects.
        """
        path = self.config.get('rattail', 'generated_projects.storage_dir')
        if path:
            return path
        return os.path.join(self.config.workdir(require=True),
                            'generated-projects')

    def make_project_schema(self, key):
        """
        Make and return a colander schema representing the context
        needed for generating a project for the given key.
        """
        generator = self.get_project_generator(key, require=True)
        return generator.make_schema()

    def generate_project(self, key, output=None, context=None, **kwargs):
        """
        Generate source code for a new project, and return the path to
        the output folder.

        :param key: Key identifying which type of project to generate.

        :param output: Optional path to the output folder.  If not
           specified, one will be determined automatically.

        :param context: Data dictionary with template context,
           appropriate for the project type.
        """
        generator = self.get_project_generator(key)
        context = generator.normalize_context(context or {})

        if not output:
            folder = context.get('folder', key)
            output = os.path.join(self.get_storage_dir(), folder)

        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)

        generator.generate_project(output, context)
        return output

    def zip_output(self, output, zipped=None):
        """
        Compress the given output folder and save as ZIP file.

        :param output: Path to the output folder.

        :param zipped: Optional path to the final ZIP file.  If not
           specified, it will be the same path as ``output`` but with
           a ``.zip`` file extension.
        """
        if not zipped:
            zipped = '{}.zip'.format(output)

        folder = os.path.basename(output)

        with zipfile.ZipFile(zipped, 'w', zipfile.ZIP_DEFLATED) as z:
            self.zipdir(z, output, folder)

        return zipped

    def zipdir(self, zipf, path, folder):
        for root, dirs, files in os.walk(path):
            relative_root = os.path.join(folder, root[len(path)+1:])
            for fname in files:
                zipf.write(os.path.join(root, fname),
                           arcname=os.path.join(relative_root, fname))


class RattailProjectHandler(ProjectHandler):

    def __init__(self, *args, **kwargs):
        warnings.warn("RattailProjectHandler is deprecated; "
                      "please just use ProjectHandler instead",
                      DeprecationWarning, stacklevel=2)
        super(RattailProjectHandler, self).__init__(*args, **kwargs)
