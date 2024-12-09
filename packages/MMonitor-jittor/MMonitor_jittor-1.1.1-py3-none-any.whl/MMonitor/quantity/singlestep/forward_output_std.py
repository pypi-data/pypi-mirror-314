# 用于计算激活值的std
from .base_class import SingleStepQuantity
from MMonitor.extensions import ForwardOutputExtension
import jittor as jt

class ForwardOutputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        return jt.std(data)  

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions
