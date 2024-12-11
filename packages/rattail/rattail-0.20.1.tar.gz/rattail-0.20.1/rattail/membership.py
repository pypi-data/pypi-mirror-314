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
Membership Handler
"""

import warnings

from rattail.app import GenericHandler


class MembershipHandler(GenericHandler):
    """
    Base class and default implementation for membership handlers.
    """

    def max_one_per_person(self):
        """
        Check whether a person is allowed to have just one member
        account, or if multiple are allowed.

        :returns: Boolean; if true then only one member account is
           allowed per person; if false then multiple are allowed.
        """
        return self.config.getbool('rattail', 'members.max_one_per_person',
                                   default=False)

    def ensure_member(self, person, **kwargs):
        """
        Returns the Member record associated with the given person, creating
        it first if necessary.
        """
        member = self.get_member(person)
        if member:
            return member

        return self.make_member(person, **kwargs)

    def make_member(self, person, **kwargs):
        """
        Make and return a new Member instance.
        """
        raise NotImplementedError

    def begin_membership(self, member, **kwargs):
        """
        Begin an active membership.
        """
        raise NotImplementedError

    def get_member(self, obj):
        """
        Returns the member associated with the given person, if there is one.
        """
        model = self.model

        if isinstance(obj, model.Member):
            return obj

        elif isinstance(obj, model.Customer):
            if obj.members:
                return obj.members[0]

        else:
            person = self.app.get_person(obj)
            if person and person.members:
                return person.members[0]

    def get_members_for_account_holder(
            self,
            person,
            **kwargs
    ):
        """
        Return all Member records for which the given Person is the
        account holder.
        """
        return list(person.members)

    def get_customer(self, obj):
        """
        Returns the customer associated with the given member, if there is one.
        """
        warnings.warn("MembershipHandler.get_customer() is deprecated; "
                      "please use AppHandler.get_customer() instead")

        return self.app.get_customer(obj)

    def get_person(self, obj):
        """
        Returns the person associated with the given member, if there is one.
        """
        warnings.warn("MembershipHandler.get_person() is deprecated; "
                      "please use AppHandler.get_person() instead")

        return self.app.get_person(obj)

    def get_last_patronage_date(self, member, **kwargs):
        raise NotImplementedError

    def get_equity_full_investment_amount(self, **kwargs):
        """
        Should return the amount required for an account to become
        fully invested.
        """
        raise NotImplementedError

    def get_equity_total(self, member, cached=True, **kwargs):
        """
        Get the official equity total for the given member account.
        """
        if cached:
            return member.equity_total

        return sum([payment.amount for payment in member.equity_payments])
