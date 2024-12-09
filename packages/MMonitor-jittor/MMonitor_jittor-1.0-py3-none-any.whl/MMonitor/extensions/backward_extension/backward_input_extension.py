# 相对于当前层输入的梯度
from ..extension import Extension
class BackwardInputExtension(Extension):
    def __init__(self):
        self._name = 'input_grad'

    def _default(self, module, grad_input, grad_output):
        return grad_input[0]

    def _Linear(self, module, grad_input, grad_output):
        return grad_input[0]

    def _Conv(self, module, grad_input, grad_output):
        return grad_input[0]