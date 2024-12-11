# -*- coding: utf-8; -*-

try:
    from importlib.metadata import version
except ImportError: # pragma: no cover
    from importlib_metadata import version


__version__ = version('rattail')
