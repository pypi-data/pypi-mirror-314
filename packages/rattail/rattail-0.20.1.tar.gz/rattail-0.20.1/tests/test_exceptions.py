# -*- coding: utf-8; -*-

import unittest

from rattail import exceptions


class TestRecipientsNotFound(unittest.TestCase):

    def test_init(self):
        self.assertRaises(TypeError, exceptions.RecipientsNotFound)
        exc = exceptions.RecipientsNotFound('testing')
        self.assertEqual(exc.key, 'testing')

    def test_unicode(self):
        exc = exceptions.RecipientsNotFound('testing')
        self.assertEqual(str(exc),
                         "No recipients found in config for 'testing' emails.  Please set "
                         "'testing.to' (or 'default.to') in the [rattail.mail] section.")
