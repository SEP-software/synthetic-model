#!/usr/bin/env python3
"""Testcase to test the deposit event.

Run this test to ensure code does not break and behavior is as expected
"""
import os
import papermill as pm
import pytest
import syntheticModel, Hypercube
import numpy as np
import geology

def test_blob_same_seed():
  """Test if providing same seed to a model results in identical blobs.
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=128, o=0.0, d=1)
  y_axis = Hypercube.axis(n=128, o=0.0, d=1)
  z_axis = Hypercube.axis(n=128, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  
  # set random seed
  seed = np.random.randint(0,10000)
  
  # create model A and B with same seed
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=seed)
  geomodel_A = geology.blob(geomodel_A)
  
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=seed)
  geomodel_B = geology.blob(geomodel_B)
  
  # check vp values are the same
  geomodel_A_vp = geomodel_A.get('vp').getNdArray()
  geomodel_B_vp = geomodel_B.get('vp').getNdArray()
  assert ( geomodel_A_vp == pytest.approx(geomodel_B_vp))
  
def test_blob_unique_seed():
  """Test if providing unique seeds to two models results in different blobs.
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
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=101)
  geomodel_A = geology.blob(geomodel_A)
  
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=102)
  geomodel_B = geology.blob(geomodel_B)
  
  # check vp values are the different
  geomodel_A_vp = geomodel_A.get('vp').getNdArray()
  geomodel_B_vp = geomodel_B.get('vp').getNdArray()
  assert ( geomodel_A_vp != pytest.approx(geomodel_B_vp))