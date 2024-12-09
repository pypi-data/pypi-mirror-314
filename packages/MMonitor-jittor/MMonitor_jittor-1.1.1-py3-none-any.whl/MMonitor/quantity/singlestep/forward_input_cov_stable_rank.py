from .base_class import SingleStepQuantity
from ...extensions import ForwardInputEigOfCovExtension
import jittor as jt
from ..utils.calculation import *
class ForwardInputCovStableRank(SingleStepQuantity):
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
            _,eig_values = jt.ops.argsort(eig_values, descending=True)  # 对特征值按降序排序
            setattr(self._module, 'eig_values', (eig_values, global_step))
        max_eigen_value = eig_values[0]
        eigs_sum = eig_values.sum()
        
        if max_eigen_value == 0:
            return eigs_sum * 0
        
        stable_rank = eigs_sum / max_eigen_value
        return stable_rank

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions