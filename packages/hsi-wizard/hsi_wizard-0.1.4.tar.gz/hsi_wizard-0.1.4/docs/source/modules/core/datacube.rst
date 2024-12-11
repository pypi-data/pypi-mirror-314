.. _datacube:

DataCube
--------
.. module:: datacube
   :platform: Unix
   :synopsis: DataCube class for storing hyperspectral imaging (HSI) data.

Module Overview
***************
This module provides the `DataCube` class, which is designed to store and manage hyperspectral imaging (HSI) data. The `DataCube` is represented as a 3D array, where the `x` and `y` axes represent spatial dimensions (pixels), and the `v` axis represents values like spectral counts, channels, or wavelengths.

The `DataCube` class offers methods for manipulating and interacting with hyperspectral data, including arithmetic operations between cubes, data access, and wavelength management. Additionally, the class can track method executions and save them as reusable templates


Class
*****

.. autoclass:: wizard.DataCube

Methods
*******
The `DataCube` class comes with serval base methods.


- `__add__`: Adds two `DataCube` instances by concatenating along the `v` axis.
- `__getitem__`: Retrieves a specific slice of the cube.
- `__setitem__`: Sets values in the cube.
- `set_wavelengths`: Assigns wavelength data.
- `set_cube`: Updates the cube with new data and validates its shape.
- `start_recording` and `stop_recording`: Controls method execution tracking.
- `save_template` and `execute_template`: Saves and loads method execution templates in YAML format.

Additionl methods for processing the `DataCube` gets automaticlly added from the :ref:'DataCube Operations <datacube_ops>'.


