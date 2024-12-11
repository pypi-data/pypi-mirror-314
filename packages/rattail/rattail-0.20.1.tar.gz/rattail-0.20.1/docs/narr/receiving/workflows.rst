
Receiving Workflows
===================

Here we describe the workflows for "receiving" product, which are supported by
Rattail.  There are 2 main types, each of which has 2 sub-types:

* traditional

  * from purchase
  * from scratch

* truck dump

  * from purchases (children first)
  * from scratch (children last)


"Traditional" Receiving
-----------------------

This ("traditional") is one of two "main types" of receiving workflows, which
are supported by Rattail.  The other is "truck dump" which is described further
below.

The distinguishing feature of the "traditional" receiving workflows, is that
only one purchase / delivery is dealt with at a time.  If you need to juggle
multiple orders as if they were part of one larger unit, then you would want
the "truck dump" workflows instead.


From Purchase
^^^^^^^^^^^^^

This is generally the "most ideal" workflow, in that it's only one order at a
time (so it's relatively simple) and it implies that we *do* have purchase
order data available at time of receiving, which means the receiving process
itself can be more helpful to the user, for better accuracy and efficiency.

The life cycle of a "traditional receiving from purchase" batch usually goes
something like this:

* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.make_batch()` - empty
  batch is created according to attributes provided by user
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.do_populate()` - batch is
  initially populated from "data source" - which may vary, but should contain
  details of the original purchase order and/or final invoice; main thing is
  that it contain "order/ship quantities" of product, which we receive against
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.receive_row()` - user
  enters receiving data as they work through the physical (delivered) product
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.mark_complete()` - batch
  is marked complete, to "freeze" it until another user verifies its state etc.
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.do_execute()` - batch is
  finally executed, which may export its data to a POS and/or accounting
  system, etc.


From Scratch
^^^^^^^^^^^^

This again assumes we're dealing with only *one* purchase / delivery, but that
the purchase order / shipping details are *not* known at time of receiving.
Basically this is just what the name says, we start from scratch and add to the
batch any product we physically have received.

It perhaps goes without saying that the "costing" objective and even some types
of "credits" may not be fully supported for this batch type, since e.g. no
final invoice is available when receiving.

The life cycle of a "traditional receiving from scratch" batch usually goes
something like this:

* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.make_batch()` - empty
  batch is created according to attributes provided by user
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.receive_row()` - user
  enters receiving data as they work through the physical (delivered) product
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.mark_complete()` - batch
  is marked complete, to "freeze" it until another user verifies its state etc.
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.do_execute()` - batch is
  finally executed, which may export its data to a POS and/or accounting
  system, etc.


"Truck Dump" Receiving
----------------------

This ("truck dump") is one of two "main types" of receiving workflows, which
are supported by Rattail.  The other is "traditional" which is described above.

The distinguishing feature of the "truck dump" receiving workflows, is that
they provide a way to deal with *multiple* purchases which are delivered at the
same time, and in fact, mixed together (hence the name, truck dump).  If you
have only a single purchase / delivery, or even if there are multiple purchases
in a single delivery, but each order is clearly separated, then you probably
would want the "traditional" workflows instead.

Whereas a traditional workflow will only involve one batch, the truck dump
workflows each involve multiple batches: one "parent" batch, and two or more
"child" batches.  There is a child batch for each unique purchase order /
invoice, and they all are sort of aggregated in the parent batch, which is
where the actual receiving happens.

Note also, by default only a truck dump "parent" batch may be directly
executed.  When this happens each child batch is in turn executed; however the
user cannot directly execute a child batch.  The idea is to ensure that the
truck dump parent batch is fully "reconciled" with its children, at which point
the whole lot is assumed to be safe to execute, all at once.


From Purchases (aka. "children first")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note the plural here; this workflow assumes that you have purchase data
(i.e. order/ship quantities) for multiple orders, but need to receive the whole
lot at once, as opposed to receiving each order separately.

As with the "traditional from purchase" workflow, this is the "most ideal" of
the truck dump workflows, since we have the order data at time of receiving and
can therefore be more helpful to the user, for better accuracy and efficiency.

The "children first" moniker refers to the fact that the truck dump "child"
batches are created and attached to the parent *first*, i.e. before the actual
receiving process begins.  As these child batches are added, the parent itself
is populated with product from each child, so that receiving may then be done
against the order/ship quantities present in the parent.

The life cycle of a "truck dump receiving from purchases" batch usually goes
something like this:

* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.make_batch()` - empty
  parent batch is created according to attributes provided by user
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.add_truck_dump_child_from_invoice()` -
  child batch is created and attached to parent, using invoice file as data source
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.receive_row()` - user
  enters receiving data as they work through the physical (delivered) product
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.mark_complete()` - batch
  is marked complete, to "freeze" it until another user verifies its state etc.
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.do_execute()` - batch is
  finally executed, which may export its data to a POS and/or accounting
  system, etc.


From Scratch (aka. "children last")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This workflow assumes that you have multiple orders, but need to receive the
whole lot at once, as opposed to receiving each order separately.  It also
assumes that you do *not* have the purchase data for these orders, at time of
receiving.

However please note, this workflow *does* assume that you will have purchase
data before it's all said and done!  If you will not be able to provide
separate data for each purchase order / invoice, then there will be no way to
"split up" the truck dump parent batch, and you probably should just use the
"traditional from scratch" workflow instead.

The "children last" moniker refers to the fact that the truck dump parent batch
is created empty, then populated directly via the receiving process, and the
*last* step is to attach child batches via invoice file etc., at which point
all received product is "divvied up" among the child batches.

The life cycle of a "truck dump receiving from scratch" batch usually goes
something like this:

* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.make_batch()` - empty
  parent batch is created according to attributes provided by user
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.receive_row()` - user
  enters receiving data as they work through the physical (delivered) product
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.mark_complete()` - batch
  is marked complete, to "freeze" it until another user verifies its state etc.
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.add_truck_dump_child_from_invoice()` -
  child batch is created and attached to parent, using invoice file as data source
* :meth:`~rattail.batch.purchase.PurchaseBatchHandler.do_execute()` - batch is
  finally executed, which may export its data to a POS and/or accounting
  system, etc.
