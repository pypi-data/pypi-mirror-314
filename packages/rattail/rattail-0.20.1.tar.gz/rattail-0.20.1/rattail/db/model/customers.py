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
Data Models for Customers
"""

import datetime
import warnings

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list

from rattail.db.model import (Base, uuid_column, getset_factory,
                              PhoneNumber, EmailAddress, MailingAddress,
                              Person, Note, User)
from .contact import ContactMixin


class Customer(ContactMixin, Base):
    """
    Represents a customer account.

    Customer accounts may consist of more than one person, in some cases.
    """
    __tablename__ = 'customer'
    __table_args__ = (
        sa.ForeignKeyConstraint(['account_holder_uuid'],
                                ['person.uuid'],
                                name='customer_fk_account_holder'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    id = sa.Column(sa.String(length=20), nullable=True, doc="""
    String ID for the customer, if known/relevant.  This may or may not
    correspond to the :attr:`number`, depending on your system.
    """)

    number = sa.Column(sa.Integer(), nullable=True, doc="""
    Customer number, if known/relevant.  This may or may not correspond to the
    :attr:`id`, depending on your system.
    """)

    name = sa.Column(sa.String(length=255))

    account_holder_uuid = sa.Column(sa.String(length=32), nullable=True)
    account_holder = orm.relationship(
        Person, doc="""
        Reference to the account holder (person), if applicable.
        """,
        cascade_backrefs=False,
        backref=orm.backref(
            # TODO: `customers` would be a better backref name, but
            # that is already taken for CustomerPerson relationship
            'customer_accounts', doc="""
            List of customer records for which this person is the
            account holder.
            """,
            cascade_backrefs=False))

    email_preference = sa.Column(sa.Integer())

    wholesale = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating whether the customer is a "wholesale" account - whatever
    that happens to mean for your business logic.
    """)

    active_in_pos = sa.Column(sa.Boolean(), nullable=True, doc="""
    Whether or not the customer account should be "active" within the POS
    system, if applicable.  Whether/how this field is populated and/or
    leveraged are up to your system.
    """)

    active_in_pos_sticky = sa.Column(sa.Boolean(), nullable=False, default=False, doc="""
    Whether or not the customer account should *always* be "active" within the
    POS system.  This field may be useful if :attr:`active_in_pos` gets set
    dynamically.
    """)

    invalid_address = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the customer's mailing address(es) on file are invalid.
    """)

    def __str__(self):
        return self.name or ""

    def add_email_address(self, address, type='Home'):
        email = CustomerEmailAddress(address=address, type=type)
        self.emails.append(email)
        return email

    def add_phone_number(self, number, type='Home'):
        phone = CustomerPhoneNumber(number=number, type=type)
        self.phones.append(phone)
        return phone

    def add_mailing_address(self, **kwargs):
        addr = CustomerMailingAddress(**kwargs)
        self.addresses.append(addr)
        return addr

    @property
    def employee(self):
        """
        DEPRECATED

        Return the employee associated with the customer, if any.  Assumes a
        certain "typical" relationship path.
        """
        warnings.warn("customer.employee is deprecated; "
                      "please use app.get_employee(customer) instead",
                      DeprecationWarning, stacklevel=2)
        if self.person:
            return self.person.employee

    def first_person(self):
        """
        DEPRECATED

        Convenience method to retrieve the "first" Person record which is
        associated with this customer, or ``None``.
        """
        warnings.warn("customer.first_person() is deprecated; "
                      "please use app.get_person(customer) instead",
                      DeprecationWarning, stacklevel=2)
        if self.account_holder:
            return self.account_holder
        if self.shoppers:
            return self.shoppers[0].person
        if self.people:
            return self.people[0]

    def only_person(self, require=True):
        """
        DEPRECATED

        Convenience method to retrieve the one and only Person record which is
        associated with this customer.  An error will be raised if there is not
        exactly one person associated.
        """
        warnings.warn("customer.only_person() is deprecated; "
                      "please use app.get_person(customer) instead",
                      DeprecationWarning, stacklevel=2)
        person = self.first_person()
        if require and not person:
            raise ValueError(f"customer {self.uuid} has no person")
        return person

    def only_member(self, require=True):
        """
        Convenience method to retrieve the one and only Member record which is
        associated with this customer.  If ``require=True`` then an error will
        be raised if there is not exactly one member found.
        """
        if len(self.members) > 1 or (require and not self.members):
            raise ValueError("customer {} should have 1 member but instead has {}: {}".format(
                self.uuid, len(self.members), self))
        return self.members[0] if self.members else None


class CustomerPhoneNumber(PhoneNumber):
    """
    Represents a phone (or fax) number associated with a :class:`Customer`.
    """

    __mapper_args__ = {'polymorphic_identity': 'Customer'}


Customer._contact_phone_model = CustomerPhoneNumber

Customer.phones = orm.relationship(
    CustomerPhoneNumber,
    backref='customer',
    primaryjoin=CustomerPhoneNumber.parent_uuid == Customer.uuid,
    foreign_keys=[CustomerPhoneNumber.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=CustomerPhoneNumber.preference,
    cascade='save-update, merge, delete, delete-orphan')

Customer.phone = orm.relationship(
    CustomerPhoneNumber,
    primaryjoin=sa.and_(
        CustomerPhoneNumber.parent_uuid == Customer.uuid,
        CustomerPhoneNumber.preference == 1),
    foreign_keys=[CustomerPhoneNumber.parent_uuid],
    uselist=False,
    viewonly=True)


class CustomerEmailAddress(EmailAddress):
    """
    Represents an email address associated with a :class:`Customer`.
    """

    __mapper_args__ = {'polymorphic_identity': 'Customer'}


Customer._contact_email_model = CustomerEmailAddress

Customer.emails = orm.relationship(
    CustomerEmailAddress,
    backref='customer',
    primaryjoin=CustomerEmailAddress.parent_uuid == Customer.uuid,
    foreign_keys=[CustomerEmailAddress.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=CustomerEmailAddress.preference,
    cascade='save-update, merge, delete, delete-orphan')

Customer.email = orm.relationship(
    CustomerEmailAddress,
    primaryjoin=sa.and_(
        CustomerEmailAddress.parent_uuid == Customer.uuid,
        CustomerEmailAddress.preference == 1),
    foreign_keys=[CustomerEmailAddress.parent_uuid],
    uselist=False,
    viewonly=True)


class CustomerMailingAddress(MailingAddress):
    """
    Represents a mailing address for a customer
    """
    __mapper_args__ = {'polymorphic_identity': 'Customer'}


Customer._contact_address_model = CustomerMailingAddress

Customer.addresses = orm.relationship(
    CustomerMailingAddress,
    backref='customer',
    primaryjoin=CustomerMailingAddress.parent_uuid == Customer.uuid,
    foreign_keys=[CustomerMailingAddress.parent_uuid],
    collection_class=ordering_list('preference', count_from=1),
    order_by=CustomerMailingAddress.preference,
    cascade='all, delete-orphan')

Customer.address = orm.relationship(
    CustomerMailingAddress,
    primaryjoin=sa.and_(
        CustomerMailingAddress.parent_uuid == Customer.uuid,
        CustomerMailingAddress.preference == 1),
    foreign_keys=[CustomerMailingAddress.parent_uuid],
    uselist=False,
    viewonly=True)


class CustomerNote(Note):
    """
    Represents a note attached to a customer.
    """
    __mapper_args__ = {'polymorphic_identity': 'Customer'}

    customer = orm.relationship(
        Customer,
        primaryjoin='Customer.uuid == CustomerNote.parent_uuid',
        foreign_keys='CustomerNote.parent_uuid',
        doc="""
        Reference to the customer to which this note is attached.
        """,
        backref=orm.backref(
            'notes',
            primaryjoin='CustomerNote.parent_uuid == Customer.uuid',
            foreign_keys='CustomerNote.parent_uuid',
            order_by='CustomerNote.created',
            cascade='all, delete-orphan',
            cascade_backrefs=False,
            doc="""
            Sequence of notes which belong to the customer.
            """))


class CustomerGroup(Base):
    """
    Represents an arbitrary group to which customers may belong.
    """
    __tablename__ = 'customer_group'
    __versioned__ = {}

    uuid = uuid_column()
    id = sa.Column(sa.String(length=20))
    name = sa.Column(sa.String(length=255))

    def __str__(self):
        return self.name or ''


class CustomerGroupAssignment(Base):
    """
    Represents the assignment of a customer to a group.
    """
    __tablename__ = 'customer_x_group'
    __table_args__ = (
        sa.ForeignKeyConstraint(['group_uuid'], ['customer_group.uuid'], name='customer_x_group_fk_group'),
        sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='customer_x_group_fk_customer'),
    )
    __versioned__ = {}

    uuid = uuid_column()
    customer_uuid = sa.Column(sa.String(length=32), nullable=False)
    group_uuid = sa.Column(sa.String(length=32), nullable=False)
    ordinal = sa.Column(sa.Integer(), nullable=False)

    group = orm.relationship(
        CustomerGroup,
        backref=orm.backref(
            '_customers',
            cascade='all, delete-orphan',
            cascade_backrefs=False))


Customer._groups = orm.relationship(
    CustomerGroupAssignment, backref='customer',
    collection_class=ordering_list('ordinal', count_from=1),
    order_by=CustomerGroupAssignment.ordinal,
    cascade='save-update, merge, delete, delete-orphan')

Customer.groups = association_proxy(
    '_groups', 'group',
    getset_factory=getset_factory,
    creator=lambda g: CustomerGroupAssignment(group=g))


class CustomerShopper(Base):
    """
    Represents a "shopper" on a customer account.  Most customer
    accounts will have at least one of these (shopper #1) who is the
    account holder.
    """
    __tablename__ = 'customer_shopper'
    __table_args__ = (
        sa.ForeignKeyConstraint(['customer_uuid'],
                                ['customer.uuid'],
                                name='customer_shopper_fk_customer'),
        sa.ForeignKeyConstraint(['person_uuid'],
                                ['person.uuid'],
                                name='customer_shopper_fk_person'),
        sa.UniqueConstraint('customer_uuid', 'shopper_number',
                            name='customer_shopper_uq_shopper_number'),
        sa.Index('customer_shopper_ix_customer', 'customer_uuid'),
        sa.Index('customer_shopper_ix_person', 'person_uuid'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    customer_uuid = sa.Column(sa.String(length=32), nullable=False)
    customer = orm.relationship(
        Customer, doc="""
        Reference to the customer account to which the shopper belongs.
        """,
        cascade_backrefs=False,
        backref=orm.backref(
            'shoppers', doc="""
            List of all shoppers (past and present) for the customer.
            """,
            order_by='CustomerShopper.shopper_number',
            cascade='all, delete-orphan',
            cascade_backrefs=False))

    person_uuid = sa.Column(sa.String(length=32), nullable=False)
    person = orm.relationship(
        Person,
        doc="""
        Reference to the person who "is" this shopper.
        """,
        backref=orm.backref(
            'customer_shoppers', doc="""
            List of all shopper records for this person, under various
            customer accounts.
            """,
            cascade_backrefs=False))

    shopper_number = sa.Column(sa.Integer(), nullable=False, doc="""
    Sequence number (starting with 1) for this shopper record, within
    the context of the customer account.
    """)

    active = sa.Column(sa.Boolean(), nullable=True, doc="""
    Whether this shopper record is currently active for the customer.
    """)

    def __str__(self):
        return f"#{self.shopper_number} - {self.person}"

    def get_current_history(self):
        """
        Returns the "current" history record for the shopper, if
        applicable.  Note that this history record is not necessarily
        "active" - it's just the most recent.
        """
        if self.history:
            return self.history[-1]


class CustomerShopperHistory(Base):
    """
    History records for customer shoppers.
    """
    __tablename__ = 'customer_shopper_history'
    __table_args__ = (
        sa.ForeignKeyConstraint(['shopper_uuid'],
                                ['customer_shopper.uuid'],
                                name='customer_shopper_history_fk_shopper'),
        sa.Index('customer_shopper_history_ix_shopper', 'shopper_uuid'),
    )
    __versioned__ = {}

    uuid = uuid_column()

    shopper_uuid = sa.Column(sa.String(length=32), nullable=False)
    shopper = orm.relationship(
        CustomerShopper, doc="""
        Reference to the shopper record to which this history pertains.
        """,
        cascade_backrefs=False,
        backref=orm.backref(
            'history',
            order_by='(CustomerShopperHistory.start_date, CustomerShopperHistory.end_date)',
            cascade_backrefs=False,
            doc="""
            Sequence of history records for the shopper.
            """))

    start_date = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the shopper became active for the customer.
    """)

    end_date = sa.Column(sa.Date(), nullable=True, doc="""
    Date on which the shopper became inactive, if applicable.
    """)


