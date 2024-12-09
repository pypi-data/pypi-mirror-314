from .base_class import SingleStepQuantity
from ...extensions import ForwardInputEigOfCovExtension
from ..utils.calculation import *
import jittor as jt

class ForwardInputCovMaxEig(SingleStepQuantity):
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
            eig_values = jt.ops.argsort(eig_values, descending=True)  # Sort eigenvalues in descending order
            
            setattr(self._module, 'eig_values', (eig_values, global_step))
        max_eigen_value = eig_values[1][0]  # 最大特征值
        return max_eigen_value

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions
