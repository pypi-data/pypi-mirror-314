
``rattail.batch.purchase``
==========================

.. automodule:: rattail.batch.purchase

.. autoclass:: PurchaseBatchHandler

   Most of the interface can be seen in the documentation for the
   :class:`~rattail.batch.handlers.BatchHandler` class.  Additional or
   overridden attributes and methods provided by this ``PurchaseBatchHandler``
   class are listed below.

   .. automethod:: after_add_row

   .. automethod:: assign_purchase_order

   .. automethod:: execute

   .. automethod:: execute_truck_dump

   .. automethod:: get_purchase_order

   .. automethod:: init_batch

   .. automethod:: make_purchase

   .. automethod:: order_row

   .. automethod:: populate

   .. automethod:: receive_purchase

   .. automethod:: receive_row

   .. automethod:: receiving_find_best_child_row

   .. automethod:: receiving_update_row_attrs

   .. automethod:: receiving_update_row_child

   .. automethod:: receiving_update_row_children

   .. automethod:: receiving_update_row_credits

   .. automethod:: refresh

   .. automethod:: refresh_batch_status

   .. automethod:: refresh_row

   .. automethod:: remove_row

   .. automethod:: should_populate

   .. automethod:: update_order_counts

   .. automethod:: update_row_cost

   .. automethod:: update_row_quantity

   .. automethod:: why_not_execute

   ..
      .. automethod:: allow_cases

      .. automethod:: allow_expired_credits

      .. automethod:: get_eligible_purchases

      .. automethod:: populate_from_truck_dump_invoice

      .. automethod:: make_row_from_invoice

      .. automethod:: quick_entry

      .. automethod:: quick_locate_product

      .. automethod:: quick_locate_rows

      .. automethod:: locate_parent_row_for_child

      .. automethod:: locate_product

      .. automethod:: remove_row

      .. automethod:: transform_pack_to_unit

      .. automethod:: can_declare_credit

      .. automethod:: declare_credit

      .. automethod:: make_credits

      .. automethod:: populate_credit

      .. automethod:: calculate_pending

      .. automethod:: auto_receive_all_items
