## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} Trainwreck databases which were
    expected to exist, but are missing.&nbsp; Please investigate and
    fix at your convenience.
  </p>
</%def>

<%def name="simple_row(dbkey, i)">
  <tr>
    <td>${dbkey}</td>
  </tr>
</%def>

${self.simple_table(["DB Key"])}
