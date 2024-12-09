# 用于计算激活值的norm
from .base_class import SingleStepQuantity
from MMonitor.extensions import ForwardOutputExtension
import jittor as jt

class ForwardOutputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        data = jt.flatten(data)
        return jt.norm(data, p=2)  # 使用Jittor的norm计算L2范数

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions
