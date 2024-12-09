from .base_class import SingleStepQuantity
from ...extensions import ForwardOutputExtension

import jittor as jt
# 计算零激活
class ZeroActivationPrecentage(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output[0]
        zero_precentage = (data==0).sum() * 100
        return zero_precentage

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions
