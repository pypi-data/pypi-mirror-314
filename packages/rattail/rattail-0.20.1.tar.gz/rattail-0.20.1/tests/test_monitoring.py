# -*- coding: utf-8; -*-

import unittest
from unittest.mock import patch, Mock

from rattail import monitoring
from rattail.config import RattailConfig


class TestMonitorAction(unittest.TestCase):

    def setUp(self):
        self.config = RattailConfig()

    def test_attributes(self):
        action = monitoring.MonitorAction(self.config)
        self.assertIs(action.config, self.config)
        self.assertTrue(hasattr(action, 'app'))

    def test_not_implemented(self):
        action = monitoring.MonitorAction(self.config)
        self.assertRaises(NotImplementedError, action)


class TestCommandAction(unittest.TestCase):

    def setUp(self):
        self.config = RattailConfig()

    def test_attributes(self):
        action = monitoring.CommandAction(self.config, "echo test")
        self.assertIs(action.config, self.config)
        self.assertTrue(hasattr(action, 'app'))
        self.assertEqual(action.cmd, "echo test")

    @patch('rattail.monitoring.subprocess')
    def test_run_invokes_command(self, subprocess):
        subprocess.check_call = Mock()
        action = monitoring.CommandAction(self.config, "echo {filename}")
        action('test.txt')
        self.assertEqual(subprocess.check_call.call_count, 1)
        # nb. shell=False is a default kwarg
        subprocess.check_call.assert_called_with(['echo', 'test.txt'], shell=False)

    @patch('rattail.monitoring.subprocess')
    def test_run_with_shell(self, subprocess):
        subprocess.check_call = Mock()
        action = monitoring.CommandAction(self.config, "echo {filename}")
        action('test.txt', shell=True)
        self.assertEqual(subprocess.check_call.call_count, 1)
        subprocess.check_call.assert_called_with('echo test.txt', shell=True)
