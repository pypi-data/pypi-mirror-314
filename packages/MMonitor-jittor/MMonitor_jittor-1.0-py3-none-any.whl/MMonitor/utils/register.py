from collections import defaultdict


class Register:
    def __init__(self):
        self.forward_handles = defaultdict()

    @staticmethod
    def register_forward(model, forward_hooks):
        for hook in forward_hooks:
            model.register_forward_hook(hook)

    @staticmethod
    def register_backward(model, backward_hooks):
        for hook in backward_hooks:
            model.register_backward_hook(hook)


