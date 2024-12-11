"""
_utils/_loader/csv.py
=======================

.. module:: csv
   :platform: Unix
   :synopsis: Provides reader and writer functions for CSV files.

Module Overview
---------------

This module includes functions for reading and writing `.csv` files.

Functions
---------

.. autofunction:: _read_csv

"""

import csv

from ..._core import DataCube
from ._helper import to_cube


def _read_csv(filepath: str) -> DataCube:
    """
    Read a CSV file and convert it into a DataCube.

    The CSV file is expected to have the following format:
    - The first two columns contain integer values representing
      the dimensions (x, y) of the data.
    - Subsequent columns contain wave values.

    :param filepath: Path to the CSV file.
    :type filepath: str
    :return: A DataCube object containing the data from the CSV.
    :rtype: DataCube
    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the CSV format is incorrect.
    """
    wave_data = []

    with open(filepath, mode='r') as file:
        reader = csv.reader(file, delimiter=';')

        # Skip header row
        headers = [h.replace(',', '.') for h in next(reader)]

        for row in reader:
            row = [r.replace(',', '.') for r in row]
            if len(row) < 3:
                raise ValueError("CSV file format is incorrect: expected at least three columns.")
            x = row[0]
            y = row[1]

            # All columns after x, y are waves
            waves = [int(wave_value) for wave_value in row[2:]]  
            wave_data.append(waves)

    cube = to_cube(wave_data, len_x=x, len_y=y)

    return DataCube(cube, wavelengths=headers[2:])
