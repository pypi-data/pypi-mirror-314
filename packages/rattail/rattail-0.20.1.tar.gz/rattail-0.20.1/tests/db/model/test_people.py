# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import Mock

try:
    from rattail.db import model
    from rattail.db.model import people
    from ... import DataTestCase
except ImportError:
    pass
else:

    class TestPerson(DataTestCase):

        def test_str(self):
            person = model.Person()
            self.assertEqual(str(person), "(NO NAME!)")

            person = model.Person(display_name="Fred Flintstone")
            self.assertEqual(str(person), "Fred Flintstone")

            person = model.Person(first_name="Barney", last_name="Rubble")
            self.assertEqual(str(person), "Barney Rubble")

        # TODO: this is duplicated in TestPerson
        def test_add_email_address(self):
            person = model.Person()
            self.assertEqual(len(person.emails), 0)
            person.add_email_address('fred@mailinator.com')
            self.assertEqual(len(person.emails), 1)
            email = person.emails[0]
            self.assertEqual(email.type, 'Home')

            person = model.Person()
            self.assertEqual(len(person.emails), 0)
            person.add_email_address('fred@mailinator.com', type='Work')
            self.assertEqual(len(person.emails), 1)
            email = person.emails[0]
            self.assertEqual(email.type, 'Work')

        # TODO: this is duplicated in TestPerson
        def test_add_phone_number(self):
            person = model.Person()
            self.assertEqual(len(person.phones), 0)
            person.add_phone_number('417-555-1234')
            self.assertEqual(len(person.phones), 1)
            phone = person.phones[0]
            self.assertEqual(phone.type, 'Home')

            person = model.Person()
            self.assertEqual(len(person.phones), 0)
            person.add_phone_number('417-555-1234', type='Work')
            self.assertEqual(len(person.phones), 1)
            phone = person.phones[0]
            self.assertEqual(phone.type, 'Work')


    # TODO: deprecate/remove this?
    class TestFunctions(TestCase):

        def test_get_person_display_name(self):
            name = people.get_person_display_name("Fred", "Flintstone")
            self.assertEqual(name, "Fred Flintstone")

        def test_get_person_display_name_from_context(self):
            context = Mock(current_parameters={'first_name': "Fred", 'last_name': "Flintstone"})
            name = people.get_person_display_name_from_context(context)
            self.assertEqual(name, "Fred Flintstone")
