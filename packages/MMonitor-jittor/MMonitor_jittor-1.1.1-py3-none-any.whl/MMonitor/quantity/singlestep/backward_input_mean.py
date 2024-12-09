# 用于计算梯度的均值
from .base_class import SingleStepQuantity
from MMonitor.extensions import BackwardInputExtension
import jittor as jt

class BackwardInputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input_grad
        return jt.mean(data)  # 使用Jittor的mean计算


    def backward_extensions(self):
        extensions = [BackwardInputExtension()]
        return extensions
