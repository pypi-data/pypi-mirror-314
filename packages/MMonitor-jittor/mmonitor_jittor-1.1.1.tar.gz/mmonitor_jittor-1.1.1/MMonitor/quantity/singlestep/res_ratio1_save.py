from .base_class import SingleStepQuantity

import jittor as jt

class ResRatio1Save(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.res_ratio1
        return data 

    def forward_extensions(self):
        extensions = []  
        return extensions
