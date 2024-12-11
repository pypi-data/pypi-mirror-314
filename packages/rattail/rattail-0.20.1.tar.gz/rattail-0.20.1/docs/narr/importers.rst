
.. _importers:

Data Importers
==============

Please see :doc:`rattail-manual:data/importing/index` for more
complete information about this framework.

.. note::
   The remainder of this doc is left in place for now, but content
   will eventually be moved to the :doc:`rattail-manual:index`.


"Importer" vs. "DataSync"
-------------------------

Perhaps the first thing to clear up, is that while Rattail also has a
"datasync" framework, tasked with keeping systems in sync in real-time, the
"importer" framework is tasked with a "full" sync of two systems.  In other
words "datasync" normally deals with only one (e.g. changed) "host" object at a
time, and will update the "local" system accordingly, whereas an "importer"
will examine *all* host objects and update local system accordingly.  Also,
datasync normally runs as a proper daemon, whereas an importer will normally
run either as a cron job or in response to user request via command line or web
UI, etc.

.. todo::
   Write datasync docs / link here.

To make things even more confusing, datasync can leverage an import handler /
importer(s) where possible so that the same logic is executed for both
"real-time sync" and "full sync" modes.


"Host" vs. "Local" Systems
--------------------------

From the framework's perspective, all import tasks have two "systems" involved:
one is dubbed "host" and refers to the *source* of external/new data; the other
is dubbed "local" and refers to the *target* where existing data is to be
changed.  It is important to understand what "host" and "local" refer to as you
will encounter those terms frequently in the documentation (and code).

Note that it is perfectly fine for the same "system" proper, to be used as both
host and local systems within a given importer.  Meaning, you can read some
data from one system, and then write data changes back to the same system.
This can be useful for applying business rules logic to "core" (e.g. customer)
records as an asynchronous process after they are changed normally within UI or
as part of EOD etc.  Typical use though of course is for the host and local
systems to be actually different systems.

The term "system" here doesn't imply a database or anything in particular,
really.  All that is required of a "host system" is that it be able to provide
data for the import; all required of a "local system" is that it be able to
provide "corresponding data" (i.e. for comparison, to determine if an
add/update/delete is needed) and/or be able to apply add/update/delete
operations as requested.  Therefore in practice either the "host" or "local"
systems may be a database, web API, Excel spreadsheet, flat text file, etc.

Also, the host -> local data flow is not always strictly the case, for instance
it sometimes is necessary to change the "host" system to reflect changes which
were made in the "local" system (e.g. mark a host record as exported).  The
typical scenario of course is for only the "local" system to be changed.

Since all importers have this "host -> local" pattern, on the code level it is
almost always the case that an importer will inherit from two base classes, one
for the host side and another for the local.  More on that later though.


"Importer" vs. "Import Handler"
-------------------------------

Another important distinction within the framework itself, is that of the
"importer" vs. "import handler".  Technically a single ``Importer`` contains
the logic for reading data from host, and reading/changing data on local
system, but specific to a single "data model" (e.g. products table) whereas an
``ImportHandler`` contains logic for the overall transaction
(i.e. commit/rollback).  Therefore a single *import handler* might "handle"
multiple *importers*, e.g. one for products, customers etc., so that multiple
data models might be updated within a single transaction.

Note however that even within these docs you will find the term "importer"
thrown around more often, sometimes in the generic sense meant only to refer to
the overall importer concept / framework / implementation.  Hopefully when the
distinction is important to be made within the docs, it will be.

Also note that in practice, the "handler" abstraction layer is not always
strictly necessary; for instance you might need an importer to push new
customer email addresses to an online mailing list, and it may have to use a
web API which only supports one add per call.  In other words you have only one
"data model" to update, so you don't need a handler to manage multiple
importers, and the web API doesn't support the commit/rollback approach because
each change submitted, is committed at once.  However the suggested approach is
to stick with established patterns and use a handler; various other parts of
the Rattail framework (command line, datasync) will expect one.


Making a new Importer
---------------------

Okay then, you must be serious if you made it this far...

First step of course will be to identify the "host" and "local" systems for
your particular scenario.  For the sake of a simple example here we'll assume
you wish to import product data from your "host" point of sale system (named
"MyPOS" within these docs) to your "local" Rattail system.

Note also that to make a new importer, you must have already started a project
based on Rattail; this doc will not explain that process.  The examples which
follow assume this project is named 'myapp'.

.. note::
   For now, we do have a wiki doc for `Creating a New Project`_.  Note that the
   wiki uses the name "Poser" to refer to the custom app, whereas the doc
   you're currently reading uses "myapp" for the same purpose.  Some day they
   both should use "Poser" though...

.. _Creating a New Project: https://rattailproject.org/moin/NewProject


File / Module Structure
^^^^^^^^^^^^^^^^^^^^^^^

With the host and local systems identified, you can now start writing
code...but where to put it?  Assuming you already have a Rattail-based project
with package named 'myapp' and assuming you were adding a POS->Rattail
importer, the suggestion would be to add the following files to your project:

.. code-block:: none

   myapp/
      __init__.py
      importing/
         __init__.py
         model.py
         mypos.py

This is just a suggestion really, although it is the author's personal
convention which has served him well.  Another typical scenario might be where
you wish to "export" data from Rattail->POS, in which case you might do
something like this instead:

.. code-block:: none

   myapp/
      __init__.py
      mypos/
         __init__.py
         importing/
            __init__.py
            model.py
            rattail.py

