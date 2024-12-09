from .base_class import SingleStepQuantity
from ...extensions import ForwardInputEigOfCovExtension
from ..utils.calculation import *
import math
import jittor as jt
class ForwardInputCovCondition80(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input_eig_data
            cov = cal_cov_matrix(data)
            eig_values = cal_eig(cov)
            if isinstance(eig_values, jt.Var):
                eig_values = eig_values
            else:
                eig_values = jt.Var(eig_values.real) # 直接转换为 Jittor Var
            eig_values = jt.ops.argsort(eig_values, descending=True)  # 对特征值按降序排序
            setattr(self._module, 'eig_values', (eig_values, global_step))
        
        eig_values_float = eig_values[1]
        length = len(eig_values_float)
        index = math.floor(length * 0.8)
        eps = 1e-7
        condition80 = eig_values_float[0] / (jt.abs(eig_values_float[index]) + eps)
        return condition80

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions
