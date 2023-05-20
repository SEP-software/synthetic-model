from synthetic_model._synthetic_model import GeoModel
from synthetic_model._event import Event
import numpy as np


class Gaussian(Event):
    """Default class for adding a Gaussian"""

    def __init__(self, **kw):
        super().__init__(**kw)

    def applyBase(
        self,
        inM: GeoModel,
        azimuth: float = 0.0,
        center1: float = 0.5,
        center2: float = 0.5,
        center3: float = 0.5,
        vplus: dict = None,
        var: float = 0.0,
    ) -> GeoModel:
        """
        Add gaussian to a model

        Arguements:

            input - Input model
            center2 - [.5] Relative position of anomaly axis2
            center1 - [.5] Relative position of anomaly axis1
            center3 - [.5] Relative position of anomaly axis3
            vplus   - [None] Specify a dictionary with {property:value}
            var     - [0.] Relative variance of anomaly

        Returns

            outModel - Returns updated model
        """
        axes = inM.getPrimaryProperty().get_hyper4().axes

        exts = [ax.d * ax.n for ax in axes]
        ns = [ax.n for ax in axes]
        os = [ax.o for ax in axes]
        ds = [ax.d for ax in axes]

        outM = inM.expand(0, 0)

        if not isinstance(vplus, dict):
            raise Exception("Expecting vplus to be a dictionary")

        d1 = (
            np.linspace(os[0], os[0] + ns[0] * ds[0], ns[0], endpoint=False)
            - center1 * exts[0]
        )
        d2 = (
            np.linspace(os[1], os[1] + ns[1] * ds[1], ns[1], endpoint=False)
            - center2 * exts[1]
        )
        d3 = (
            np.linspace(os[2], os[2] + ns[2] * ds[2], ns[2], endpoint=False)
            - center3 * exts[2]
        )

        dd1, dd2, dd3 = np.meshgrid(d1, d2, d3)

        sc = np.exp(-0.5 * np.sqrt(dd1 * dd1 + dd2 * dd2 + dd3 * dd3) / var)

        for fld in outM.getFloatFieldList():
            if not fld in vplus:
                raise Exception("vplus not specified for %s" % fld)
            out = outM.getFloatField(fld).get_nd_array()
            out += fld["vplus"] * sc
        return outM


class Base(Gaussian):
    def __init__(self, **kw):
        """
        Basic add gaussian anomaly, for now we have not specialized

        """
        super().__init__(**kw)
