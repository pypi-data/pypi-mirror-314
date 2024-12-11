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
Data models for sales
"""

import sqlalchemy as sa

from .core import Base, uuid_column


class Tender(Base):
    """
    Represents a tender for taking payment, or tracking thereof.
    """
    __tablename__ = 'tender'
    __versioned__ = {}

    uuid = uuid_column()

    code = sa.Column(sa.String(length=10), nullable=True, doc="""
    Unique code for the tender.
    """)

    name = sa.Column(sa.String(length=100), nullable=True, doc="""
    Common name for the tender.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Extra notes to describe the tender.
    """)

    is_cash = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating this tender represents "cash" or equivalent.  This
    is mostly used in conjunction with :attr:`allow_cash_back` to
    determine "cash back" behavior at POS.
    """)

    is_foodstamp = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating this tender represents "food stamps" or
    equivalent.  This is mostly used to calculate FS-eligible balance
    at POS.
    """)

    allow_cash_back = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the customer is allowed to "over-pay" for the
    transaction using this tender, with the intention of getting cash
    back.

    Tenders which do *not* have this flag set, are restricted such
    that the tender amount must be less than or equal to the current
    transaction balance.
    """)

    kick_drawer = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the drawer should be kicked open when a
    transaction is finalized which includes this tender.
    """)

    disabled = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the tender is disabled, and should not be used.
    """)

    def __str__(self):
        return str(self.name or '')