The difference may be subtle, but the intended effect is for the ``model.py``
file to contain logic which targets the "local" side of the importer, while the
"other" file (e.g. ``mypos.py`` in the first example, ``rattail.py`` in the
second) would contain logic for the "host" side of the importer.  This "other"
file is also where the import *handler* would live, since ultimately both sides
must be known for an importer to function.

The main advantage to this layout / structure is that a given ``model.py``
might be shared among various importers.  For example
``rattail.importing.model`` defines all the natively-supported importer logic
when targeting various Rattail data models on the local side.  (So technically
if you didn't need to override any of that, you wouldn't need to provide your
own ``model.py`` in the POS->Rattail scenario.)

Note that in practice the ``__init__.py`` file for an ``importing`` package
typically has (only) the following contents, for convenience:

.. code-block:: python

   from . import model



Define Import Handler
^^^^^^^^^^^^^^^^^^^^^

For the sake of a single example we'll continue to assume a POS->Rattail import
is desired.  Given the above file structure, that means the file
``myapp/importing/mypos.py`` will contain the handler.  Within that file you'll
need to add something like the following:

.. code-block:: python

   from rattail import importing
   from rattail.gpc import GPC

   from myapp.mypos.db import Session as MyPosSession, model as mypos


   class FromPosToRattail(importing.FromSQLAlchemyHandler, importing.ToRattailHandler):
       """
       Handler for MyPOS -> Rattail import.
       """
       host_title = "MyPOS"
       local_title = "Rattail"

       def make_host_session(self):
           return MyPosSession()

       def get_importers(self):
           return {
               'Department':    DepartmentImporter,
               'Vendor':        VendorImporter,
               'Product'        ProductImporter,
           }

Note that the importers (dept/vend/prod) don't exist yet; those will be defined
next, within this same file.  Also here you can again see the strong "host ->
local" patterns within the handler.

Choosing the correct base class(es) will be important.  Here, by inheriting
from ``ToRattailHandler`` we don't have to declare connection info for the
"local" (target) system because that is provided by the parent.  Similarly for
the host/source side, the ``FromSQLAlchemyHandler`` provides the bulk of logic
and all we really have to do is provide a session opened on our POS database.
Depending on your needs you may or may not find existing base classes to make
things easier on you, vs. having to code all that logic yourself (which is
still rather minimal).  Also in some cases you may only wind up needing one
base class for your handler, instead of two (which is more typical).


Define Importers
^^^^^^^^^^^^^^^^

Okay now for the fun part..right?  Keeping with our example we'll add 3 simple
importers, for department, vendor and product data coming from the POS into
Rattail.  Since we'll be targeting Rattail on the local side, we once again can
leverage existing code so all we really have to do is describe the host data.
So, within the same file to which you added the handler, do something like:

.. code-block:: python

   class FromPOS(importing.FromSQLAlchemy):
       """
       Base class for importers with MyPOS as host.
       """

   class DepartmentImporter(FromPOS, importing.model.DepartmentImporter):
       """
       Import department data from MyPOS -> Rattail.
       """
       host_model_class = mypos.Department
       key = 'number'
       supported_fields = [
           'number',
           'name',
       ]

       def normalize_host_object(self, mypos_dept):
           return {
               'number': mypos_dept.id,
               'name': mypos_dept.name.strip(),
           }


   class VendorImporter(FromPOS, importing.model.VendorImporter):
       """
       Import vendor data from MyPOS -> Rattail.
       """
       host_model_class = mypos.Vendor
       key = 'id'
       supported_fields = [
           'id',
           'name',
       ]

       def normalize_host_object(self, mypos_vend):
           return {
               'id': mypos_vend.code.strip(),
               'name': mypos_vend.name.strip(),
           }


   class ProductImporter(FromPOS, importing.model.ProductImporter):
       """
       Import product data from MyPOS -> Rattail.
       """
       host_model_class = mypos.Product
       key = 'upc'
       supported_fields = [
           'upc',
           'description',
           'size',
       ]

       def normalize_host_object(self, mypos_prod):
           return {
               'upc': GPC(mypos_prod.barcode),
               'description': mypos_prod.name.strip(),
               'size': mypos_prod.unit_size.strip(),
           }


.. todo::
   need to explain the above a bit more


Configure Command Line
^^^^^^^^^^^^^^^^^^^^^^

If is typically useful to configure a command line interface for your
new importer, for use with cron etc.

The convention is to define a subcommand, under a top-level command.
For sake of example here we'll add the ``import-mypos`` subcommand
under the top-level ``rattail`` command.

Create or edit the module at e.g. ``poser/commands.py`` and add the
subcommand::

   from rattail.commands import rattail_typer
   from rattail.commands.typer import importer_command, typer_get_runas_user
   from rattail.commands.importing import ImportCommandHandler

   @rattail_typer.command()
   @importer_command
   def import_mypos(
           ctx: typer.Context,
           **kwargs
   ):
       """
       Import data from MyPOS to Rattail
       """
       config = ctx.parent.rattail_config
       progress = ctx.parent.rattail_progress
       handler = ImportCommandHandler(
           config, import_handler_key='to_rattail.from_mypos.import')
       kwargs['user'] = typer_get_runas_user(ctx)
       handler.run(kwargs, progress=progress)

Since we are adding to the top-level ``rattail`` command, we also must
register our module so our subcommand will be discovered at runtime.
To do this add the following to your ``pyproject.toml`` file:

.. code-block:: toml

   [project.entry-points."rattail.typer_imports"]
   poser = "poser.commands"

Once your project is installed, you can run the command, e.g.:

.. code-block:: sh

   cd /srv/envs/poser
   bin/rattail import-mypos --help
