#!/usr/bin/env python
#
# pyQvarsi, plotting Module.
#
# Module to plot the flow.
#
# Last rev: 25/01/2023

__VERSION__ = 2.0

from .plot_pyvista    import pvplot, pvcontour, pvslice
from .plot_matplotlib import Plotter

del plot_pyvista, plot_matplotlib