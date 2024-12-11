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
Commands related to purging of old data
"""

import os
import datetime
import shutil
import logging


log = logging.getLogger(__name__)


def run_purge(config, purge_title, purge_title_plural, thing_finder, thing_purger,
              before=None, before_days=None, default_before_days=90,
              dry_run=False, progress=None):
    from rattail.db.util import finalize_session

    log.info("will purge things of type: %s", purge_title)

    if before and before_days:
        log.warning("specifying both --before and --before-days is "
                    "redundant; --before will take precedence.")

    app = config.get_app()
    session = app.make_session()

    # calculate our cutoff date
    if before:
        cutoff = before
    else:
        today = app.today()
        cutoff = today - datetime.timedelta(days=before_days or default_before_days)
    cutoff = datetime.datetime.combine(cutoff, datetime.time(0))
    cutoff = app.localtime(cutoff)
    log.info("using %s as cutoff date", cutoff.date())

    # find things, and purge them
    things = thing_finder(session, cutoff, dry_run=dry_run)
    log.info("found %s thing(s) to purge", len(things or []))
    if things:
        purged = purge_things(config, session, things, thing_purger, cutoff, purge_title_plural,
                              dry_run=dry_run, progress=progress)
        log.info("%spurged %s %s",
                 "(would have) " if dry_run else "",
                 purged, purge_title_plural)

    finalize_session(session, dry_run=dry_run)


def purge_things(config, session, things, purger, cutoff, purge_title_plural,
                 dry_run=False, progress=None):
    app = config.get_app()
    result = app.make_object(purged=0)

    def purge(thing, i):
        if purger(session, thing, cutoff, dry_run=dry_run):
            result.purged += 1
        if i % 200 == 0:
            session.flush()

    app.progress_loop(purge, things, progress,
                      message=f"Purging {purge_title_plural}")
    return result.purged
