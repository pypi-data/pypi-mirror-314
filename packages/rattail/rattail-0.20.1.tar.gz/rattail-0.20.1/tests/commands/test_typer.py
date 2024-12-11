# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch

from wuttjamaican.testing import FileConfigTestCase

from rattail.commands import typer as mod


class TestMakeCliConfig(FileConfigTestCase):

    def test_basic(self):
        # nb. must specify config file to avoid any files in dev environment
        myconf = self.write_file('my.conf', '')
        ctx = MagicMock(params={
            'config_paths': [myconf],
        })
        config = mod.make_cli_config(ctx)
        self.assertEqual(config.files_read, [myconf])

    def test_no_init(self):
        ctx = MagicMock(params={
            'no_init': True,
        })
        config = mod.make_cli_config(ctx)
        self.assertEqual(config.files_read, [])

    def test_bad_model(self):
        myconf = self.write_file('my.conf', """
[rattail]
model_spec = invalid_model_spec
""")
        ctx = MagicMock(params={
            'config_paths': [myconf],
        })
        config = mod.make_cli_config(ctx)
        app = config.get_app()
        self.assertRaises(ImportError, getattr, app, 'model')

    def test_versioning(self):
        # nb. must specify config file to avoid any files in dev environment
        myconf = self.write_file('my.conf', '')
        ctx = MagicMock(params={
            'config_paths': [myconf],
            'versioning': True,
        })

        configure_versioning = MagicMock()
        mock_config = MagicMock(configure_versioning=configure_versioning)
        with patch.dict('sys.modules', **{'rattail.db.config': mock_config}):
            config = mod.make_cli_config(ctx)
            configure_versioning.assert_called_once()

    def test_missing_sqlalchemy(self):
        # nb. must specify config file to avoid any files in dev environment
        myconf = self.write_file('my.conf', '')
        ctx = MagicMock(params={
            'config_paths': [myconf],
        })

        orig_import = __import__

        def mock_import(name, globals=None, locals=None, fromlist={}, level=0):
            if name == 'rattail.db.config' and fromlist == ('configure_versioning',):
                return ImportError
            return orig_import(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

        with patch('builtins.__import__', side_effect=mock_import):
            # nb. just make sure there are no errors
            config = mod.make_cli_config(ctx)
