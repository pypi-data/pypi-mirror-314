# -*- coding: utf-8; -*-

from unittest import TestCase


from rattail.config import RattailConfig

try:
    import sqlalchemy as sa
    from rattail.autocomplete import employees as mod
    from rattail.db import Session
except ImportError:
    pass
else:

    class TestEmployeeAutocompleter(TestCase):

        def setUp(self):
            self.config = RattailConfig()
            self.app = self.config.get_app()
            self.autocompleter = self.make_autocompleter()

        def make_autocompleter(self):
            return mod.EmployeeAutocompleter(self.config)

        def test_autocomplete(self):
            engine = sa.create_engine('sqlite://')
            model = self.app.model
            model.Base.metadata.create_all(bind=engine)
            session = Session(bind=engine)
            enum = self.config.get_enum()

            # first create some employees
            alice = model.Person(display_name='Alice Chalmers')
            alice.employee = model.Employee(status=enum.EMPLOYEE_STATUS_CURRENT)
            session.add(alice)
            bob = model.Person(display_name='Bob Loblaw')
            bob.employee = model.Employee(status=enum.EMPLOYEE_STATUS_CURRENT)
            session.add(bob)
            charlie = model.Person(display_name='Charlie Chaplin')
            charlie.employee = model.Employee(status=enum.EMPLOYEE_STATUS_FORMER)
            session.add(charlie)

            # searching for nothing yields no results
            result = self.autocompleter.autocomplete(session, '')
            self.assertEqual(len(result), 0)

            # search for 'l' yields only 2 current employees
            result = self.autocompleter.autocomplete(session, 'l')
            self.assertEqual(len(result), 2)

            # search for 'alice' yields just Alice Chalmers
            result = self.autocompleter.autocomplete(session, 'alice')
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['value'], alice.employee.uuid)
