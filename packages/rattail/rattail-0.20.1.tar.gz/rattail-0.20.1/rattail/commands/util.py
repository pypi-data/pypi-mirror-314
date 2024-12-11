# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Command utilities
"""

import subprocess
import sys

from wuttjamaican.util import parse_bool


def require_prompt_toolkit():
    try:
        import prompt_toolkit
    except ImportError:
        value = input("\nprompt_toolkit is not installed.  shall i install it? [Yn] ")
        value = value.strip()
        if value and not parse_bool(value):
            sys.stderr.write("prompt_toolkit is required; aborting\n")
            sys.exit(1)

        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', 'prompt_toolkit'])


def require_rich():
    try:
        import rich
    except ImportError:
        value = input("\nrich is not installed.  shall i install it? [Yn] ")
        value = value.strip()
        if value and not parse_bool(value):
            sys.stderr.write("rich is required; aborting\n")
            sys.exit(1)

        subprocess.check_call([sys.executable, '-m', 'pip',
                               'install', 'rich'])


def rprint(*args, **kwargs):
    require_rich()

    # TODO: this could look different once python2 is out of the
    # picture; but must avoid `print` keyword for python2
    import rich
    rprint = getattr(rich, 'print')
    return rprint(*args, **kwargs)


def basic_prompt(info, default=None, is_password=False, is_bool=False, required=False):
    require_prompt_toolkit()

    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style

    # message formatting styles
    style = Style.from_dict({
        '': '',
        'bold': 'bold',
    })

    # build prompt message
    message = [
        ('', '\n'),
        ('class:bold', info),
    ]
    if default is not None:
        if is_bool:
            message.append(('', ' [{}]: '.format('Y' if default else 'N')))
        else:
            message.append(('', ' [{}]: '.format(default)))
    else:
        message.append(('', ': '))

    # prompt user for input
    try:
        text = prompt(message, style=style, is_password=is_password)
    except (KeyboardInterrupt, EOFError):
        rprint("\n\t[bold yellow]operation canceled by user[/bold yellow]\n",
                    file=sys.stderr)
        sys.exit(2)

    if is_bool:
        if text == '':
            return default
        elif text.upper() == 'Y':
            return True
        elif text.upper() == 'N':
            return False
        rprint("\n\t[bold yellow]ambiguous, please try again[/bold yellow]\n")
        return basic_prompt(info, default, is_bool=True)

    if required and not text and not default:
        return basic_prompt(info, default, is_password=is_password,
                            required=True)

    return text or default
