## -*- mode: markdown; -*-

# ${name}

This is a Vue.js mobile frontend app, based on `byjove` and meant for
use with a Tailbone API backend.

It comes with basic app structure, user auth (login) etc.


<%text>##</%text> Getting Started

First install requirements:

    npm install

There are a couple of config files in this project, which will vary
per instance and so you must create these, and modify as needed:

    cp vue.config.js.dist vue.config.js
    cp src/appsettings.js.dist src/appsettings.js

Then run the app with:

    npm run serve


<%text>##</%text> Production Deployment

There is an `invoke` task for this.

TODO: you will need to edit `tasks.py` to make this work 100%

    inv release
