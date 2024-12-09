# 用于计算激活值的均值
from .base_class import SingleStepQuantity
from MMonitor.extensions import ForwardOutputExtension
import jittor as jt

class ForwardOutputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        return jt.mean(data)  # 使用Jittor的norm计算L2范数

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions
