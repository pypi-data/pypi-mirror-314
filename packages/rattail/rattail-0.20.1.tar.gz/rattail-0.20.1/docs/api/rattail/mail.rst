
``rattail.mail``
================

.. automodule:: rattail.mail

.. autoclass:: EmailHandler
   :members:

.. autofunction:: send_email

.. class:: Email

    Represents an email message, of a particular type.  Various aspects of the
    message may be defined by a subclass and/or configuration.

    :attribute key:
       Unique key for a particular type of email.  This is used to determine
       which template(s) will be used to generate the email body, as well as
       the email sender and recipients (via config/settings), etc.
