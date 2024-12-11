"""
_utils/helper.py
=================

.. module:: helper
   :platform: Unix
   :synopsis: Helper functions for processing wave and cube values.

Module Overview
---------------

This module contains helper functions to assist in processing wave and cube values.

Functions
---------

.. autofunction:: find_nex_greater_wave
.. autofunction:: find_nex_smaller_wave

"""


def find_nex_greater_wave(waves, wave_1: int, maximum_deviation: int = 5) -> int:
    """
    Finds the next greater wave value in a list of waves within a specified deviation.

    This function identifies the smallest wave value greater than the specified `wave_1`
    within a range defined by `maximum_deviation`. If no such value exists, it returns -1.

    :param waves: A list of integers representing the available wave values.
    :type waves: list[int]
    :param wave_1: The starting wave value to find the next greater wave for.
    :type wave_1: int
    :param maximum_deviation: The maximum deviation from `wave_1` to consider.
    :type maximum_deviation: int
    :returns: The next greater wave value within the deviation range, or -1 if no such value exists.
    :rtype: int
    """

    wave_next = -1

    for n in range(maximum_deviation):
        wave_n = wave_1 + n

        if wave_n in waves:
            wave_next = wave_n
            break

    return wave_next


def find_nex_smaller_wave(waves, wave_1: int, maximum_deviation: int = 5) -> int:
    """
    Finds the next smaller wave value in a list of waves within a specified deviation.

    This function identifies the largest wave value smaller than the specified `wave_1`
    within a range defined by `maximum_deviation`. If no such value exists, it returns -1.

    :param waves: A list of integers representing the available wave values.
    :type waves: list[int]
    :param wave_1: The starting wave value to find the next smaller wave for.
    :type wave_1: int
    :param maximum_deviation: The maximum deviation from `wave_1` to consider.
    :type maximum_deviation: int
    :returns: The next smaller wave value within the deviation range, or -1 if no such value exists.
    :rtype: int
    """
    
    wave_next = -1

    for n in range(maximum_deviation):
        wave_n = wave_1 - n

        if wave_n in waves:
            wave_next = wave_n
            break

    return wave_next
