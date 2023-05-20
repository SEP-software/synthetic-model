#!/usr/bin/env python3
"""Testcase to test the faulting event in notebooks.

Run this test to ensure code does not break. Check notebooks to ensure fault
behavior works as expected
"""
import os
import papermill as pm
import pytest
import syntheticModel, Hypercube
import numpy as np
# import fault
import geology

def test_fault_notebook(tmpdir):
  """Test simple faulting in notebook"""
  notebook_path = os.path.join(os.path.dirname(__file__),
                               "fault_tutorial.ipynb")
  test_output_name = os.path.join(tmpdir, "_test_output.ipynb")
  pm.execute_notebook(notebook_path, test_output_name)
  assert os.path.isfile(test_output_name)
  
def test_fault_and_squish_notebook(tmpdir):
  """Test squishing after faulting in notebook"""
  notebook_path = os.path.join(os.path.dirname(__file__),
                               "fault_and_squish_tutorial.ipynb")
  test_output_name = os.path.join(tmpdir, "_test_output.ipynb")
  pm.execute_notebook(notebook_path, test_output_name)
  assert os.path.isfile(test_output_name)
  
def test_fault_same_seed():
  """Test if providing same seed to a model results in identical faults.
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=128, o=0.0, d=1)
  y_axis = Hypercube.axis(n=128, o=0.0, d=1)
  z_axis = Hypercube.axis(n=128, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  seed = np.random.randint(0,10000)
  # create model A 
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary, 
                                       seed=seed)
  # fault model A 
  fault_kw = {"begx":0.5,
              "begy":0.5,
              "begz":0.5,
              "angle":10,
              "indicate":True,
              "radiusFreq":0.1,
              "ruptureLength":50,
              "extentInLine":75,
              "extentCrossLine":200,
              "shift":15,
              "radius":2000,
              "indicateF":True,
              "indicateI":True}
  geomodel_A = geology.fault(geomodel_A,**fault_kw)
  
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary, 
                                       seed=seed)
  geomodel_B = geology.fault(geomodel_B,**fault_kw)
   
  # check integer and float fault indicators are the same
  geomodel_A_float_indicator = geomodel_A.getIndicatorF().getNdArray()
  geomodel_B_float_indicator = geomodel_B.getIndicatorF().getNdArray()
  assert ( geomodel_A_float_indicator == pytest.approx(geomodel_B_float_indicator))
  
  geomodel_A_int_indicator = geomodel_A.getIndicatorI().getNdArray()
  geomodel_B_int_indicator = geomodel_B.getIndicatorI().getNdArray()
  assert ( geomodel_A_int_indicator == pytest.approx(geomodel_B_int_indicator))
  
def test_fault_unique_seed():
  """Test if providing unique seeds to two models results in different faults.
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=128, o=0.0, d=1)
  y_axis = Hypercube.axis(n=128, o=0.0, d=1)
  z_axis = Hypercube.axis(n=128, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  
  # create model A 
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary, 
                                       seed=np.random.randint(0,10000))
  # fault model A 
  fault_kw = {"begx":0.5,
              "begy":0.5,
              "begz":0.5,
              "angle":10,
              "indicate":True,
              "radiusFreq":0.1,
              "ruptureLength":50,
              "extentInLine":75,
              "extentCrossLine":200,
              "shift":15,
              "radius":2000,
              "indicateF":True,
              "indicateI":True}
  geomodel_A = geology.fault(geomodel_A,**fault_kw)
  
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary, 
                                       seed=np.random.randint(0,10000))
  geomodel_B = geology.fault(geomodel_B,**fault_kw)
   
  # check integer and float fault indicators are the same
  geomodel_A_float_indicator = geomodel_A.getIndicatorF().getNdArray()
  geomodel_B_float_indicator = geomodel_B.getIndicatorF().getNdArray()
  assert ( geomodel_A_float_indicator != pytest.approx(geomodel_B_float_indicator))
  
  geomodel_A_int_indicator = geomodel_A.getIndicatorI().getNdArray()
  geomodel_B_int_indicator = geomodel_B.getIndicatorI().getNdArray()
  assert ( geomodel_A_int_indicator != pytest.approx(geomodel_B_int_indicator))