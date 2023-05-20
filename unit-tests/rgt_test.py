#!/usr/bin/env python3
"""Testcase to test the relative geologic time (RGT) event in notebooks.

Run this test to ensure code does not break. Check notebooks to ensure rgt
behavior works as expected
"""
import os
import papermill as pm
import pytest
import syntheticModel, Hypercube
import numpy as np

def test_rgt_notebook(tmpdir):
  """Test simple faulting in notebook"""
  notebook_path = os.path.join(os.path.dirname(__file__),
                               "rgt_tutorial.ipynb")
  test_output_name = os.path.join(tmpdir, "_test_output.ipynb")
  pm.execute_notebook(notebook_path, test_output_name)
  assert os.path.isfile(test_output_name)