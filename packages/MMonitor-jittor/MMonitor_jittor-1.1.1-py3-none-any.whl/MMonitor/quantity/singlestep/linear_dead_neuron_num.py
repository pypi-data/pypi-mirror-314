from .base_class import SingleStepQuantity
from ...extensions import ForwardOutputExtension
import jittor as jt
# 用于计算死亡神经元的比例，但是设置了一定的大小
class LinearDeadNeuronNum(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        output = data.view(-1, data.shape[-1])
        
        zero_num = [jt.all(output[:, i] <= -2) for i in range(data.shape[-1])]
        return jt.sum(jt.array(zero_num)) / data.shape[-1]  # 计算死神经元比例

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions