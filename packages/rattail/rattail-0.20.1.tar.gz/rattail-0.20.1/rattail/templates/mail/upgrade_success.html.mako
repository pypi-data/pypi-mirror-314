## -*- coding: utf-8; -*-
<html>
  <head>
    <style type="text/css">
      label {
          display: block;
          font-weight: bold;
          margin-top: 1em;
      }
      p {
          margin: 1em 0 1em 1.5em;
      }
      p.notes {
          white-space: pre-wrap;
      }
    </style>
  </head>
  <body>
    <h1>Upgrade Success for ${system_title}</h1>

    <p>
      An upgrade was just performed for ${system_title}, and it seems
      to have gone off without a hitch.
    </p>

    <label>Description</label>
    <p><a href="${upgrade_url}">${upgrade.description}</a></p>

    <label>Notes</label>
    <p class="notes">${upgrade.notes}</p>

    <label>Executed</label>
    <p>${app.render_datetime(app.localtime(upgrade.executed, from_utc=True))}</p>

    <label>Executed by</label>
    <p>${upgrade.executed_by}</p>

  </body>
</html>
