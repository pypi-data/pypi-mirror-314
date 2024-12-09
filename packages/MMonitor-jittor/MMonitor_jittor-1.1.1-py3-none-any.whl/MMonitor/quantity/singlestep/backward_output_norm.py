from .base_class import SingleStepQuantity
from MMonitor.extensions import BackwardOutputExtension
import jittor as jt

class BackwardOutputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        data = jt.flatten(data)
        return jt.norm(data, p=2)  # 使用Jittor的norm计算L2范数

    def backward_extensions(self):
        extensions = [BackwardOutputExtension()]
        return extensions
