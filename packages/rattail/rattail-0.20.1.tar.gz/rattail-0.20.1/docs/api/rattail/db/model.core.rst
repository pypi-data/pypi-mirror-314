
``rattail.db.model.core``
=========================

.. automodule:: rattail.db.model.core

.. autoclass:: ModelBase

   .. attribute:: model_title

      Optionally set this to a "humanized" version of the model name, for
      display in templates etc.  Default value will be guessed from the model
      class name, e.g. 'Product' => "Products" and 'CustomerOrder' => "Customer
      Order".

   .. attribute:: model_title_plural

      Optionally set this to a "humanized" version of the *plural* model name,
      for display in templates etc.  Default value will be guessed from the
      model class name, e.g. 'Product' => "Products" and 'CustomerOrder' =>
      "Customer Orders".

.. autoclass:: Setting
  :members:

.. autoclass:: Change
  :members:

.. automodule:: rattail.db.model.contact
  :members:

.. todo::
   Geez a lot of work left here...
