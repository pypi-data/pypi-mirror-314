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
Report Commands
"""

import logging

from sqlalchemy import orm

from rattail.time import get_sunday, get_monday


log = logging.getLogger(__name__)


def run_weekly_report(config, report_key, simple_report_name, email_key=None, user=None,
                      progress=None):
    app = config.get_app()
    model = app.model
    session = app.make_session()

    # first must determine most recent complete Mon-Sun date range
    # TODO: should probably be more flexible about date range..
    today = app.today()
    sunday = get_sunday(today)
    monday = get_monday(sunday)
    start_date = monday
    end_date = sunday

    # determine naming for the report
    report_name = "{} {} thru {}".format(
        simple_report_name,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"))

    try:
        # see if this report has already been ran
        output = session.query(model.ReportOutput)\
                        .filter(model.ReportOutput.report_type == report_key)\
                        .filter(model.ReportOutput.report_name == report_name)\
                        .one()

    except orm.exc.NoResultFound:

        # generate report file and commit result
        handler = app.get_report_handler()
        report = handler.get_report(report_key)
        params = {'start_date': start_date, 'end_date': end_date}
        if user:
            user = session.get(model.User, user.uuid)
        output = handler.generate_output(session, report, params, user,
                                         progress=progress)
        session.commit()

        # try to make url for report
        report_url = None
        base_url = config.base_url()
        if base_url:
            report_url = '{}/reports/generated/{}'.format(
                base_url, output.uuid)

        # send report output as email
        handler.email_output(report, output, email_key or report_key,
                             extra_data={'report_url': report_url})

    else:
        log.warning("report output already exists: %s", report_name)

    session.close()
