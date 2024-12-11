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
Autocomplete Handler for Members
"""

import sqlalchemy as sa

from rattail.autocomplete import Autocompleter
from rattail.db.model import Member


class MemberAutocompleter(Autocompleter):
    """
    Autocompleter for Members (by name)
    """
    autocompleter_key = 'members'
    model_class = Member
    autocomplete_fieldname = 'name'

    def make_base_query(self, session):
        model = self.model
        return session.query(model.Member)\
                      .outerjoin(model.Customer)\
                      .outerjoin(model.Person,
                                 model.Person.uuid == model.Member.person_uuid)

    def filter_autocomplete_query(self, session, query, term):
        model = self.model

        # TODO: should also filter by Customer.name ?
        # or maybe just need a separate autocompleter for that
        column = model.Person.display_name
        criteria = [column.ilike(f'%{word}%')
                    for word in term.split()]
        return query.filter(sa.and_(*criteria))

    def autocomplete_display(self, member):
        return member.person.display_name

    def sort_autocomplete_query(self, session, query):
        model = self.model
        return query.order_by(model.Person.display_name)
