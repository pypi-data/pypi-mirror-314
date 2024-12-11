.. -*- coding: utf-8 -*-

Email Notifications
===================

Often it is useful to send email notifications out to certain folks when
certain things occur or are noticed within the business logic.  Rattail assumes
that you might define any number of such events for which email should be sent
out, and of course that you may want different recipients etc. for each event.
With this in mind, the following email subsystem exists.


From Code
---------

The Python code is listed before the configuration syntax, as it best
illustrates the *reasoning* behind the config syntax.  Here is a simplistic
notification example:

.. code-block:: python

   from rattail.mail import send_email

   def my_business_logic(config, yesterday_sales):
       max_sales = config.get_int('myapp', 'max_sales')
       if yesterday_sales > max_sales:
           send_email(config, 'sales_max_broken', {'sales': yesterday_sales})

Here also is the API doc for :func:`rattail.mail.send_email()`.

The point here is that ``send_email()`` should require nothing more than a
handle on the current configuration object (which should always be available in
some direct way), a "key" to distinguish the particular type of event for which
the email is being sent, and an optional dictionary to be used as template
context when rendering the email body.


Configuration
-------------

There are really three different aspects to the email configuration.

* **Meta Configuration** - transcends "types" of email notification
* **Generic Configuration** - common to all types of email notification
* **Specific Configuration** - unique to a particular type of email notification

Note that all configuration for this system will fall under the
``[rattail.mail]]`` section within your config file(s).


Meta Configuration
^^^^^^^^^^^^^^^^^^

This aspect of configuration consists of settings which have nothing to do with
the "type" of email notification involved.  Instead of listing and describing
them separately (for now), here is a config snippet which defines each::

   [rattail.mail

   smtp.server = localhost
   smtp.username = mymailuser
   smtp.password = mymailpass

   templates =
           rattail:templates/email
           myproject:templates/email

.. todo::
   Need to explain current limitations of SMTP authentication.

.. todo::
   Need to properly explain email template path setting.


Generic Configuration
^^^^^^^^^^^^^^^^^^^^^

This aspect of configuration consists of settings which may (but need not be)
overridden for any specific "type" of email notification.  That is, they
provide the default value if no specific override exists.  Again, here is a
config snippet which defines each::

   [rattail.mail]

   default.from = Rattail <rattail@example.com>

   default.to =
        "Admins <admin@example.com>"
        "Managers" <manager@example.com>"

   default.subject = [Rattail] Notification

Note that the "from" address is interpreted as a single address in all cases,
and therefore does not require quotes; same goes for the subject.  However the
"to" address *does* require quotes around each individual address within what
may (but need not be) a list.

Note also that it is generally assumed that you *will* define each of the
settings above; this makes optional all Specific Configuration (below).


Specific Configuration
^^^^^^^^^^^^^^^^^^^^^^

These are settings which override those described in Generic Configuration
(above), and are specific to a particular "type" of email notification.

Each "type" of notification must have a unique "key" by which it will be
distinguished.  This key is then leveraged within the config syntax to define
settings specific to the type.  For instance, if there is a key "foo", then
this might be valid config for the "foo" notification type::

   [rattail.mail]

   foo.from = Rattail Foo Alerts <rattail-foo@example.com>

   foo.to = "Foo Interested Parties" <foo@example.com>"

   foo.subject = [Rattail] Foo Is

It is important to note that the key ("foo" in this example) cannot be created
by way of configuration alone.  Business logic code essentially "invents" a new
type of notification any time a call to :func:`rattail.mail.send_email()` is
made; the notification type will from then on be designated by the ``key``
argument provided to that function.  Any config settings designated by a key
for which no code will attempt to send email (i.e. "made-up" keys within the
config file) will be ignored.

The key name should ideally be descriptive for humans' sake; this will also
help to ensure it is unique.  Something like "sales_max_broken" is of course
much better than "foo" in that regard.  But again, one must ultimately consult
the code to determine what key should be used for configuring which conceptual
type of notification.  The "default" key is reserved for Generic Configuration
(above).

Note also that since it is assumed you will have already provided Generic
Configuration, you need only override those settings for which the generic
value will not suffice.  For instance it is very common to override the
recipients for a specific notification, but the sender address is overridden
less often.


.. Templates
.. ---------

.. Currently there is only support for `Mako`_ templates.  It is assumed that
.. adding support for others would be trivial, but the reason for which to do so
.. has yet to present itself.

.. .. _Mako: http://www.makotemplates.org/
