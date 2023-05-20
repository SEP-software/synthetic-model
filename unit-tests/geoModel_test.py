#!/usr/bin/env python3
"""Testcase to test the geomodel class
"""
import os
import papermill as pm
import pytest
import syntheticModel, Hypercube
import numpy as np
  
def test_simple_init():
  """Test if model initializes
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=128, o=0.0, d=1)
  y_axis = Hypercube.axis(n=128, o=0.0, d=1)
  z_axis = Hypercube.axis(n=128, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  
  # create model A and B with same seed
  geomodel = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                    seed=101)