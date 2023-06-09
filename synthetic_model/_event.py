from synthetic_model._synthetic_model import GeoModel
import copy


class Event:
    def __init__(self, **kw):
        self.kw = kw

    def updateArguments(self, **kw):
        """Override arguments used to create class"""

        kuse = copy.deepcopy(self.kw)
        for k, v in kw.items():
            kuse[k] = v
        return kuse

    def applyBase(self, **kw):
        """Base class to implement various function, must be overriten"""
        raise Exception("Must override argBase")

    def apply(self, modIn: GeoModel, **kw) -> GeoModel:
        """
        Basic apply function

        modIn - Input model

        You can override in of the arguemnts of the base class with
        function arguments. Self-doc the base class applyBase function


        """
        return self.applyBase(modIn, **self.updateArguments(**kw))
