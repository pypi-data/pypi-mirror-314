from .base_class import SingleStepQuantity
from ...extensions import ForwardInputExtension

import jittor as jt

class ForwardInputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        
        if data.ndim == 3:
            data = data.transpose(0, 2).contiguous().reshape(data.shape[2], -1)
        else:
            data = data.transpose(0, 1).contiguous().reshape(data.shape[1], -1)

        return jt.std(data)  # 使用Jittor的std计算标准差

    def forward_extensions(self):
        extensions = [ForwardInputExtension()]
        return extensions
