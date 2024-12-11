
Receiving Overview
==================

Here we offer a general overview of the "product receiving" features provided
by Rattail.


Rationale
---------

The details of the receiving process can vary quite a bit for each
organization, but some patterns emerge and Rattail tries to offer tools around
these patterns.

Regardless of where your true authority lives for purchase data, Rattail should
be able to e.g. read PO data from it, and (ideally) write PO data to it as
well. (The latter especially can depend on a lot of factors of course.)

So, even if you don't use Rattail to track your purchase history "proper" the
goal for Rattail is still to provide useful workflow tools.  Of course, if you
have no other system for POs then Rattail can provide a basic home for that.

Why would you even bother with this? Especially if the system where PO data
lives already has a receiving workflow/UI, that's a good question. Short answer
is, you may not want to.  But then again it is possible that Rattail can be
leveraged to obtain a more efficient and/or flexible workflow. This can
sometimes make a big difference on labor costs as well as morale.

Objectives
----------

Short version:

#. inventory
#. credits
#. costing

The #1 objective for the receiving process - at least from Rattail's
perspective - is to accurately adjust inventory levels.  Typically this means
*incrementing* inventory for all product being received, although of course
that can vary.  But the key here is accuracy; the Rattail workflows are meant
to help avoid e.g. blindly "receiving" all product from a PO, regardless of
whether or not it was in fact physically received.

Depending on the nature of your business, sometimes product may arrive damaged,
or expired, etc.  Sometimes it doesn't arrive at all even though you were
invoiced for it, or you received the wrong product instead.  So the #2
objective, is to provide a way to deal with these exceptions, since presumably
the inventory levels should *not* be adjusted for them, but you may still want
to track them as "credits" with the vendor.

That sort of leads into #3 objective, which is named "costing" but is perhaps
aka. "accounting" - this is simply the recording of true unit costs etc.  for
each product being received, for sake of history (reporting) and/or to drive
further business logic.  For instance the receiving cost might be compared to
"expected" cost (per product master) and action taken if it's higher.  But
again the point here is accuracy; cost history is great but only if "true".


Strategy
--------

The general feature is meant to allow a user to "receive" product into a unique
batch.  Population of the batch data can happen over time, e.g. by scanning in
product.  When the batch is "complete" then it is "executed" - at which point
the inventory and/or cost data it contains is "committed" to some DB(s).

That is a simplification of the process; see :doc:`workflows` for more info.
