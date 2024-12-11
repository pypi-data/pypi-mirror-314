
``rattail.db.sess``
===================

.. automodule:: rattail.db.sess
   :members:

   .. class:: Session

      SQLAlchemy session class used for all (normal) :term:`app database`
      connections.

      This is a subclass of :class:`SessionBase`.

      See the :class:`sqlalchemy:sqlalchemy.orm.Session` docs for more
      info.

      .. note::

         WuttJamaican also provides a
         :class:`~wuttjamaican:wuttjamaican.db.sess.Session` class,
         however for now Rattail still must define/use its own.
