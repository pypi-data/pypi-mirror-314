from ..extension import Extension
from ..utils.calculation import cal_cov_matrix,cal_eig

class BackwardOutputEigOfCovExtension(Extension):

    def __init__(self):
        super(BackwardOutputEigOfCovExtension, self).__init__()
        self._name = 'output_grad_eig'

    def _default(self, module, grad_input, grad_output):
        data = grad_output[0]
        cov = cal_cov_matrix(data)
        result = cal_eig(cov)
        return result.real

    def _Linear(self, module, grad_input, grad_output):
        data = grad_output[0]
        cov = cal_cov_matrix(data)
        result = cal_eig(cov)
        return result.real

    def _Conv(self, module, grad_input, grad_output):
        data = grad_output[0]
        b, c, w, h = data.shape
        assert (c > 1), "channel must > 1"
        data = data.transpose(0, 1).contiguous().view(-1, c)
        cov = cal_cov_matrix(data)
        result = cal_eig(cov)
        return result.real

