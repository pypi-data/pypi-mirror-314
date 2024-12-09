from .backward_extension import *
from .forward_extension import *
import jittor as jt

class ExtensionSelector:

    @staticmethod
    def select(extension_name):
        if extension_name not in globals():
            raise NotImplementedError(
                "hook not found: {}".format(extension_name))
        extension = globals()[extension_name]
        return extension