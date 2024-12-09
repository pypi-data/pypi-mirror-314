from .base_class import SingleStepQuantity

import jittor as jt

class WeightStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.weight
        
        return jt.std(data)
