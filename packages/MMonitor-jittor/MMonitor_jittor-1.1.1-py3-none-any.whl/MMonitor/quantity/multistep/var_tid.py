from .base_class import MultiStepQuantity
from ...extensions import ForwardInputExtension
import jittor as jt

class VarTID(MultiStepQuantity):

    def _compute_ones(self, global_step):
        data = self._module.input
        if data.dim() == 3:
            data = data.transpose(0, 2).contiguous().view(data.shape[2], -1)
        else:
            data = data.transpose(0, 1).contiguous().view(data.shape[1], -1)
        return jt.sqrt(data.var(dim=1))  # 使用Jittor的sqrt和var
    
    def _compute(self, global_step):
        running_sigma = jt.sqrt(self._module.running_var)  # 使用Jittor的sqrt
        diff_data = [d - running_sigma for d in self.cache]
        diff_data = jt.stack(diff_data, dim=0)  # 使用Jittor的stack
        
        eps = 1e-8
        result = diff_data.norm(dim=-1) / (running_sigma.norm(dim=-1) + eps)
        return result.mean()

    def forward_extensions(self):
        extensions = [ForwardInputExtension()]
        return extensions
