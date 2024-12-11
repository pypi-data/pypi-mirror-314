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
Trainwreck Config
"""

from wuttjamaican.conf import WuttaConfigExtension

try:
    from rattail.trainwreck.db import Session as TrainwreckSession
except ImportError:
    TrainwreckSession = None


class TrainwreckConfig(WuttaConfigExtension):
    """
    Configures any Trainwreck database connections
    """
    key = 'rattail.trainwreck'

    def configure(self, config):
        if TrainwreckSession:
            from wuttjamaican.db import get_engines
            engines = get_engines(config, 'trainwreck.db')
            config.trainwreck_engines = engines
            config.trainwreck_engine = engines.get('default')
            TrainwreckSession.configure(bind=config.trainwreck_engine)
