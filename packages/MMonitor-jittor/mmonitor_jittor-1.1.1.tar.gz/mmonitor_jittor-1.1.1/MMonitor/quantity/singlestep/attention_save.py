from .base_class import SingleStepQuantity


class AttentionSave(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.attention
        return data