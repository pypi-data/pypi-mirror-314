"""
_utils/tracker.py
=================

.. module:: tracker
   :platform: Unix
   :synopsis: Tracker functions for monitoring DataCube changes.

Module Overview
---------------

This module contains functions to track changes made to DataCube instances.

Classes
-------

.. autoclass:: TrackExecutionMeta
   :members:
   :undoc-members:
   :show-inheritance:

"""

exculted = ['stop_recording', 'save_template', '_clean_data', '_map_args_to_kwargs', 'execute_template']


class TrackExecutionMeta(type):
    """
    Metaclass for tracking DataCube method executions.

    This metaclass keeps track of the functions and methods invoked on
    DataCube instances. It can record method calls dynamically.
    """

    recording = False
    recorded_methods = []

    def __new__(cls, name, bases, dct):
        """
        Create a new instance of the metaclass.

        This method wraps methods in the class with a recording decorator
        unless they are excluded from tracking.

        :param cls: The metaclass.
        :param name: The name of the class.
        :param bases: A tuple of base classes.
        :param dct: A dictionary containing the class's namespace.
        :return: A new instance of the class.
        """
        for key, value in dct.items():
            # Wrap only dynamic methods or those that are not in the excluded list
            if callable(value) and key != 'execute_template':
                dct[key] = cls.record_method(value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def record_method(func):
        """
        Decorator for recording method calls.

        This decorator tracks the execution of dynamic methods when recording is enabled.

        :param func: The function to be wrapped.
        :return: A wrapper function that records method calls.
        """
        def wrapper(*args, **kwargs):
            if TrackExecutionMeta.recording:
                if getattr(func, '__is_dynamic__', False):
                    print(f"Tracking dynamic method: {func.__name__}")
                    TrackExecutionMeta.recorded_methods.append(
                        (func.__name__, args, kwargs))
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def start_recording():
        """
        Start tracking method executions.

        This method enables recording of method calls.
        :return: None
        """
        TrackExecutionMeta.recording = True
        TrackExecutionMeta.recorded_methods = []

    @staticmethod
    def stop_recording():
        """
        Stop tracking method executions.

        This method disables recording of method calls.
        :return: None
        """
        TrackExecutionMeta.recording = False
