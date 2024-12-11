# -*- coding: utf-8; -*-

import os
from unittest import TestCase

from rattail import mail
from rattail.config import RattailConfig


class TestEmail(TestCase):

    def test_template_lookup_paths(self):

        # default paths
        config = RattailConfig()
        email = mail.Email(config, 'testing')
        self.assertEqual(len(email.html_templates.directories), 1)
        path = email.html_templates.directories[0]
        self.assertTrue(path.endswith(os.path.join('rattail', 'templates', 'mail')))
        
        # config may specify paths
        config = RattailConfig()
        config.setdefault('rattail.mail', 'templates', '/tmp/foo /tmp/bar')
        email = mail.Email(config, 'testing')
        self.assertEqual(email.html_templates.directories, ['/tmp/foo', '/tmp/bar'])
