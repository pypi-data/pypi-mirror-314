# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

import os
import shutil
from unittest import TestCase

from rattail import labels as mod
from rattail.config import RattailConfig
from rattail.exceptions import LabelPrintingError


class TestLabelPrinter(TestCase):

    def setUp(self):
        self.config = RattailConfig()
        self.printer = self.make_printer()

    def make_printer(self):
        return mod.LabelPrinter(self.config)

    def test_print_labels(self):
        labels = []

        # not implemented by default
        self.assertRaises(NotImplementedError, self.printer.print_labels, labels)


class TestCommandFilePrinter(TestCase):

    def setUp(self):
        self.config = RattailConfig(defaults={
            'rattail.timezone.default': 'America/Chicago',
        })
        self.printer = self.make_printer()

    def make_printer(self):
        printer = mod.CommandFilePrinter(self.config)
        printer.formatter = mod.CommandFormatter(self.config, template="")
        return printer

    def test_print_labels(self):
        app = self.config.get_app()
        labels = []

        # output_dir is required setting
        self.assertRaises(LabelPrintingError, self.printer.print_labels, labels)

        # okay now with output_dir
        outdir = app.make_temp_dir()
        self.printer.output_dir = outdir
        path = self.printer.print_labels(labels)
        self.assertEqual(os.path.dirname(path), outdir)

        # also can override output_dir by passing it in call
        outdir2 = app.make_temp_dir()
        path2 = self.printer.print_labels(labels, output_dir=outdir2)
        self.assertEqual(os.path.dirname(path2), outdir2)

        shutil.rmtree(outdir)
        shutil.rmtree(outdir2)
