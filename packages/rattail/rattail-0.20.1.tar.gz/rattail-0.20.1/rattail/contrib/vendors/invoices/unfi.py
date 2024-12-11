# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Vendor invoice parser for United Natural Foods (UNFI)
"""

import csv
import datetime

from rattail.db import model
from rattail.gpc import GPC
from rattail.vendors.invoices import InvoiceParser


class UnfiInvoiceParser(InvoiceParser):
    """
    Parser for UNFI CSV invoice files.
    """
    key = 'rattail.contrib.unfi'
    display = "United Natural Foods (UNFI)"
    vendor_key = 'unfi'

    def open_csv_file(self, path):
        return open(path, 'rt', encoding='latin_1')

    def parse_invoice_number(self, path):
        csv_file = self.open_csv_file(path)
        reader = csv.DictReader(csv_file)
        data = next(reader)
        csv_file.close()
        return data['InvNum']

    def parse_invoice_date(self, data_path):
        csv_file = self.open_csv_file(data_path)
        reader = csv.DictReader(csv_file)
        data = next(reader)
        csv_file.close()
        return datetime.datetime.strptime(data['InvoiceDate'], '%m/%d/%Y').date()

    def parse_rows(self, data_path):
        csv_file = self.open_csv_file(data_path)

        # TODO: The following logic is largely copied from the Scan Genius
        # order parser (in `rattail_livnat.scangenius`).  I wonder if we
        # can abstract it into a generic yet custom CSV parser...?

        # We want to ignore the header section here.  However the use of
        # DictReader below requires iteration, and yet also expects
        # the "beginning" of the file to contain the fieldnames.  To force
        # this all to play nicely, we calculate our offset and then seek to
        # it explicitly.  It's probably likely that there is a better way,
        # but this works.
        offset = self.find_details_offset(csv_file)
        csv_file.seek(offset)

        reader = csv.DictReader(csv_file)
        for data in reader:

            # Only consider 'Detail' rows; this check is mostly for the
            # sake of ignoring 'Footer' rows.
            if data['RecType'] != 'Detail':
                continue

            row = model.VendorInvoiceBatchRow()
            row.item_entry = data['UPC'].replace('-', '')
            row.upc = GPC(row.item_entry)
            row.vendor_code = data['ProductID']
            row.brand_name = data['Brand']
            row.description = data['Description']
            row.size = data['Size']
            row.case_quantity = self.int_(data['Servings'])
            row.ordered_cases = int(self.decimal(data['QuantityOrdered']))
            row.shipped_cases = self.int_(data['QuantityShipped'])
            row.out_of_stock = True if data['Status'] == 'OUT' else False
            row.total_cost = self.decimal(data['ExtendedPrice'])

            # nb. UFNI total cost (ExtendedPrice) may reflect a
            # discount, whereas unit cost (NetPricePerUnit) does not.
            # so only use latter if former not available.
            if row.total_cost:
                row.case_cost = row.total_cost / row.shipped_cases
                row.unit_cost = row.case_cost / row.case_quantity
            else:
                row.unit_cost = self.decimal(data['NetPricePerUnit'])
                row.case_cost = row.unit_cost * row.case_quantity

            yield row

        csv_file.close()

    def find_details_offset(self, csv_file):
        """
        Find the character offset of the details data within a CSV file.
        """
        # TODO: The following logic is largely copied from the Scan Genius
        # order parser (in ``rattail_livnat.scangenius``).  I wonder if we can
        # abstract it into a generic yet custom CSV parser...?

        offset = 0
        for line, row in enumerate(csv_file, 1):
            offset += len(row)
            if line == 2:
                break

        # account for newline chars
        offset += 2 * (len(csv_file.newlines) - 1)

        return offset
