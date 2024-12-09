from .base_class import SingleStepQuantity

import jittor as jt

class WeightNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.weight
        data = jt.flatten(data)
        return jt.norm(data, p=2)  
