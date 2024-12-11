## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} pending product records.&nbsp; Please
    resolve or ignore, at your convenience.
  </p>

  % if url:
      <p><a href="${url}">${url}</a></p>
  % endif
</%def>

<%def name="simple_row(pending, i)">
  <tr>
    <td>${products_handler.render_product_key(pending)}</td>
    <td>${pending.brand_name}</td>
    <td>${pending.description}</td>
    <td>${pending.size}</td>
    <td>${enum.PENDING_PRODUCT_STATUS[pending.status_code]}</td>
  </tr>
</%def>

${self.simple_table([app.get_product_key_label(), "Brand", "Description", "Size", "Status"])}
