## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} product keys which are
    duplicated.&nbsp; In other words each key show below, corresponds
    to more than one product.&nbsp; Please investigate and fix at your
    convenience.
  </p>
</%def>

<%def name="simple_row(obj, i)">
  <% key, products = obj %>
  <tr>
    <td>${key}</td>
    <td><ul>
        % for product in products:
            <li>${product}</li>
        % endfor
    </ul></td>
  </tr>
</%def>

${self.simple_table([product_key_label, "Products"])}
