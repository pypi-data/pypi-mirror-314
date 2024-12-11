# -*- coding: utf-8; -*-

import os
import shutil
from unittest import TestCase

from rattail import util as mod


class A: pass
class B(A): pass
class C(B): pass

class TestGetClassHierarchy(TestCase):

    def test_basic(self):

        classes = mod.get_class_hierarchy(A)
        self.assertEqual(classes, [A])

        classes = mod.get_class_hierarchy(B)
        self.assertEqual(classes, [A, B])

        classes = mod.get_class_hierarchy(C)
        self.assertEqual(classes, [A, B, C])

        classes = mod.get_class_hierarchy(C, topfirst=False)
        self.assertEqual(classes, [C, B, A])


class ImportTests(TestCase):

    def setUp(self):
        dirname = os.path.abspath(os.path.dirname(__file__))
        os.mkdir(os.path.join(dirname, 'foo'))
        with open(os.path.join(dirname, 'foo', '__init__.py'), 'w') as f:
            f.write('\n')
        with open(os.path.join(dirname, 'foo', 'bar.py'), 'w') as f:
            f.write('\n')
        os.mkdir(os.path.join(dirname, 'foo', 'baz'))
        with open(os.path.join(dirname, 'foo', 'baz', '__init__.py'), 'w') as f:
            f.write('\n')

    def tearDown(self):
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'foo'))

    def test_module_already_imported(self):
        util_module = mod.import_module_path('rattail.util')
        self.assertTrue(util_module is mod)

    # def test_new_module(self):
    #     dirname = os.path.abspath(os.path.dirname(__file__))

    #     foo = mod.import_module_path('tests.foo')
    #     self.assertEqual(foo.__file__, os.path.abspath(
    #             os.path.join(dirname, 'foo', '__init__.py')))

    #     bar = mod.import_module_path('tests.foo.bar')
    #     self.assertEqual(bar.__file__, os.path.abspath(
    #             os.path.join(dirname, 'foo', 'bar.py')))

    #     baz = mod.import_module_path('tests.foo.baz')
    #     self.assertEqual(baz.__file__, os.path.abspath(
    #             os.path.join(dirname, 'foo', 'baz', '__init__.py')))

#     def test_load_object(self):
#         with open(os.path.join(os.path.dirname(__file__), 'foo', 'baz', '__init__.py'), 'w') as f:
#             f.write("""

# somevar = 42

# def somefunc():
#     return somevar * 10

# """)

#         somevar = mod.load_object('tests.foo.baz:somevar')
#         self.assertEqual(somevar, 42)

#         somefunc = mod.load_object('tests.foo.baz:somefunc')
#         self.assertEqual(somefunc(), 420)


class TestPrettify(TestCase):

    def test_basic(self):
        text = mod.prettify('foo_bar')
        self.assertEqual(text, "Foo Bar")
