## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Tasks for ${name}
"""

import os
import json

from invoke import task


@task
def release(c):
    """
    Release a new version of ${name}
    """
    # figure out current package version
    package_json = os.path.join(os.path.dirname(__file__), 'package.json')
    with open(package_json, 'rt') as f:
        js = json.load(f)
        version = js['version']

    # use production appsettings for the build
    if not os.path.exists('src/appsettings.building.js'):
        # don't overwrite this file, if previous build failed, since that would
        # cause us to lose our local settings
        c.run('mv --force src/appsettings.js src/appsettings.building.js')
    c.run('cp src/appsettings.production.js src/appsettings.js')

    # build the app, create zip archive
    c.run('npm run build')
    os.chdir('dist')
    c.run('zip --recurse-paths ${slug}-{}.zip *'.format(version))

    # TODO: upload zip archive somewhere...
    filename = '${slug}-{}.zip'.format(version)
    #c.run(f'scp {filename} me@server:/path/to/pypi/{filename}')
    #c.run(f"ssh me@server 'cd /path/to/pypi && ln -sf {filename} latest.zip'")

    # restore previous appsettings
    os.chdir(os.pardir)
    c.run('mv --force src/appsettings.building.js src/appsettings.js')
