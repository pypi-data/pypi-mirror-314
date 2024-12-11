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
"Customer Mailing" report
"""

from sqlalchemy import orm

from rattail.reporting import ExcelReport


class CustomerMailing(ExcelReport):
    """
    Generates a customer mailing address list.
    """
    type_key = 'customer_mailing'
    name = "Customer Mailing"

    output_fields = [
        'first_name',
        'last_name',
        'street',
        'street2',
        'city',
        'state',
        'zipcode',
        'address_invalid',
    ]

    def make_data(self, session, params, progress=None, **kwargs):
        model = self.model

        # looking for all customers with account holder
        customers = session.query(model.Customer)\
                           .join(model.Person)\
                           .order_by(model.Person.first_name,
                                     model.Person.last_name)
        rows = []

        def add_row(customer, i):
            person = customer.account_holder
            address = customer.address or person.address
            rows.append({
                'first_name': person.first_name,
                'last_name': person.last_name,
                'street': address.street if address else None,
                'street2': address.street2 if address else None,
                'city': address.city if address else None,
                'state': address.state if address else None,
                'zipcode': address.zipcode if address else None,
                'address_invalid': address.invalid if address else None,
            })

        self.progress_loop(add_row, customers, progress,
                           message="Fetching data for report")
        return rows
