from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
from MMonitor.extensions import ForwardInputExtension
import jittor as jt

class ForwardInputSndNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        # 由于jittor按照行计算l2范数
        # 需要将其转换为一维
        data_flatten = jt.flatten(data)
        return jt.norm(data_flatten, p=2)  # 使用Jittor的norm计算L2范数

    def forward_extensions(self):
        extensions = [ForwardInputExtension()]
        return extensions

