from synthetic_model._synthetic_model import GeoModel
from synthetic_model._event import Event
import datetime


class ErodeFlat(Event):
    """Base class for eroding a plane"""

    def __init__(self, **kw):
        """Initialize the base class for erode flat"""
        super().__init__(**kw)

    def applyBase(self, inM: GeoModel, depth: float = 50.0) -> GeoModel:
        """Squish a model

        Arguements:

        depth - [50.] Depth (axis 1) to slice off

        Returns

        outModel - Returns updated model
        """

        axes = inM.getPrimaryProperty().get_hyper().axes
        outM = inM.expand(0, 0)

        ic = int(depth / axes[0].d)

        lay = outM.getLayer().get_nd_array()

        lay[:, :, :ic] = -1

        return outM


class Basic(ErodeFlat):
    def __init__(self, **kw):
        """
        Basic erosion plane, for now we have not specialized

        """
        super().__init__(**kw)