class CustomerPerson(Base):
    """
    Represents the association between a person and a customer account.
    """
    __tablename__ = 'customer_x_person'
    __table_args__ = (
        sa.ForeignKeyConstraint(['customer_uuid'], ['customer.uuid'], name='customer_x_person_fk_customer'),
        sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], name='customer_x_person_fk_person'),
        sa.Index('customer_x_person_ix_customer', 'customer_uuid'),
        sa.Index('customer_x_person_ix_person', 'person_uuid'),
    )
    __versioned__ = {}

    uuid = uuid_column()
    customer_uuid = sa.Column(sa.String(length=32), nullable=False)
    person_uuid = sa.Column(sa.String(length=32), nullable=False)
    ordinal = sa.Column(sa.Integer(), nullable=False)

    customer = orm.relationship(Customer, back_populates='_people')

    person = orm.relationship(Person)


Customer._people = orm.relationship(
    CustomerPerson, back_populates='customer',
    primaryjoin=CustomerPerson.customer_uuid == Customer.uuid,
    collection_class=ordering_list('ordinal', count_from=1),
    order_by=CustomerPerson.ordinal,
    cascade='save-update, merge, delete, delete-orphan')

Customer.people = association_proxy(
    '_people', 'person',
    getset_factory=getset_factory,
    creator=lambda p: CustomerPerson(person=p))

