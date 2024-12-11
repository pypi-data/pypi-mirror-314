# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
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
Data Models for Vendors
"""

import warnings

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from .core import Base, uuid_column, getset_factory
from .contact import PhoneNumber, EmailAddress
from .people import Person


class Vendor(Base):
    """
    Represents a vendor from which products are purchased by the store.
    """
    __tablename__ = 'vendor'
    __table_args__ = (
        sa.UniqueConstraint('id', name='vendor_uq_id'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    id = sa.Column(sa.String(length=15), nullable=True, doc="""
    "Official" string ID for the vendor.  It is assumed / hoped that this will
    be shared across systems where possible.
    """)

    abbreviation = sa.Column(sa.String(length=20), nullable=True, doc="""
    Abbreviation for the vendor.  Whereas presumably the :attr:`id` would never
    change, this abbreviation is expected to (possibly) change over time.
    """)

    name = sa.Column(sa.String(length=50), nullable=True)
    special_discount = sa.Column(sa.Numeric(precision=5, scale=3))

    lead_time_days = sa.Column(sa.Numeric(precision=5, scale=1), nullable=True, doc="""
    The number of days expected to elapse between the order generation and receipt
    of goods.  (This description is borrowed from the SIL standard.)
    """)

    order_interval_days = sa.Column(sa.Numeric(precision=5, scale=1), nullable=True, doc="""
    The number of days expected to elapse between repeated order placement.  (This
    description is borrowed from the SIL standard.)
    """)

    terms = sa.Column(sa.String(length=100), nullable=True, doc="""
    Payment terms for the vendor, if applicable.
    """)

    def __str__(self):
        return self.name or ''

    @property
    def fax_number(self):
        for phone in self.phones:
            if 'fax' in (phone.type or '').lower():
                return phone.number

    def add_email_address(self, address, type='Info'):
        email = VendorEmailAddress(address=address, type=type)
        self.emails.append(email)

    def add_phone_number(self, number, type='Voice'):
        phone = VendorPhoneNumber(number=number, type=type)
        self.phones.append(phone)

    def get_email(self, type_='Info'):
        warnings.warn("vendor.get_email() is deprecated; please "
                      "use app.get_contact_email(vendor) instead",
                      DeprecationWarning, stacklevel=2)
        for email in self.emails:
            if email.type == type_:
                return email

    def get_email_address(self, *args, **kwargs):
        warnings.warn("vendor.get_email_address() is deprecated; please "
                      "use app.get_contact_email_address(vendor) instead",
                      DeprecationWarning, stacklevel=2)
        email = self.get_email(*args, **kwargs)
        if email:
            return email.address

    
class VendorPhoneNumber(PhoneNumber):
    """
    Represents a phone (or fax) number associated with a vendor.
    """

    __mapper_args__ = {'polymorphic_identity': 'Vendor'}


Vendor.phones = orm.relationship(
    VendorPhoneNumber,
    backref='vendor',
    primaryjoin=VendorPhoneNumber.parent_uuid == Vendor.uuid,
    foreign_keys=[VendorPhoneNumber.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=VendorPhoneNumber.preference,
    cascade='save-update, merge, delete, delete-orphan')

Vendor.phone = orm.relationship(
    VendorPhoneNumber,
    primaryjoin=sa.and_(
        VendorPhoneNumber.parent_uuid == Vendor.uuid,
        VendorPhoneNumber.preference == 1),
    foreign_keys=[VendorPhoneNumber.parent_uuid],
    uselist=False,
    viewonly=True)


class VendorEmailAddress(EmailAddress):
    """
    Represents an email address associated with a vendor.
    """

    __mapper_args__ = {'polymorphic_identity': 'Vendor'}


Vendor.emails = orm.relationship(
    VendorEmailAddress,
    backref='vendor',
    primaryjoin=VendorEmailAddress.parent_uuid == Vendor.uuid,
    foreign_keys=[VendorEmailAddress.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=VendorEmailAddress.preference,
    cascade='save-update, merge, delete, delete-orphan')

Vendor.email = orm.relationship(
    VendorEmailAddress,
    primaryjoin=sa.and_(
        VendorEmailAddress.parent_uuid == Vendor.uuid,
        VendorEmailAddress.preference == 1),
    foreign_keys=[VendorEmailAddress.parent_uuid],
    uselist=False,
    viewonly=True)


class VendorContact(Base):
    """
    Represents a point of contact (e.g. salesperson) for a vendor.
    """
    __tablename__ = 'vendor_contact'
    __table_args__ = (
        sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'], name='vendor_contact_fk_vendor'),
        sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], name='vendor_contact_fk_person'),
    )
    __versioned__ = {}

    uuid = uuid_column()
    vendor_uuid = sa.Column(sa.String(length=32), nullable=False)
    person_uuid = sa.Column(sa.String(length=32), nullable=False)
    preference = sa.Column(sa.Integer(), nullable=False)

    person = orm.relationship(
        Person,
        backref=orm.backref(
            '_vendor_contacts',
            cascade='all, delete-orphan',
            cascade_backrefs=False))

    def __str__(self):
        return str(self.person)


Vendor._contacts = orm.relationship(
    VendorContact, backref='vendor',
    collection_class=ordering_list('preference', count_from=1),
    order_by=VendorContact.preference,
    cascade='save-update, merge, delete, delete-orphan')

Vendor.contacts = association_proxy(
    '_contacts', 'person',
    getset_factory=getset_factory,
    creator=lambda p: VendorContact(person=p))

Vendor._contact = orm.relationship(
    VendorContact,
    primaryjoin=sa.and_(
        VendorContact.vendor_uuid == Vendor.uuid,
        VendorContact.preference == 1),
    uselist=False,
    viewonly=True)

Vendor.contact = association_proxy(
    '_contact', 'person',
    getset_factory=getset_factory)


class VendorSampleFile(Base):
    """
    Contains a vendor sample file, e.g. catalog or invoice.
    """
    __tablename__ = 'vendor_sample_file'
    __table_args__ = (
        sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'],
                                name='vendor_sample_file_fk_vendor'),
        sa.ForeignKeyConstraint(['created_by_uuid'], ['user.uuid'],
                                name='vendor_sample_file_fk_user'),
    )
    __versioned__ = {
        'exclude': ['bytes'],
    }
    model_title = "Vendor Sample File"
    model_title_plural = "Vendor Sample Files"

    uuid = uuid_column()

    vendor_uuid = sa.Column(sa.String(length=32), nullable=True)
    vendor = orm.relationship(
        'Vendor',
        doc="""
        Reference to the vendor associated with the sample file (if any).
        """)

    file_type = sa.Column(sa.String(length=100), nullable=False, doc="""
    Type of file this is, e.g. catalog or invoice.
    """)

    filename = sa.Column(sa.String(length=100), nullable=False, doc="""
    Name of the file.
    """)

    bytes = sa.Column(sa.LargeBinary(), nullable=False, doc="""
    Raw bytes for the file.
    """)

    effective_date = sa.Column(sa.Date(), nullable=True, doc="""
    When the sample file becomes relevant, if applicable.
    """)

    notes = sa.Column(sa.Text(), nullable=True, doc="""
    Arbitrary notes pertaining to the file.
    """)

    created_by_uuid = sa.Column(sa.String(length=32), nullable=False)
    created_by = orm.relationship(
        'User',
        doc="""
        Reference to the user who created the record.
        """)

    def __str__(self):
        return self.filename or ""
