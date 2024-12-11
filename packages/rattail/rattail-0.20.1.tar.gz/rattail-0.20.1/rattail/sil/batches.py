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
Batch Stuff
"""

import configparser
import warnings

import lockfile

from rattail.config import get_user_file
from rattail.batch import batch_id_str


def consume_batch_id(source='RATAIL'):
    """
    Returns the next available batch identifier for ``source``, incrementing
    the number to preserve uniqueness.
    """
    warnings.warn("sil.consume_batch_id() function is deprecated; "
                  "please use batch_handler.consume_batch_id() instead",
                  DeprecationWarning, stacklevel=2)

    path = get_user_file('rattail.conf', createdir=True)
    with lockfile.LockFile(path):

        parser = configparser.RawConfigParser()
        parser.read(path)
        option = 'next_batch_id.{0}'.format(source)

        batch_id = 1
        if parser.has_section('rattail.sil'):
            if parser.has_option('rattail.sil', option):
                batch_id = parser.get('rattail.sil', option)
                batch_id = int(batch_id) if batch_id.isdigit() else 1

        if not parser.has_section('rattail.sil'):
            parser.add_section('rattail.sil')
        parser.set('rattail.sil', option, str(batch_id + 1))

        with open(path, 'wt') as f:
            parser.write(f)

    return batch_id_str(batch_id)
