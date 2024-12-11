## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${problems[0][0]} Trainwreck transactions which are
    older than the cutoff date, ${app.render_date(problems[0][1].date())}.&nbsp; Please
    investigate and fix at your convenience.
  </p>
</%def>
