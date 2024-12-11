# -*- coding: utf-8; -*-

import os
import shutil
import tempfile
from unittest import TestCase

from rattail.config import make_config
from rattail.filemon import config_ as config
from rattail.filemon import Action
from rattail.exceptions import ConfigurationError


class TestProfile(TestCase):

    def setUp(self):
        self.config = make_config([], extend=False)
        self.config.setdefault('rattail.filemon', 'foo.actions', 'bar')

    def test_empty_config_means_empty_profile(self):
        profile = config.Profile(self.config, u'nonexistent_key')
        self.assertEqual(len(profile.dirs), 0)
        self.assertFalse(profile.watch_locks)
        self.assertTrue(profile.process_existing)
        self.assertFalse(profile.stop_on_error)
        self.assertEqual(len(profile.actions), 0)

    def test_action_must_specify_callable(self):
        self.assertRaises(ConfigurationError, config.Profile, self.config, u'foo')

    def test_action_must_not_specify_both_func_and_class_callables(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.class', 'baz')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'baz')
        self.assertRaises(ConfigurationError, config.Profile, self.config, u'foo')

    def test_action_with_func_callable(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'os:remove')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(action.spec, u'os:remove')
        self.assertTrue(action.action is os.remove)

    def test_action_with_class_callable(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.class', 'rattail.filemon:Action')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(action.spec, u'rattail.filemon:Action')
        self.assertTrue(isinstance(action.action, Action))

    def test_action_with_args(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'shutil:move')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.args', '/dev/null')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(len(action.args), 1)
        self.assertEqual(action.args[0], u'/dev/null')

    def test_action_with_kwargs(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'rattail.filemon.actions:raise_exception')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.kwarg.message', "Hello World")
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(len(action.kwargs), 1)
        self.assertEqual(action.kwargs[u'message'], u"Hello World")

    def test_action_with_default_retry(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'rattail.filemon.actions:noop')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(action.retry_attempts, 1)
        self.assertEqual(action.retry_delay, 0)

    def test_action_with_valid_configured_retry(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'rattail.filemon.actions:noop')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.retry_attempts', '42')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.retry_delay', '100')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(action.retry_attempts, 42)
        self.assertEqual(action.retry_delay, 100)

    def test_action_with_invalid_configured_retry(self):
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'rattail.filemon.actions:noop')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.retry_attempts', '-1')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.retry_delay', '-1')
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        action = profile.actions[0]
        self.assertEqual(action.retry_attempts, 1)
        self.assertEqual(action.retry_delay, 0)

    def test_normalize_dirs(self):
        tempdir = tempfile.mkdtemp()
        dir1 = os.path.join(tempdir, 'dir1')
        os.makedirs(dir1)
        # dir2 will be pruned due to its not existing
        dir2 = os.path.join(tempdir, 'dir2')
        # file1 will be pruned due to its not being a directory
        file1 = os.path.join(tempdir, 'file1')
        with open(file1, 'wt') as f:
            f.write('')
        self.config.setdefault('rattail.filemon', 'foo.action.bar.func', 'os:remove')
        self.config.setdefault('rattail.filemon', 'foo.dirs', ' '.join(['"{0}"'.format(d) for d in [dir1, dir2, file1]]))
        profile = config.Profile(self.config, u'foo')
        self.assertEqual(len(profile.dirs), 1)
        self.assertEqual(profile.dirs[0], dir1)
        shutil.rmtree(tempdir)


class TestLoadProfiles(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.config = self.make_config()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def make_config(self, monitor=True, foo_dirs=True, foo_actions=True,
                    bar_dirs=True, bar_actions=True):
        cfg = make_config([], extend=False)
        if monitor:
            cfg.setdefault('rattail.filemon', 'monitor', 'foo, bar')
        if foo_dirs:
            cfg.setdefault('rattail.filemon', 'foo.dirs', '"{0}"'.format(self.tempdir))
        if foo_actions:
            cfg.setdefault('rattail.filemon', 'foo.actions', 'delete')
        cfg.setdefault('rattail.filemon', 'foo.action.delete.func', 'os:remove')
        if bar_dirs:
            cfg.setdefault('rattail.filemon', 'bar.dirs', '"{0}"'.format(self.tempdir))
        if bar_actions:
            cfg.setdefault('rattail.filemon', 'bar.actions', 'delete')
        cfg.setdefault('rattail.filemon', 'bar.action.delete.func', 'os:remove')
        return cfg

    def test_returns_all_profiles_specified_in_monitor_option(self):
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 2)

        # leave profiles intact but replace monitor option with one key only
        self.config = self.make_config(monitor=False)
        self.config.setdefault('rattail.filemon', 'monitor', 'foo')
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 1)

    def test_monitor_option_must_be_specified(self):
        self.config = self.make_config(monitor=False)
        self.assertRaises(ConfigurationError, config.load_profiles, self.config)

    def test_profiles_which_define_no_watched_folders_are_pruned(self):
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 2)
        # remove foo's watched folder(s)
        self.config = self.make_config(foo_dirs=False)
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 1)

    def test_profiles_which_define_no_actions_are_pruned(self):
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 2)
        # remove foo's actions
        self.config = self.make_config(foo_actions=False)
        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 1)

    def test_fallback_to_legacy_mode(self):

        # replace 'monitor' option with 'monitored' and update profiles accordingly
        # TODO: This seems hacky.
        self.config = self.make_config(monitor=False, foo_dirs=False, foo_actions=False,
                                       bar_dirs=False, bar_actions=False)
        self.config.setdefault('rattail.filemon', 'monitored', 'foo,bar')

        self.config.setdefault('rattail.filemon', 'foo.dirs', "['{0}']".format(self.tempdir))
        self.config.setdefault('rattail.filemon', 'foo.actions', "['os:remove']")
        self.config.setdefault('rattail.filemon', 'bar.dirs', "['{0}']".format(self.tempdir))
        self.config.setdefault('rattail.filemon', 'bar.actions', "['os:remove']")

        # self.config.setdefault('rattail.filemon', 'foo.dirs', "['{0}']".format(self.tempdir))
        # self.config.setdefault('rattail.filemon', 'foo.actions', 'delete')
        # self.config.setdefault('rattail.filemon', 'foo.action.delete.func', "['os:remove']")
        # self.config.setdefault('rattail.filemon', 'bar.dirs', "['{0}']".format(self.tempdir))
        # self.config.setdefault('rattail.filemon', 'bar.actions', 'delete')
        # self.config.setdefault('rattail.filemon', 'bar.action.delete.func', "['os:remove']")

        monitored = config.load_profiles(self.config)
        self.assertEqual(len(monitored), 2)
        profiles = list(monitored.values())
        self.assertTrue(isinstance(profiles[0], config.LegacyProfile))
        self.assertTrue(isinstance(profiles[1], config.LegacyProfile))


