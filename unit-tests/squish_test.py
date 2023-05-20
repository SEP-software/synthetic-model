#!/usr/bin/env python3
"""Testcase to test the squish event.

Run this test to ensure code does not break and behavior is as expected
"""
import os
import papermill as pm
import pytest
import syntheticModel, Hypercube
import numpy as np
import time 
import geology

def test_squish_same_seed():
  """Test if providing same seed to a model results in identical depositions.
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=20, o=0.0, d=1)
  y_axis = Hypercube.axis(n=20, o=0.0, d=1)
  z_axis = Hypercube.axis(n=20, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  seed = np.random.randint(0,10000)
  # deposit params
  deposit_kw = {"prop":deposit_basement_vp,
                "thick":108,
                "interbedPropVar":10,
                "vp_var":0.00
                }
  # sqiush params
  squish_kw = {"widthInline": 2000,
                "widthCrossline": 2000,
                "max": 50,
                "azimuth": 360
               }
 
  
  # create model A with seed
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed = seed)
  geomodel_A = geology.deposit(geomodel_A,**deposit_kw)
  geomodel_A = geology.squish(geomodel_A,**squish_kw)
  
  # create model B with same seed
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=seed)

  geomodel_B = geology.deposit(geomodel_B,**deposit_kw)
  geomodel_B = geology.squish(geomodel_B,**squish_kw)
  
  # check vp values are the same
  geomodel_A_vp = geomodel_A.get('vp').getNdArray()
  geomodel_B_vp = geomodel_B.get('vp').getNdArray()
  assert ( geomodel_A_vp == pytest.approx(geomodel_B_vp))
  
def test_squish_unique_seed():
  """Test if providing unique seeds to two models results in different depositions.
  """
  # hypercube for model 
  x_axis = Hypercube.axis(n=20, o=0.0, d=1)
  y_axis = Hypercube.axis(n=20, o=0.0, d=1)
  z_axis = Hypercube.axis(n=20, o=0.0, d=1)
  hyper = Hypercube.hypercube(axes=[z_axis, y_axis, x_axis])
  deposit_basement_vp = 2000
  basement = {"vp": deposit_basement_vp}
  primary = "vp"
  
  # deposit params
  deposit_kw = {"prop":deposit_basement_vp,
                "thick":108,
                "interbedPropVar":10,
                "vp_var":0.00
                }
  # sqiush params
  squish_kw = {"widthInline": 2000,
                "widthCrossline": 2000,
                "max": 50,
                "azimuth": 360
               }
 
  
  # create model A with seed
  geomodel_A = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed = 101)
  geomodel_A = geology.deposit(geomodel_A,**deposit_kw)
  geomodel_A = geology.squish(geomodel_A,**squish_kw)
  
  # create model B with same seed
  geomodel_B = syntheticModel.geoModel(hyper, 
                                       basement, 
                                       primary,
                                       seed=102)

  geomodel_B = geology.deposit(geomodel_B,**deposit_kw)
  geomodel_B = geology.squish(geomodel_B,**squish_kw)
                
  # check vp values are the same
  geomodel_A_vp = geomodel_A.get('vp').getNdArray()
  geomodel_B_vp = geomodel_B.get('vp').getNdArray()
  assert ( geomodel_A_vp != pytest.approx(geomodel_B_vp))