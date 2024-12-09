from ..extension import Extension
# 相对于输出的梯度
class BackwardOutputExtension(Extension):

    def __init__(self):
        self._name = 'output_grad'

    def _default(self, module, grad_input, grad_output):
        return grad_output[0]

    def _Linear(self, module, grad_input, grad_output):
        return grad_output[0]

    def _Conv(self, module, grad_input, grad_output):
        return grad_output[0]