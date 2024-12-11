
``rattail.batch.handlers``
==========================

.. automodule:: rattail.batch.handlers

.. autofunction:: get_batch_handler

.. autoclass:: BatchHandler

   We'll try to list the various attributes and methods below, in an order
   which somewhat follows the life cycle of a batch.

   .. autoattribute:: batch_key

   .. autoattribute:: batch_model_class

   .. automethod:: consume_batch_id

   .. automethod:: make_batch

   .. automethod:: make_basic_batch

   .. automethod:: init_batch

   .. attribute:: populate_batches

      Simple flag to indicate whether any/all batches will require initial
      population from a relevant data source.  Note that this flag should be
      set to ``True`` if *any* batches may need population (its default value
      is ``False``).  Whether or not a given batch actually needs to be
      populated, is ultimately determined by the :meth:`should_populate()`
      method.

      Default value is ``False`` which means no batches will be populated.

      Set this to ``True`` and do *not* override :meth:`should_populate()` if
      you need all batches to be populated.

      Set this to ``True`` and *do* override :meth:`should_populate()` if you
      need more fine-grained control, e.g. by inspecting the given batch.

   .. automethod:: should_populate

   .. attribute:: populate_with_versioning

      This flag indicates whether it's okay for data versioning to be enabled
      during initial batch population.

      If set to ``True`` (the default), then versioning is allowed and
      therefore the caller need take no special precautions when populating
      the batch.

      If set to ``False`` then versioning is *not* allowed; if versioning is
      not enabled for the current process, the caller may populate the batch
      with no special precautions.  However if versioning *is* enabled, the
      caller must launch a separate process with versioning disabled, in order
      to populate the batch.

   .. automethod:: setup_populate

   .. automethod:: do_populate

   .. automethod:: populate

   .. automethod:: make_row

   .. automethod:: add_row

   .. automethod:: after_add_row

   .. automethod:: teardown_populate

   .. attribute:: repopulate_when_refresh

      Flag to indicate that when a batch is refreshed, the first step of that
      should be to delete all data rows for, and then re-populate the batch.
      The flag is ``False`` by default, in which case the batch is *not*
      repopulated, i.e. the refresh will work with existing batch rows.

   .. automethod:: refreshable

   .. attribute:: refresh_with_versioning

      This flag indicates whether it's okay for data versioning to be enabled
      during batch refresh.

      If set to ``True`` (the default), then versioning is allowed and
      therefore the caller need take no special precautions when populating the
      batch.

      If set to ``False`` then versioning is *not* allowed; if versioning is
      not enabled for the current process, the caller may populate the batch
      with no special precautions.  However if versioning *is* enabled, the
      caller must launch a separate process with versioning disabled, in order
      to refresh the batch.

   .. automethod:: setup_refresh

   .. automethod:: do_refresh

   .. automethod:: refresh

   .. automethod:: refresh_many

   .. automethod:: refresh_row

   .. automethod:: locate_product_for_entry

   .. automethod:: refresh_batch_status

   .. automethod:: teardown_refresh

   .. automethod:: do_remove_row

   .. automethod:: remove_row

   .. automethod:: get_effective_rows

   .. automethod:: executable

   .. automethod:: why_not_execute

   .. automethod:: auto_executable

   .. attribute:: execute_with_versioning

      This flag indicates whether it's okay for data versioning to be enabled
      during batch execution.

      If set to ``True`` (the default), then versioning is allowed and
      therefore the caller need take no special precautions when populating
      the batch.

      If set to ``False`` then versioning is *not* allowed; if versioning is
      not enabled for the current process, the caller may populate the batch
      with no special precautions.  However if versioning *is* enabled, the
      caller must launch a separate process with versioning disabled, in order
      to execute the batch.

   .. automethod:: do_execute

   .. automethod:: execute

   .. automethod:: execute_many

   .. automethod:: setup_clone

   .. automethod:: clone

   .. automethod:: teardown_clone

   .. automethod:: delete

   .. automethod:: purge_batches

   ..
      .. autoattribute:: root_datadir

      .. automethod:: datadir

      .. automethod:: make_datadir

      .. automethod:: set_input_file

      .. automethod:: clone