class TestLegacyProfile(TestCase):

    def setUp(self):
        self.config = make_config([], extend=False)

    def test_empty_config_means_empty_profile(self):
        profile = config.LegacyProfile(self.config, u'nonexistent_key')
        self.assertEqual(len(profile.dirs), 0)
        self.assertFalse(profile.watch_locks)
        self.assertTrue(profile.process_existing)
        self.assertFalse(profile.stop_on_error)
        self.assertEqual(len(profile.actions), 0)

    def test_action_with_spec_only(self):
        self.config.setdefault('rattail.filemon', 'foo.actions', "['os:remove']")
        profile = config.LegacyProfile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        spec, action, args, kwargs = profile.actions[0]
        self.assertEqual(spec, u'os:remove')
        self.assertTrue(action is os.remove)

    def test_action_with_spec_and_args(self):
        self.config.setdefault('rattail.filemon', 'foo.actions', "[('shutil:move', u'/dev/null')]")
        profile = config.LegacyProfile(self.config, u'foo')
        self.assertEqual(len(profile.actions), 1)
        spec, action, args, kwargs = profile.actions[0]
        self.assertEqual(spec, u'shutil:move')
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], u'/dev/null')

    def test_normalize_dirs(self):
        tempdir = tempfile.mkdtemp()
        dir1 = os.path.join(tempdir, 'dir1')
        os.makedirs(dir1)
        # dir2 will be pruned due to its not existing
        dir2 = os.path.join(tempdir, 'dir2')
        # file1 will be pruned due to its not being a directory
        file1 = os.path.join(tempdir, 'file1')
        with open(file1, 'wt') as f:
            f.write('')
        self.config.setdefault('rattail.filemon', 'foo.dirs',
                               "[{0}]".format(', '.join(["'{0}'".format(d) for d in [dir1, dir2, file1]])))
        profile = config.LegacyProfile(self.config, u'foo')
        self.assertEqual(len(profile.dirs), 1)
        self.assertEqual(profile.dirs[0], dir1)
        shutil.rmtree(tempdir)


class TestLoadLegacyProfiles(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.config = self.make_config()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def make_config(self, monitored=True, foo_dirs=True, foo_actions=True):
        cfg = make_config([], extend=False)
        if monitored:
            cfg.setdefault('rattail.filemon', 'monitored', 'foo, bar')
        if foo_dirs:
            cfg.setdefault('rattail.filemon', 'foo.dirs', "['{0}']".format(self.tempdir))
        if foo_actions:
            cfg.setdefault('rattail.filemon', 'foo.actions', "['os:remove']")
        cfg.setdefault('rattail.filemon', 'bar.dirs', "['{0}']".format(self.tempdir))
        cfg.setdefault('rattail.filemon', 'bar.actions', "['os:remove']")
        return cfg

    def test_returns_all_profiles_specified_in_monitor_option(self):

        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 2)

        # leave profiles intact but replace monitored option with one key only
        self.config = self.make_config(monitored=False)
        self.config.setdefault('rattail.filemon', 'monitored', 'foo')
        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 1)

    def test_monitor_option_must_be_specified(self):
        self.config = self.make_config(monitored=False)
        self.assertRaises(ConfigurationError, config.load_legacy_profiles, self.config)

    def test_profiles_which_define_no_watched_folders_are_pruned(self):
        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 2)

        # remove foo's watched folder(s)
        self.config = self.make_config(foo_dirs=False)
        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 1)

    def test_profiles_which_define_no_actions_are_pruned(self):
        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 2)

        # remove foo's actions
        self.config = self.make_config(foo_actions=False)
        monitored = config.load_legacy_profiles(self.config)
        self.assertEqual(len(monitored), 1)
