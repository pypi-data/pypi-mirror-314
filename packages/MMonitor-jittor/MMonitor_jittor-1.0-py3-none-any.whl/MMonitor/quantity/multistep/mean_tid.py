from .base_class import MultiStepQuantity
from ...extensions import ForwardInputExtension
import jittor as jt
import numpy as np
class MeanTID(MultiStepQuantity):

    def _compute_ones(self, global_step):
        data = self._module.input
        if data.dim() == 3:
            data = data.transpose(0, 2).contiguous().view(data.shape[2], -1)
        else:
            data = data.transpose(0, 1).contiguous().view(data.shape[1], -1)
        return data.mean(dim=1)
    
    def _compute(self, global_step):
        diff_data = [d - self._module.running_mean for d in self.cache]
        diff_data = jt.stack(diff_data, dim=0)  # 使用Jittor的stack
        eps = 1e-8
        running_var = self._module.running_var
        if isinstance(running_var, np.ndarray):
            running_var = jt.array(running_var)
        result = diff_data.norm(dim=-1) / (jt.sqrt(running_var).norm(dim=-1) + eps)
        return result.mean()

    def forward_extensions(self):
        extensions = [ForwardInputExtension()]
        return extensions
