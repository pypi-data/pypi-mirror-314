
.. _batches:

Data Batches
============

This document briefly outlines what comprises a batch in terms of the Rattail
database etc.


Data Model
----------

First and foremost is the data model, as each type of batch requires two tables
in which to store its data.  So two model classes must be defined, one for the
batch itself and another for its row data.  These model classes must inherit
from one of the following:

Batch proper, i.e. batch header:

* :class:`rattail.db.batch.model.BatchMixin`
* :class:`rattail.db.batch.model.FileBatchMixin`

Batch data rows:

* :class:`rattail.db.batch.model.BatchRowMixin`
* :class:`rattail.db.batch.model.ProductBatchRowMixin`

Note that all parent classes will add certain columns to your tables, though
which ones will vary by parent.  Any columns you define will be in addition to
those provided by the parent, although (I think?) specifying a duplicate name
would effectively overwrite a column.

For some implementation examples, you can see the vendor catalog batch:

* :class:`rattail.db.batch.vendorcatalog.model.VendorCatalogBatch`
* :class:`rattail.db.batch.vendorcatalog.model.VendorCatalogBatchRow`


Handler
-------

In addition to the data models, each batch type must be supported by a(t least
one) handler, which is where the logic lives for populating the batch and
executing it.  The handler class should inherit from the following:

* :class:`rattail.db.batch.handler.BatchHandler`

And here's the vendor catalog example:

* :class:`rattail.db.batch.vendorcatalog.handler.VendorCatalogHandler`


Using the Batch
---------------

Actually interacting with the batch(es) as a user implies something outside of
the scope of core Rattail.  However the Tailbone package provides some tools to
make adding support for a new batch relatively painless.  See the docs in that
package for more information.
