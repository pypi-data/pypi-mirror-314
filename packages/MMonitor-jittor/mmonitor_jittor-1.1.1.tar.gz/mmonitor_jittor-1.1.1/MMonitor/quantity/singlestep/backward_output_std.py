# 用于计算梯度的标准差
from .base_class import SingleStepQuantity
from MMonitor.extensions import BackwardOutputExtension
import jittor as jt

class BackwardOutputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        return jt.std(data)  # 使用Jittor的std计算标准差


    def backward_extensions(self):
        extensions = [BackwardOutputExtension()]
        return extensions
