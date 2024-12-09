import math
import jittor as jt
from .base_class import SingleStepQuantity
from ...extensions import ForwardInputEigOfCovExtension
from ..utils.calculation import *
class ForwardInputCovCondition50(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input_eig_data
            cov = cal_cov_matrix(data)
            eig_values = cal_eig(cov)
            # 确保 eig_values 是一个 Jittor Var
            if not isinstance(eig_values, jt.Var):
                eig_values = jt.Var(eig_values.real)
            # 对特征值进行排序（降序）并只保留值
            eig_values = jt.sort(eig_values, descending=True)[0]  # 添加[0]来只获取排序后的值
            setattr(self._module, 'eig_values', (eig_values, global_step))
        length = len(eig_values)
        index = math.floor(length * 0.5)
        eps = 1e-7
        condition50 = eig_values[0] / (jt.abs(eig_values[index]) + eps)
        return condition50

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions