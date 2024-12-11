.. _examples:

Creaty Empty Cube
-----------------

.. code-block:: python

   import wizard

   # create empty DataCube
   dc = wizard.DataCube()

   # add Data
   dc.set_cube(np.zeros(shpae=(3,4,5,)))

   print(dc)


Read Data
---------

.. code-block:: python

   import wizard

   # define path
   path_to_data = 'some/randome/path'

   # read data
   dc = wizard.read(path_to_data)

   print(dc)


Write Data
----------

.. code-block:: python

   import wizard

   # define DataCube
   a = wizard.DataCube()

   # write data
   a.write('some/output/path.csv')
