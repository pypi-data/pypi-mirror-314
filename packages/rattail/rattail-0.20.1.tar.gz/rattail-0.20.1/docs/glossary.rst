.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   app
     As the term is used within Rattail Project documentation, this usually
     refers to a custom software application, built using Rattail, which runs
     on a server somewhere.  Such an app may often be referred to with the name
     :term:`Poser`, within the docs.  An app may or may not be a :term:`web
     app` for instance.  Of course, "app" may also refer to *any* software
     application.

   web app
     An :term:`app` which runs in a web browser, from the user's perspective.

   app model
     The overall collection of :term:`models<model>` for the
     :term:`app`.  This is implemented as a Python module, which
     contains all the model classes in its namespace.

   app node
     A specific instance of an :term:`app` which is part of a broader
     (i.e. multi-node) :term:`system`.

   model
     Depending on context, this generally refers to a data table which
     is mapped to a class via the SQLAlchemy ORM.  But it can also
     refer to the overall collection of such models (e.g. the
     :term:`app model`).

   model title
     Singular title string for a given :term:`model` (e.g. "Product").
     See also :term:`plural model title`.

   plural model title
     Plural title string for a given :term:`model` (e.g. "Products").
     See also :term:`model title`.

   system
     This is mostly used generically, to represent various software
     applications and/or devices etc. with which the :term:`app` must interact.
     However sometimes the app itself may be referred to as a system, for
     instance.

   Poser
     The "stand-in" name for a custom :term:`app` built using Rattail.  No
     actual app should ever be named Poser!  When you see the name Poser, you
     should mentally and literally replace it with whatever *other* name you
     chose to give your app.

   batch
     Can generally be thought of as a temporary or "workspace" table, with data
     which came from some source or other, and which the user may review and/or
     manipulate, before ultimately "executing" it, which in turn will update
     data within various systems, as appropriate.  Note that the term "batch"
     primarily refers to the data itself, or the model instance representing
     it; see :term:`batch handler` for the logic part.

     .. seealso::

        :ref:`batches`

   batch handler
     Class or instance thereof, responsible for the "handling" logic for a
     certain type of :term:`batch`.  Generally each type of batch will have at
     least one "default" handler available, though more are possible.  The
     batch handler knows how to populate, refresh and execute batches.

   importer
     Class or instance thereof, which contains logic for the import/export of
     data for *one specific model*, from one system to another.  Note the
     difference between an importer and an :term:`import handler`.  Whereas the
     handler is responsible for the overall "transaction" between the two
     systems, the importer is responsible only for a single table,
     conceptually.  In casual discussion, the term "importer" may sometimes be
     thrown around a bit more loosely, and e.g. refer to the system-level
     processes.  But within the code proper, the term "importer" always will
     imply a particular data model association.

     .. seealso::

        :ref:`importers`

   import handler
     Class or instance thereof, responsible for the "handling" logic for an
     overall import/export from one system to another.  Primarily this is
     concerned with the "transaction" (e.g. database connections) and
     rollback/commit for the systems involved, where applicable.  Each handler
     will contain at least one :term:`importer` although most have more.

   daemon
     A software :term:`app` or part thereof, which runs continually in the
     background.  Examples are :term:`datasync` and a :term:`web app`.

   datasync
     Refers to a particular :term:`daemon` whose responsibility is to "watch"
     various systems for data changes, and when any are found, cause various
     other systems to "consume" those changes.  This is a configurable,
     multi-threaded app which spawns a separate thread for each :term:`datasync
     watcher`, as well as a separate thread for each :term:`datasync consumer`
     (per watcher).

   datasync watcher
     Class or instance thereof, responsible for "watching" a particular system
     for data changes, within the :term:`datasync` daemon.  May also refer to
     the specific thread spawned by the daemon to run the watcher logic.
     Changes found by the watcher are then processed by at least one
     :term:`datasync consumer`.

   datasync consumer
     Class or instance thereof, responsible for "consuming" changes from a
     "watched" system within the :term:`datasync` daemon.  Any change coming
     from a :term:`datasync watcher` is (potentially) then consumed by one or
     more other systems; each of which will use a separate consumer.  May also
     refer to the specific thread spawned by the daemon to run the consumer
     logic.
