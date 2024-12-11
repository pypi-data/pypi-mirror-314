## -*- mode: markdown; -*-

# ${name}

This is a custom Rattail/Poser project, for ${organization}.  See the
[Rattail website](https://rattailproject.org/) for more info.

<%text>##</%text> Quick Start

Make a virtual environment:

    cd /path/to/envs
    python3 -m venv ./${env_name}

Enter and activate it:

    cd ${env_name}
    source bin/activate

Install the ${name} package:

    pip install ${pypi_name}

Run the ${name} app installer:

    ${pkg_name} install

<%text>##</%text> Running from Source

The above shows how to run from a package release.

To run from local source folder instead, substitute the `pip install`
command above with:

    pip install -e /path/to/src/${folder}
