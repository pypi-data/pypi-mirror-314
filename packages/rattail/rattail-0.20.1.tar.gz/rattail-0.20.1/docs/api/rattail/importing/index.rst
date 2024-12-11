
``rattail.importing``
=====================

.. automodule:: rattail.importing

There are a handful of importers and import handlers made available within this
namespace, i.e. not just the base classes but some variations thereof etc.  You
may import each of these directly from this namespace, e.g.::

   from rattail.importing import Importer

However it's more typical to do this instead::

   from rattail import importing

That way you can reference ``importing.Importer`` as well as
``importing.model.ProductImporter`` etc.  The full list of what's available in
this ``rattail.importing`` namespace follows.

Please also see :doc:`/narr/importers` for some of the general concepts
involved here.

Importers
---------

 * :class:`rattail.importing.importers.Importer`
 * :class:`rattail.importing.importers.FromQuery`
 * :class:`rattail.importing.importers.BulkImporter`
 * :class:`rattail.importing.sqlalchemy.FromSQLAlchemy`
 * :class:`rattail.importing.sqlalchemy.ToSQLAlchemy`
 * :class:`rattail.importing.postgresql.BulkToPostgreSQL`

Import Handlers
---------------

 * :class:`rattail.importing.handlers.ImportHandler`
 * :class:`rattail.importing.handlers.BulkImportHandler`
 * :class:`rattail.importing.handlers.FromSQLAlchemyHandler`
 * :class:`rattail.importing.handlers.ToSQLAlchemyHandler`
 * :class:`rattail.importing.rattail.FromRattailHandler`
 * :class:`rattail.importing.rattail.ToRattailHandler`

Rattail Model Importers
-----------------------

This is a little different but worth a mention.  If you do::

   from rattail import importing

then you will have access to the full set of Rattail data importers (i.e. the
"local" side of an import which targets a Rattail database) via
``importing.model`` - in other words you can then do this:

.. code-block:: python

   class ProductImporter(importing.model.ProductImporter):
       """ Custom product importer. """

Of course that's only helpful if you're importing data to Rattail.  See
:mod:`rattail.importing.model` for what's available in that namespace.
