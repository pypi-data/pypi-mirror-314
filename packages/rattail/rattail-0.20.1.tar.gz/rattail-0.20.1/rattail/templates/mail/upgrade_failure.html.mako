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
    <h1>Upgrade Failure for ${system_title}</h1>

    <p>
      An upgrade was just attempted for ${system_title}, but something
      seems to have gone wrong!
    </p>

    <label>Description</label>
    <p><a href="${upgrade_url}">${upgrade.description}</a></p>

    <label>Notes</label>
    <p class="notes">${upgrade.notes}</p>

    <label>Executed</label>
    <p>${app.render_datetime(app.localtime(upgrade.executed, from_utc=True))}</p>

    <label>Executed by</label>
    <p>${upgrade.executed_by}</p>

    <label>Exit Code</label>
    <p>${upgrade.exit_code}</p>

  </body>
</html>
