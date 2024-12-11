
Configuration
=============

Here we'll try to explain "everything" there is to know about Rattail configuration.


Overview
--------

First a word about what we mean by config in Rattail.

The basic idea is just that we need a place(s) from which options/settings may
be read, which will in turn affect the behavior of the running app(s).  (Note
that we may use "options" and/or "settings" interchangeably within
documentation.)

In general, Rattail tries not to assume anything beyond that loose structure;
for instance there are very few "required" config options/settings.  The
intention is for any app to define/use only those options it needs.

Config options/settings are stored in two places: file and database.  Due to
the nature of this storage, the values are always persisted as simple strings.
The app logic is responsible for "coercing" values to another data type
(e.g. integer, list) where necessary.


File Locations
--------------

Ideally, the path to config file(s) should always be specified, as opposed to
"default locations" being used.  This is for the sake of clarity.

Technically there is some built-in logic to discover config files at "default"
(expected) locations.  For now though, we're not going to cover that; again you
should explicitly declare your config file paths.

Therefore when you run a command on the console, just make sure to include (at
least) ``--config <PATH>`` somewhere in your arguments.  Similarly, your web
app, datasync, filemon etc. should be configured with an explicit config path.
Where these config files actually exist is entirely up to you, although there
are some common patterns you may wish to follow.

.. todo::

   Need to describe the "patterns" of config file locations/naming.


.. _config-file-inheritance:

File Inheritance
----------------

Per the above, the most typical scenario is where some Rattail software is ran,
with config file path(s) declared explicitly.  However that just gets us the
"initial" set of config files.

Each config file may "inherit" from one or more other config files.  Each of
the "parent" files from which the first inherits, will provide various config
options, but which the "first" file is free to override.  Note that this
inheritance is recursive.

For example, if config file A is the one specified via command line, but file A
"includes" file B, which in turn "includes" files C and D, then:

First the config options from C and D are read, then any in B will override,
and finally any in A will override.  The end result should be a merged set of
options from all files, with the "initial" file taking precedence since it was
specified via command line.

The general use case for this, is to let several "distinct" apps (e.g. web app,
datasync, filemon) share a common config base while each having their own
"primary" config file.  Sometimes there may be a "site-wide" config file(s) to
simplify configuration of apps on several different machines.

See :ref:`conf:rattail.config.include` for more info.


File Syntax
-----------

Config files are `INI-style`_, meaning their contents look basically like this:

.. _INI-style : https://en.wikipedia.org/wiki/INI_file

.. code-block:: ini

   [poser]
   foo = bar
   baz = 42

   [rattail]
   production = false


Note that this means, multiple "layers" of an app may easily share the same
config file, as long as each layer looked only at certain sections within the
config file.  Rattail takes advantage of this for e.g. the web app, datasync
and other layers, as well as for logging config.

Each name in square brackets (e.g. ``[rattail]``) is a "section" and there can
be (n)one or more "options" defined within each section.  We use these specific
terms ("section" and "option") because that is the terminology used by the
``ConfigParser`` in Python's standard library.


File Options vs. Database Settings
----------------------------------

The most fundamental configuration is defined by way of INI-files, as described
above.  Again we use the term "options" especially for config which comes from
files.

However if everything is setup correctly, config may also come from records
within the app's database.  The name of the table is ``settings`` and therefore
we use the term "settings" especially for config which comes from the DB.

Whether or not settings should be read from the DB, will generally depend on
what config options are present within the file(s).  The default behavior of
course is to *not* try to read settings from the DB.  But depending on certain
config file options, the app may be instructed to read all other config from
"DB first, then file" or "file first, then DB".

This means that if you configure "DB first, then file" like so:

.. code-block:: ini

   [rattail.config]
   usedb = true
   preferdb = true

   [rattail.db]
   default.url = postgresql://localhost/poser

Then you would be able to edit settings "on the fly" by writing to the DB, and
the app config would automatically get the new settings since it knows to
always check the DB first.

Note that whereas config files have "sections" and "options" the DB config is
different.  Again it uses a ``settings`` table which only has 2 columns:
``name`` and ``value``.  When consulting the config, app logic must request
both a "section" and "option" in which case where such config would "live"
within a file should be obvious.  But if you want to define this setting in the
DB, you must concatenate the "section" and "option" into a single "name".  So
the following config file chunk:

.. code-block:: ini

   [poser.whatever]
   my.setting = 1
   my.other.setting = 2

Would be added to the DB like so:

.. code-block:: sql

   insert into setting (name, value) values ('poser.whatever.my.setting', '1');
   insert into setting (name, value) values ('poser.whatever.my.other.setting', '2');


Usage in Code
-------------

There "always" should be a "global" config object within reach of your code.
This config object is created upon app startup, and is passed around
"everywhere" thereafter.  Sometimes it is available under different names, e.g.
you often can get to it via ``self.config`` but it may be somewhere else.  (In
particular it's ``self.rattail_config`` within Tailbone web views, or
``request.rattail_config`` within web templates.)

Let's start by assuming your config file includes this snippet:

.. code-block:: ini

   [poser]
   some_setting = foo
   some_flag = true
   another_flag = false
   some_integer = 42

Let's say you have a ``config`` object directly available to you.  You can use
it by "getting" various option values from it, e.g.::

   config.get('poser', 'some_setting')      # <== 'foo'
   config.get('poser', 'some_flag')         # <== 'true'
   config.getbool('poser', 'some_flag')     # <== True
   config.getbool('poser', 'another_flag')  # <== False
   config.get('poser', 'some_integer')      # <== '42'
   config.getint('poser', 'some_integer')   # <== 42

If you need to make your own config object, e.g. for a one-off script::

   from rattail.config import make_config

   # use whatever primary config file path(s) you want, and leave out the
   # versioning flag altogether if you want the config file itself to determine
   # that behavior
   config = make_config('/srv/envs/poser/app/quiet.conf',
                        versioning=False)

Please note that if you use data versioning, your config object must be created
*prior* to any of your data models being imported into the Python runtime.
This means your script probably should look something like this::

   from rattail.config import make_config

   def do_stuff(config):
       from rattail.db import Session

       app = config.get_app()
       model = app.model        # or e.g. 'from poser.db import model'

       session = Session()
       print(session.query(model.Product).count())
       session.close()

   if __name__ == '__main__':
       config = make_config('app/quiet.conf')
       do_stuff(config)


List of Options
---------------

Here we try to list all/most of the "core" config options which Rattail
software will expect / utilize.

``[rattail]`` section
^^^^^^^^^^^^^^^^^^^^^

TODO


``[rattail.config]`` section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _conf:rattail.config.include:

``include`` option
""""""""""""""""""

Tells the app config to first read options from another file(s), before
applying options from the current config file.

For example, maybe you maintain a "machine-wide" config file in ``/etc/`` and
you want to include it from within various other config files, like so:

.. code-block:: ini

   [rattail.config]
   include = /etc/rattail/rattail.conf

Note that you can specify more than one file to include, if you need:

.. code-block:: ini

   [rattail.config]
   include =
       /etc/rattail/rattail.conf
       /mnt/shared-server/rattail-site.conf


See :ref:`config-file-inheritance` for more info.