Customer._person = orm.relationship(
    CustomerPerson,
    primaryjoin=sa.and_(
        CustomerPerson.customer_uuid == Customer.uuid,
        CustomerPerson.ordinal == 1),
    uselist=False,
    viewonly=True)

Customer.person = association_proxy(
    '_person', 'person',
    getset_factory=getset_factory)

Person._customers = orm.relationship(
    CustomerPerson,
    primaryjoin=CustomerPerson.person_uuid == Person.uuid,
    viewonly=True)

Person.customers = association_proxy('_customers', 'customer',
                                     getset_factory=getset_factory,
                                     creator=lambda c: CustomerPerson(customer=c))


class PendingCustomer(Base):
    """
    A "pending" customer record, used for new customer entry workflow.
    """
    __tablename__ = 'pending_customer'
    __table_args__ = (
        sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], name='pending_customer_fk_user'),
    )

    uuid = uuid_column()

    user_uuid = sa.Column(sa.String(length=32), nullable=False)
    user = orm.relationship(
        User,
        doc="""
        Referencef to the :class:`~rattail:rattail.db.model.User` who
        first entered the record.
        """)

    created = sa.Column(sa.DateTime(), nullable=False, default=datetime.datetime.utcnow, doc="""
    Timestamp when the record was first created.
    """)

    # Customer fields
    id = sa.Column(sa.String(length=20), nullable=True)

    # Person fields
    first_name = sa.Column(sa.String(length=50), nullable=True)
    middle_name = sa.Column(sa.String(length=50), nullable=True)
    last_name = sa.Column(sa.String(length=50), nullable=True)
    display_name = sa.Column(sa.String(length=100), nullable=True)

    # Phone fields
    phone_number = sa.Column(sa.String(length=20), nullable=True)
    phone_type = sa.Column(sa.String(length=15), nullable=True)

    # Email fields
    email_address = sa.Column(sa.String(length=255), nullable=True)
    email_type = sa.Column(sa.String(length=15), nullable=True)

    # Address fields
    address_street = sa.Column(sa.String(length=100), nullable=True)
    address_street2 = sa.Column(sa.String(length=100), nullable=True)
    address_city = sa.Column(sa.String(length=60), nullable=True)
    address_state = sa.Column(sa.String(length=2), nullable=True)
    address_zipcode = sa.Column(sa.String(length=10), nullable=True)
    address_type = sa.Column(sa.String(length=15), nullable=True)

    # workflow fields
    status_code = sa.Column(sa.Integer(), nullable=True, doc="""
    Status indicator for the new customer record.
    """)

    def __str__(self):
        return self.display_name or ""
