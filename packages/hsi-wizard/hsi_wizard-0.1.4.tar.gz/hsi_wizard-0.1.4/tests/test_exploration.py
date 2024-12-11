import numpy as np
import matplotlib

import wizard

import pytest

matplotlib.use("Agg")

class TestPlotter:

    def test_plot_function_runs(self):
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))
        wizard.plotter(dc)

class TestSurcefacePlot:

    def test_surface_function_runs(self):
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))
        wizard.plot_surface(dc)
