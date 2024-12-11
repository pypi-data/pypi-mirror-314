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
Utilities
"""

import collections
import importlib
import re
import shlex
import unicodedata
import datetime
import decimal
import subprocess
import warnings

from uuid_extensions import uuid7

from wuttjamaican.util import (UNSPECIFIED,
                               load_entry_points as wutta_load_entry_points,
                               load_object as wutta_load_object,
                               make_title as wutta_make_title,
                               get_class_hierarchy as wutta_get_class_hierarchy)


# TODO: deprecate / remove this
NOTSET = UNSPECIFIED


class OrderedDict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        warnings.warn("rattail.util.OrderedDict is deprecated; "
                      "please use collections.OrderedDict instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


def capture_output(*args, **kwargs):
    """
    Runs ``command`` and returns any output it produces.
    """
    # We *need* to pipe ``stdout`` because that's how we capture the output of
    # the ``hg`` command.  However, we must pipe *all* handles in order to
    # prevent issues when running as a GUI but *from* the Windows console.  See
    # also: http://bugs.python.org/issue3905
    kwargs.update({
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    })
    output = subprocess.Popen(*args, **kwargs).communicate()[0]
    return output


def data_diffs(local_data, host_data, fields=None,
               fuzzy_fields=None, fuzz_factor=None):
    """
    Find all (relevant) fields which differ between the host and local data
    values for a given record.
    """
    if fields is None:
        fields = list(local_data)

    diffs = []
    fuzzy_time_cutoff = datetime.timedelta(seconds=fuzz_factor or 1)
    for field in fields:

        # maybe raise explicit error to indicate *which* dict is missing data
        # (otherwise the comparison below raises "ambiguous" error about it)
        if field not in local_data:
            raise KeyError("key '{}' is missing from local_data".format(field))
        if field not in host_data:
            raise KeyError("key '{}' is missing from host_data".format(field))

        local_value = local_data[field]
        host_value = host_data[field]

        if fuzzy_fields and field in fuzzy_fields:

            if local_value and not host_value:
                diffs.append(field)
                continue

            if host_value and not local_value:
                diffs.append(field)
                continue

            if isinstance(local_value, datetime.datetime):

                if (host_value > local_value
                    and host_value - local_value >= fuzzy_time_cutoff):
                    diffs.append(field)

                elif (local_value > host_value
                      and local_value - host_value >= fuzzy_time_cutoff):
                    diffs.append(field)

                continue

            elif isinstance(local_value, (int, float, decimal.Decimal)):

                if (host_value > local_value
                    and host_value - local_value >= fuzz_factor):
                    diffs.append(field)

                elif (local_value > host_value
                      and local_value - host_value >= fuzz_factor):
                    diffs.append(field)

                continue

        if local_value != host_value:
            diffs.append(field)

    return diffs


def get_class_hierarchy(klass, topfirst=True):
    """
    DEPRECATED - use
    :func:`wuttjamaican:wuttjamaican.util.get_class_hierarchy()`
    instead.
    """
    warnings.warn("rattail.util.get_class_hierarchy() is deprecated; "
                  "please use wuttjamaican.util.get_class_hierarchy() instead",
                  DeprecationWarning, stacklevel=2)
    return wutta_get_class_hierarchy(klass, topfirst=topfirst)


def get_package_name(name):
    """
    Generic logic to derive a "package name" from the given name.

    E.g. if ``name`` is "Poser Plus" this will return "poser_plus"
    """
    # cf. https://stackoverflow.com/a/3194567
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    words = re.split(r'[\- ]', name)
    return '_'.join([word.lower() for word in words])


def get_studly_prefix(name):
    """
    Generic logic to derive a "studly prefix" from the given name.

    E.g. if ``name`` is "Poser Plus" this will return "PoserPlus"
    """
    # cf. https://stackoverflow.com/a/3194567
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    words = re.split(r'[\- ]', name)
    return ''.join([word.capitalize() for word in words])


def import_module_path(module_path):
    """
    Import an arbitrary Python module.

    .. warning::

       This function is deprecated; please use
       :func:`python:importlib.import_module()` instead.

    :param module_path: String referencing a module by its "dotted path".

    :returns: The referenced module.
    """
    warnings.warn("rattail.util.import_module_path() is deprecated; "
                  "please use importlib.import_module() instead",
                  DeprecationWarning, stacklevel=2)

    return importlib.import_module(module_path)


def import_reload(module):
    """
    Reload a module.

    .. warning::

       This function is deprecated; please use
       :func:`python:importlib.reload()` instead.

    :param module: An already-loaded module.

    :returns: The module.
    """
    warnings.warn("rattail.util.import_reload() is deprecated; "
                  "please use importlib.reload() instead",
                  DeprecationWarning, stacklevel=2)

    return importlib.reload(module)


def get_object_spec(obj):
    """
    Returns the "object spec" string for the given object.
    """
    # TODO: this only handles a class *instance* currently
    return '{}:{}'.format(obj.__module__, obj.__class__.__name__)


def load_object(spec):
    """
    Load an arbitrary object from a module, according to a specifier.

    This is a compatibility wrapper around
    :func:`wuttjamaican:wuttjamaican.util.load_object()`.  New code
    should use that instead; this will eventually be removed.
    """
    return wutta_load_object(spec)


def load_entry_points(group, ignore_errors=False):
    """
    Load a set of ``setuptools``-style entry points.

    This is a compatibility wrapper around
    :func:`wuttjamaican:wuttjamaican.util.load_entry_points()`.  New
    code should use that instead; this will eventually be removed.
    """
    return wutta_load_entry_points(group, ignore_errors=ignore_errors)


def get_pkg_version(name):
    """
    Returns the version number for the given package name, per package
    metadata.
    """
    try:
        from importlib.metadata import version
    except ImportError:
        from importlib_metadata import version
    return version(name)


def make_uuid():
    """
    Generate a universally-unique identifier.

    :returns: A 32-character hex string.
    """
    return uuid7().hex


# TODO: deprecate / remove this
def prettify(text):
    """
    DEPRECATED - use
    :meth:`wuttjamaican:wuttjamaican.app.AppHandler.make_title()`
    instead.
    """
    return wutta_make_title(text)


def pretty_boolean(value):
    """
    Returns ``'Yes'`` or ``'No'`` or empty string if value is ``None``
    """
    if value is None:
        return ""
    return "Yes" if value else "No"


def hours_as_decimal(hours, places=2):
    """
    Convert the given ``datetime.timedelta`` object into a Decimal whose
    value is in terms of hours.
    """
    if hours is None:
        return
    minutes = (hours.days * 1440) + (hours.seconds // 60)
    fmt = '{{:0.{}f}}'.format(places)
    return decimal.Decimal(fmt.format(minutes / 60.0))


def pretty_hours(hours=None, seconds=None):
    """
    DEPRECATED - use :meth:`rattail.app.AppHandler.render_duration()`
    instead.
    """
    warnings.warn("pretty_hours() function is deprecated; please "
                  "use AppHandler.render_duration() insted",
                  DeprecationWarning, stacklevel=2)

    if hours is None and seconds is None:
        return ''
    if hours is None:
        hours = datetime.timedelta(seconds=seconds)

    # determine if hours value is positive or negative.  seems like some of the
    # math can be "off" if negative values are involved, in which case we'll
    # convert to positive for sake of math and then prefix result with a hyphen
    negative = False

    if isinstance(hours, decimal.Decimal):
        if hours < 0:
            negative = True
            hours = -hours
        hours = datetime.timedelta(seconds=int(hours * 3600))

    minutes = (hours.days * 1440) + (hours.seconds / 60)
    rendered = "{}:{:02d}".format(int(minutes // 60), int(minutes % 60))
    if negative:
        rendered = "-{}".format(rendered)
    return rendered


def pretty_quantity(value, empty_zero=False):
    """
    Return a "pretty" version of the given value, as string.  This is meant primarily
    for use with things like order quantities, so that e.g. 1.0000 => 1
    """
    if value is None:
        return ''
    if int(value) == value:
        value = int(value)
        if empty_zero and value == 0:
            return ''
        return str(value)
    return str(value).rstrip('0')


def render_duration(delta=None, hours=None, seconds=None):
    """
    Render a time duration for human eyes, e.g. "1:30" for 1.5 hours.

    Note that you must specify one of: ``delta``, ``hours``, ``seconds``.

    :param delta: If specified, should be a ``datetime.timedelta``
       object representing the duration.

    :param hours: If specified, should be the number of hours
       elapsed for the duration, as decimal.

    :param seconds: If specified, should be the number of seconds
       elapsed for the duration, as integer.

    :returns: Duration rendered as human-friendly string.  Note
       that if all params are empty, this will return an empty
       string.
    """
    if delta is None and hours is None and seconds is None:
        return ""

    if delta is None:
        if seconds is None:
            seconds = int(hours * 60 * 60)
        delta = datetime.timedelta(seconds=seconds)

    # calculate minutes for the 'seconds' portion of delta.  note
    # that we must ensure it is correctly rounded
    minutes = delta.seconds / 60
    minutes = decimal.Decimal(str(minutes)).quantize(decimal.Decimal('1'))

    # now add in minutes for the 'days' portion of delta
    minutes += delta.days * 24 * 60

    # calculate/render final string
    hours = int(minutes // 60)
    minutes = int(minutes % 60)
    return f"{hours}:{minutes:02d}"


def progress_loop(func, items, factory, *args, **kwargs):
    """
    This will iterate over ``items`` and call ``func`` for each.  If a progress
    ``factory`` kwarg is provided, then a progress instance will be created and
    updated along the way.
    """
    message = kwargs.pop('message', None)
    count = kwargs.pop('count', None)
    allow_cancel = kwargs.pop('allow_cancel', False)
    if count is None:
        try:
            count = len(items)
        except TypeError:
            count = items.count()
    if not count:
        return True

    prog = None
    if factory:
        prog = factory(message, count)

    canceled = False
    for i, item in enumerate(items, 1):
        func(item, i, *args, **kwargs)
        if prog and not prog.update(i):
            canceled = True
            break
    if prog:
        prog.finish()
    if canceled and not allow_cancel:
        raise RuntimeError("Operation was canceled")
    return not canceled


def simple_error(error):
    """
    Return a "simple" string for the given error.  Result will look like::

       "ErrorClass: Description for the error"

    However the logic checks to ensure the error has a descriptive message
    first; if it doesn't the result will just be::

       "ErrorClass"
    """
    cls = str(type(error).__name__)
    msg = str(error)
    if msg:
        return "{}: {}".format(cls, msg)
    return cls


def shlex_join(split_command):
    """
    Wrapper which invokes ``shlex.join()`` if available; otherwise
    a workaround is implemented.

    cf. https://stackoverflow.com/a/50022816
    """
    # python 3.8+ has native shlex.join()
    if hasattr(shlex, 'join'):
        return shlex.join(split_command)

    # python 3.3+ has native shlex.quote()
    if hasattr(shlex, 'quote'):
        return ' '.join(shlex.quote(x) for x in split_command)

    # python 2 has neither...so the rest of this logic is copy/pasted
    # from later python
    # _find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search
    _find_unsafe = re.compile(r'[^\w@%+=:,./-]').search

    def quote(s):
        """Return a shell-escaped version of the string *s*."""
        if not s:
            return "''"
        if _find_unsafe(s) is None:
            return s

        # use single quotes, and put single quotes into double quotes
        # the string $'b is then quoted as '$'"'"'b'
        return "'" + s.replace("'", "'\"'\"'") + "'"

    return ' '.join(quote(x) for x in split_command)
