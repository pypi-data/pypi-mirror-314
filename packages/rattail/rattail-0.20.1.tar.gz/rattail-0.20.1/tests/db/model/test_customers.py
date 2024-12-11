# -*- coding: utf-8; -*-

try:
    from rattail.db import model
    from ... import DataTestCase
except ImportError:
    pass
else:

    class TestCustomer(DataTestCase):

        # TODO: this is duplicated in TestPerson
        def test_add_email_address(self):
            customer = model.Customer()
            self.assertEqual(len(customer.emails), 0)
            customer.add_email_address('fred@mailinator.com')
            self.assertEqual(len(customer.emails), 1)
            email = customer.emails[0]
            self.assertEqual(email.type, 'Home')

            customer = model.Customer()
            self.assertEqual(len(customer.emails), 0)
            customer.add_email_address('fred@mailinator.com', type='Work')
            self.assertEqual(len(customer.emails), 1)
            email = customer.emails[0]
            self.assertEqual(email.type, 'Work')

        # TODO: this is duplicated in TestPerson
        def test_add_phone_number(self):
            customer = model.Customer()
            self.assertEqual(len(customer.phones), 0)
            customer.add_phone_number('417-555-1234')
            self.assertEqual(len(customer.phones), 1)
            phone = customer.phones[0]
            self.assertEqual(phone.type, 'Home')

            customer = model.Customer()
            self.assertEqual(len(customer.phones), 0)
            customer.add_phone_number('417-555-1234', type='Work')
            self.assertEqual(len(customer.phones), 1)
            phone = customer.phones[0]
            self.assertEqual(phone.type, 'Work')
