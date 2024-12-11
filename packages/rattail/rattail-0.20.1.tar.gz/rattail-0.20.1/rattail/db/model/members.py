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
Data Models for Members
"""

from collections import OrderedDict

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.orderinglist import ordering_list

from rattail.db.model import (
    Base, uuid_column,
    Person, Customer,
    PhoneNumber, EmailAddress, MailingAddress,
)
from .contact import ContactMixin


class MembershipType(Base):
    """
    Represents a "type" of membership.
    """
    __tablename__ = 'membership_type'
    __versioned__ = {}

    uuid = uuid_column()

    id = sa.Column(sa.String(length=20), nullable=True, doc="""
    ID string for the membership type, if known/relevant.
    """)

    number = sa.Column(sa.Integer(), nullable=True, doc="""
    Number of the membership type, if known/relevant.
    """)

    name = sa.Column(sa.String(length=100), nullable=True, doc="""
    Name of the membership type.
    """)

    def __str__(self):
        return self.name or ""


class Member(ContactMixin, Base):
    """
    Represents a "member" account.
    """
    __tablename__ = 'member'
    __table_args__ = (
        sa.ForeignKeyConstraint(['membership_type_uuid'],
                                ['membership_type.uuid'],
                                name='member_fk_membership_type'),
        sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], name='member_fk_person'),
        sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='member_fk_customer'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    id = sa.Column(sa.String(length=20), nullable=True, doc="""
    ID string for the member, if known/relevant.
    """)

    number = sa.Column(sa.Integer(), nullable=True, doc="""
    Member number, if known/relevant.  This may or may not correspond to the
    :attr:`id`, depending on your system.
    """)

    membership_type_uuid = sa.Column(sa.String(length=32), nullable=True)
    membership_type = orm.relationship(
        MembershipType,
        cascade_backrefs=False,
        doc="""
        Membership type for the account.
        """)

    person_uuid = sa.Column(sa.String(length=32), nullable=True)
    person = orm.relationship(
        Person,
        doc="""
        Reference to the Person to which this Member record pertains, if applicable.
        """,
        backref=orm.backref(
            'members',
            cascade_backrefs=False,
            doc="""
            Sequence of member records with which this person is associated.
            """),
    )

    customer_uuid = sa.Column(sa.String(length=32), nullable=True)
    customer = orm.relationship(
        Customer,
        doc="""
        Reference to the Customer to which this Member record pertains, if applicable.
        """,
        backref=orm.backref(
            'members',
            cascade_backrefs=False,
            doc="""
            Sequence of member records with which this customer is associated.
            """),
    )

    joined = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the member first joined.
    """)

    active = sa.Column(sa.Boolean(), nullable=False, default=True, doc="""
    Flag indicating whether the member account is "active" (i.e. joined and not
    yet withdrawn etc.).
    """)

    equity_current = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating whether the member account's equity is "current".
    """)

    equity_total = sa.Column(sa.Numeric(precision=5, scale=2), nullable=True, doc="""
    Current equity total for the member account.
    """)

    equity_payment_due = sa.Column(sa.Date(), nullable=True, doc="""
    Date by which the next equity payment must be made, if applicable.
    """)

    equity_last_paid = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the last equity payment was made, if applicable.
    """)

    equity_payment_credit = sa.Column(sa.Numeric(precision=5, scale=2), nullable=False, default=0, doc="""
    Current amount of equity which is treated as "credit" toward the member's
    next true (minimal) equity payment.
    """)

    withdrew = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which member withdrew, if applicable.
    """)

    invalid_address = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the member's mailing address(es) on file are invalid.
    """)

    def __str__(self):
        return str(self.person or self.customer or "")

    # TODO: deprecate / remove this
    def add_email_address(self, address, type='Home'):
        email = MemberEmailAddress(address=address, type=type)
        self.emails.append(email)

    # TODO: deprecate / remove this
    def add_phone_number(self, number, type='Home'):
        phone = MemberPhoneNumber(number=number, type=type)
        self.phones.append(phone)


class MemberPhoneNumber(PhoneNumber):
    """
    Represents a phone (or fax) number associated with a Member.
    """

    __mapper_args__ = {'polymorphic_identity': 'Member'}


Member._contact_phone_model = MemberPhoneNumber

