from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
from MMonitor.extensions import ForwardInputEigOfCovExtension
from MMonitor.extensions.utils.calculation import cal_cov_matrix,cal_eig
import jittor as jt
import jittor.linalg as linalg
from collections import defaultdict

class ForwardInputCovCondition(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input_eig_data
            cov = cal_cov_matrix(data)
            eig_values = linalg.eig(cov)[0]
            if isinstance(eig_values, jt.Var):
                eig_values = eig_values
            else:
                eig_values = jt.Var(eig_values.real) # 直接转换为 Jittor Var
            eig_values = jt.ops.argsort(eig_values, descending=True)  # Sort eigenvalues in descending order
            
            setattr(self._module, 'eig_values', (eig_values, global_step))
        eps = 1e-7
        eig_values_float = eig_values[1]
        condition = eig_values_float[0] / (jt.abs(eig_values_float[-1]) + eps)
        return condition

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions