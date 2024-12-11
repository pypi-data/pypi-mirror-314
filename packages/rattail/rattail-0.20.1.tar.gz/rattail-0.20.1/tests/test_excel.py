# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

import os
from unittest import TestCase

import openpyxl

from rattail import excel as mod
from rattail.config import RattailConfig


class TestExcelReaderXLSX(TestCase):

    def setUp(self):
        self.config = RattailConfig()

    def test_strip_fieldnames(self):
        app = self.config.get_app()
        path = app.make_temp_file(suffix='.xlsx')

        # first make a workbook which has whitespace in column headers
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append([' first ', 'second   '])
        workbook.save(path)

        # reader should strip fieldnames by default
        reader = mod.ExcelReaderXLSX(path)
        self.assertEqual(reader.fields, ['first', 'second'])

        # unless we say not to strip them
        reader = mod.ExcelReaderXLSX(path, strip_fieldnames=False)
        self.assertEqual(reader.fields, [' first ', 'second   '])

        os.remove(path)
