from MMonitor.extensions.extension import Extension
class ForwardInputExtension(Extension):

    def __init__(self):
        self._name = 'input'
        super(ForwardInputExtension, self).__init__()

    def _default(self, module, input, output):
        return input[0]

    def _Linear(self, module, input, output):
        return input[0]

    def _Conv(self, module, input, output):
        return input[0]