Member.phones = orm.relationship(
    MemberPhoneNumber,
    backref='member',
    primaryjoin=MemberPhoneNumber.parent_uuid == Member.uuid,
    foreign_keys=[MemberPhoneNumber.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=MemberPhoneNumber.preference,
    cascade='save-update, merge, delete, delete-orphan')

Member.phone = orm.relationship(
    MemberPhoneNumber,
    primaryjoin=sa.and_(
        MemberPhoneNumber.parent_uuid == Member.uuid,
        MemberPhoneNumber.preference == 1),
    foreign_keys=[MemberPhoneNumber.parent_uuid],
    uselist=False,
    viewonly=True)


class MemberEmailAddress(EmailAddress):
    """
    Represents an email address associated with a :class:`Member`.
    """

    __mapper_args__ = {'polymorphic_identity': 'Member'}


Member._contact_email_model = MemberEmailAddress

Member.emails = orm.relationship(
    MemberEmailAddress,
    backref='member',
    primaryjoin=MemberEmailAddress.parent_uuid == Member.uuid,
    foreign_keys=[MemberEmailAddress.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=MemberEmailAddress.preference,
    cascade='save-update, merge, delete, delete-orphan')

Member.email = orm.relationship(
    MemberEmailAddress,
    primaryjoin=sa.and_(
        MemberEmailAddress.parent_uuid == Member.uuid,
        MemberEmailAddress.preference == 1),
    foreign_keys=[MemberEmailAddress.parent_uuid],
    uselist=False,
    viewonly=True)


class MemberMailingAddress(MailingAddress):
    """
    Represents a mailing address for a member
    """
    __mapper_args__ = {'polymorphic_identity': 'Member'}


Member._contact_address_model = MemberMailingAddress

Member.addresses = orm.relationship(
    MemberMailingAddress,
    backref='member',
    primaryjoin=MemberMailingAddress.parent_uuid == Member.uuid,
    foreign_keys=[MemberMailingAddress.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=MemberMailingAddress.preference,
    cascade='all, delete-orphan')

Member.address = orm.relationship(
    MemberMailingAddress,
    primaryjoin=sa.and_(
        MemberMailingAddress.parent_uuid == Member.uuid,
        MemberMailingAddress.preference == 1),
    foreign_keys=[MemberMailingAddress.parent_uuid],
    uselist=False,
    viewonly=True)


class MemberEquityPayment(Base):
    """
    Contains all member equity payments, from POS, manual entry etc.
    """
    __tablename__ = 'member_equity_payment'
    __table_args__ = (
        sa.ForeignKeyConstraint(['member_uuid'], ['member.uuid'],
                                name='member_equity_payment_fk_member'),
    )
    __versioned__ = {}
    model_title = "Equity Payment"

    STATUS_NORMAL               = 1
    STATUS_UNRECONCILED         = 2
    STATUS_RECONCILED           = 3
    STATUS_IGNORED              = 4

    STATUS = OrderedDict([
        (STATUS_NORMAL,         "normal"),
        (STATUS_UNRECONCILED,   "unreconciled"),
        (STATUS_RECONCILED,     "reconciled"),
        (STATUS_IGNORED,        "ignored"),
    ])

    uuid = uuid_column()

    member_uuid = sa.Column(sa.String(length=32), nullable=False)
    member = orm.relationship(
        Member, doc="""
        Reference to the member account for which the payment was taken.
        """,
        cascade_backrefs=False,
        backref=orm.backref(
            'equity_payments',
            order_by='MemberEquityPayment.received',
            cascade_backrefs=False,
            doc="""
            List of equity payments associated with this member account.
            """))

    amount = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False, doc="""
    Amount of the payment.
    """)

    received = sa.Column(sa.DateTime(), nullable=False, doc="""
    Date and time when the payment was received.
    """)

    description = sa.Column(sa.String(length=100), nullable=True, doc="""
    Text description for the payment.
    """)

    source = sa.Column(sa.String(length=50), nullable=True, doc="""
    System in which the payment first appeared, if applicable.
    """)

    transaction_identifier = sa.Column(sa.String(length=100), nullable=True, doc="""
    Human-friendly string identifying the POS transaction, if
    applicable.  This value is mostly for user reference and need not
    conform to any particular format.
    """)

    status_code = sa.Column(sa.Integer(), nullable=True, doc="""
    Numeric code indicating the status of the payment, if applicable.
    """)

    # trainwreck_txn_uuid = sa.Column(sa.String(length=32), nullable=True, doc="""
    # UUID of Trainwreck transaction, if known.

    # NB. This is *not* a true foreign key since Trainwreck is a
    # separate DB.
    # """)

    # trainwreck_item_uuid = sa.Column(sa.String(length=32), nullable=True, doc="""
    # UUID of Trainwreck line item, if known.

    # NB. This is *not* a true foreign key since Trainwreck is a
    # separate DB.
    # """)

    def __str__(self):
        return f"{self.member} for ${self.amount}"
