## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Tasks for ${name}
"""

import os
import shutil

from invoke import task


@task
def release(c):
    """
    Release a new version of ${name}
    """

    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('${egg_name}.egg-info'):
        shutil.rmtree('${egg_name}.egg-info')

    c.run('python -m build --sdist')

    # TODO: uncomment and update these details, to upload to private PyPI
    #c.run('scp dist/* myuser@pypi.example.com:/srv/pypi/${folder}/')

    # TODO: or, uncomment this to upload to public PyPI
    #c.run('twine upload dist/*')
