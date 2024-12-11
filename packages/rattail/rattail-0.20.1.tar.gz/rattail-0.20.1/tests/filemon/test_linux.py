# -*- coding: utf-8; -*-

import os
import shutil
import tempfile

import queue
from unittest import TestCase
from unittest.mock import Mock

from rattail.config import make_config
from rattail.filemon import linux
from rattail.filemon.config_ import Profile


class TestEventHandler(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.config = make_config([], extend=False)
        self.config.setdefault('rattail.filemon', 'monitor', 'foo')
        self.config.setdefault('rattail.filemon', 'foo.dirs', self.tempdir)
        self.config.setdefault('rattail.filemon', 'foo.actions', 'noop')
        self.config.setdefault('rattail.filemon', 'foo.action.noop.func', 'rattail.filemon.actions:noop')
        self.profile = Profile(self.config, u'foo')
        self.profile.queue = queue.Queue()
        self.handler = linux.EventHandler()
        self.handler.my_init(self.profile)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_file(self, fname, content):
        path = os.path.join(self.tempdir, fname)
        with open(path, 'wt') as f:
            f.write(content)
        return path

    def test_in_access_event_does_nothing(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.handler.process_IN_ACCESS(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_attrib_event_does_nothing(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.handler.process_IN_ATTRIB(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_create_event_does_nothing(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.handler.process_IN_CREATE(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_modify_event_does_nothing(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.handler.process_IN_MODIFY(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_close_write_event_queues_file_if_profile_does_not_watch_locks(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.profile.watch_locks = False
        self.handler.process_IN_CLOSE_WRITE(event)
        self.assertEqual(self.profile.queue.qsize(), 1)
        self.assertEqual(self.profile.queue.get_nowait(), os.path.join(self.tempdir, 'file'))

    def test_in_close_write_event_does_nothing_if_profile_watches_locks(self):
        event = Mock(pathname=self.write_file('file.lock', ''))
        self.profile.watch_locks = True
        self.handler.process_IN_CLOSE_WRITE(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_moved_to_event_queues_file_if_profile_does_not_watch_locks(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.profile.watch_locks = False
        self.handler.process_IN_MOVED_TO(event)
        self.assertEqual(self.profile.queue.qsize(), 1)
        self.assertEqual(self.profile.queue.get_nowait(), os.path.join(self.tempdir, 'file'))

    def test_in_moved_to_event_does_nothing_if_profile_watches_locks(self):
        event = Mock(pathname=self.write_file('file.lock', ''))
        self.profile.watch_locks = True
        self.handler.process_IN_MOVED_TO(event)
        self.assertTrue(self.profile.queue.empty())

    def test_in_delete_event_queues_file_if_profile_watches_locks(self):
        event = Mock(pathname=self.write_file('file.lock', ''))
        self.profile.watch_locks = True
        self.handler.process_IN_DELETE(event)
        self.assertEqual(self.profile.queue.qsize(), 1)
        self.assertEqual(self.profile.queue.get_nowait(), os.path.join(self.tempdir, 'file'))

    def test_in_moved_to_event_does_nothing_if_profile_does_not_watch_locks(self):
        event = Mock(pathname=self.write_file('file', ''))
        self.profile.watch_locks = False
        self.handler.process_IN_DELETE(event)
        self.assertTrue(self.profile.queue.empty())
