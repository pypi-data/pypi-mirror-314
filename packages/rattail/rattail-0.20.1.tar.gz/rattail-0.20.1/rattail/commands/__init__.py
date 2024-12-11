# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
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
Console Commands
"""

from .base import rattail_typer

# TODO: is this the best we can do, to register available commands?
from . import backup
from . import batch
from . import bouncer
from . import checkdb
from . import cleanup
from . import clonedb
from . import datasync
from . import date_organize
from . import filemon
from . import importing
from . import luigi
from . import mailmon
from . import make_appdir
from . import make_config
from . import make_user
from . import make_uuid
from . import mysql
from . import postfix
from . import problems
from . import products
from . import projects
from . import run_n_mail
from . import runsql
from . import settings
from . import telemetry
from . import upgrade
from . import versions

# discover more commands
from .typer import typer_eager_imports
typer_eager_imports(rattail_typer)
