from MMonitor.extensions.extension import Extension


class ForwardInputEigOfCovExtension(Extension):

    def __init__(self):
        super(ForwardInputEigOfCovExtension, self).__init__()
        self._name = 'input_eig_data' 

    def _default(self, module, input, output):
        data = input[0]
        return data

    def _Linear(self, module, input, output):
        data = input[0]
        return data

    def _Conv(self, module, input, output):
        data = input[0]
        return data

