"""
_utils/_loader/tdms.py
========================

.. module:: tdms
   :platform: Unix
   :synopsis: Provides functions to read and write .tdms files.

Module Overview
---------------

This module includes functions for reading .tdms files, specifically designed to extract spectral data
and organize it into a DataCube format.

Functions
---------

.. autofunction:: _read_tdms

"""

import re
import numpy as np
from nptdms import TdmsFile

from ._helper import to_cube
from ..._core import DataCube


def _read_tdms(path: str) -> DataCube:
    """
    Read a .tdms file and convert its contents into a DataCube.

    The function reads and parses the specified TDMS file and extracts relevant data,
    organizing it into a structured format suitable for further analysis.

    :param path: The file path to the TDMS file.
    :type path: str
    :return: A DataCube containing the parsed data from the TDMS file.
    :rtype: DataCube

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the data cannot be parsed correctly.

    :Example:

    >>> dc = _read_tdms('path/to/file.tdms')
    >>> print(dc.shape)  # Output: shape of the DataCube
    """
    # Type for automatic detection
    data_type = ''
    wave_col = 0
    len_col = 0

    # Get values
    file = TdmsFile(path)

    # Build DataFrame
    tdms_df = file.as_dataframe()

    # Copy columns
    col = tdms_df.columns
    col_new = []
    col_sample = []
    col_raw = []

    # Sort by dark and normal
    for i in col:
        i = i.replace(' ', '').replace('\'', '')

        if 'RAW' in i:
            col_raw.append(i)
        elif ('DarkCurrent' in i or 'cm' in i or 'nm' in i):
            continue
        else:
            col_sample.append(i)

        col_new.append(i)

    # Rename columns
    tdms_df.columns = col_new

    # Detect data type and set wave and length columns
    if any("RAMAN" in s for s in col_new):
        data_type = 'raman'
        wave_col = 1
        len_col = 4
    elif any("NIR" in s for s in col_new) or any("KNIR" in s for s in col_new):
        data_type = 'nir'
        wave_col = 1
        len_col = 3
    elif any("VIS" in s for s in col_new) or any("KVIS" in s for s in col_new):
        data_type = 'vis'
        wave_col = 1
        len_col = 3

    # Get wavelength
    wave = np.array(tdms_df[tdms_df.columns[-wave_col]])

    # Parse length information
    len_xy = re.findall(r'\d+', col_new[-len_col])
    len_x = int(len_xy[0]) + 1
    len_y = int(len_xy[1]) + 1

    # Set index and extract samples
    tdms_df = tdms_df.set_index(tdms_df.columns[-2])
    tdms_sample_df = tdms_df[col_sample].copy()

    tdms_sample = np.array(tdms_sample_df)
    tdms_sample_cube = to_cube(data=tdms_sample, len_x=len_x, len_y=len_y)

    wave = wave.astype('int')

    return DataCube(
        cube=tdms_sample_cube,
        wavelengths=wave,
        name=data_type
    )
