# -*- coding: utf-8; -*-

import os
import shutil
import tempfile
import unittest

import lockfile

from rattail import files


class TestLockingCopy(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        self.srcdir = os.path.join(self.tempdir, 'src')
        os.makedirs(self.srcdir)

        self.dstdir = os.path.join(self.tempdir, 'dst')
        os.makedirs(self.dstdir)

        self.src_file = os.path.join(self.srcdir, 'somefile')
        with open(self.src_file, 'wt') as f:
            f.write('')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_normal_copy_succeeds(self):
        files.locking_copy(self.src_file, self.dstdir)
        dst_file = os.path.join(self.dstdir, 'somefile')
        self.assertTrue(os.path.exists(dst_file))
        self.assertTrue(os.path.isfile(dst_file))
        self.assertFalse(os.path.exists(os.path.join(self.dstdir, 'somefile.lock')))


class TestResourcePath(unittest.TestCase):

    def test_basic(self):
        path = files.resource_path('rattail:files.py')
        self.assertTrue(path.endswith('rattail/files.py'))

        self.assertEqual(files.resource_path('/tmp/foo.txt'), '/tmp/foo.txt')
