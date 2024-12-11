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
Mako utility logic
"""

import os

from mako.lookup import TemplateLookup

from rattail.files import resource_path


class ResourceTemplateLookup(TemplateLookup):
    """
    This logic was largely copied/inspired from pyramid_mako,
    https://github.com/Pylons/pyramid_mako/blob/main/src/pyramid_mako/__init__.py
    """

    def adjust_uri(self, uri, relativeto):

        # do not adjust "resource path spec" uri
        isabs = os.path.isabs(uri)
        if (not isabs) and (':' in uri):
            return uri

        return super(ResourceTemplateLookup, self).adjust_uri(uri, relativeto)

    def get_template(self, uri):

        # check if uri looks like a "resource path spec"
        isabs = os.path.isabs(uri)
        if (not isabs) and (':' in uri):

            # it does..first use normal logic to try fetching from cache
            try:
                if self.filesystem_checks:
                    return self._check(uri, self._collection[uri])
                else:
                    return self._collection[uri]
            except KeyError as e:

                # but if not already in cache, must convert resource
                # path spec to absolute path on disk, and load that
                path = resource_path(uri)
                if os.path.exists(path):
                    return self._load(path, uri)

        # fallback to normal logic
        return super(ResourceTemplateLookup, self).get_template(uri)
