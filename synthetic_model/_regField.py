import numpy as np
from sep_python.hypercube import Hypercube


class RegField:
    """Basic wrapper class for a numpy array"""

    def __init__(self, hyper: Hypercube, storage: str = "dataFloat"):
        """hyper - Hypercube
        storage - Storage type"""

        self._hyper = hyper
        ns = self._hyper.getNs()
        if storage == "dataFloat":

            self._vals = np.zeros((ns[2], ns[1], ns[0]), dtype=np.float32)
        elif storage == "dataInt":
            self._vals = np.zeros((ns[2], ns[1], ns[0]), dtype=np.int32)

    def get_hyper(self):
        """Return the hypercube"""
        return self._hyper

    def get_nd_array(self):
        """Return the numpy array"""
        return self._vals
