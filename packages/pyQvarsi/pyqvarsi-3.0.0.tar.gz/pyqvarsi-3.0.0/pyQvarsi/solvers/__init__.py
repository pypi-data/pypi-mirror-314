#!/usr/bin/env python
#
# pyQvarsi, solvers Module.
#
# Linear solvers.
#
# Last rev: 07/07/2022

__VERSION__ = 2.0

from .lumped        import solver_lumped
from .approxInverse import solver_approxInverse
from .conjgrad      import solver_conjgrad

del lumped, approxInverse, conjgrad