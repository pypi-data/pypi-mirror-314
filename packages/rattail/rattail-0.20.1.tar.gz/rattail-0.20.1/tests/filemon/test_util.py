# -*- coding: utf-8; -*-

import os
import shutil
import tempfile

import queue
from unittest import TestCase

from rattail.config import make_config
from rattail.filemon import util
from rattail.filemon.config_ import Profile


class TestQueueExisting(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.config = make_config([], extend=False)
        self.config.setdefault('rattail.filemon', 'monitor', 'foo')
        self.config.setdefault('rattail.filemon', 'foo.dirs', self.tempdir)
        self.config.setdefault('rattail.filemon', 'foo.actions', 'noop')
        self.config.setdefault('rattail.filemon', 'foo.action.noop.func', 'rattail.filemon.actions:noop')
        self.profile = Profile(self.config, u'foo')
        self.profile.queue = queue.Queue()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_file(self, fname, content):
        path = os.path.join(self.tempdir, fname)
        with open(path, 'wt') as f:
            f.write(content)
        return path

    def test_nothing_queued_if_no_files_exist(self):
        util.queue_existing(self.profile, self.tempdir)
        self.assertTrue(self.profile.queue.empty())

    def test_normal_files_are_queued_but_not_folders(self):
        self.write_file('file', '')
        os.makedirs(os.path.join(self.tempdir, 'folder'))
        util.queue_existing(self.profile, self.tempdir)
        self.assertEqual(self.profile.queue.qsize(), 1)
        self.assertEqual(self.profile.queue.get_nowait(), os.path.join(self.tempdir, 'file'))
        self.assertTrue(self.profile.queue.empty())

    def test_if_profile_watches_locks_then_normal_files_are_queued_but_not_lock_files(self):
        self.profile.watch_locks = True
        self.write_file('file1.lock', '')
        self.write_file('file2', '')
        util.queue_existing(self.profile, self.tempdir)
        self.assertEqual(self.profile.queue.qsize(), 1)
        self.assertEqual(self.profile.queue.get_nowait(), os.path.join(self.tempdir, 'file2'))
        self.assertTrue(self.profile.queue.empty())
