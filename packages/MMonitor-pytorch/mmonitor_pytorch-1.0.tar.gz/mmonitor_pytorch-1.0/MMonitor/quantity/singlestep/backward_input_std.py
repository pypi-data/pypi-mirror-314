from .base_class import SingleStepQuantity
from ...extensions import BackwardInputExtension


class BackwardInputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input_grad
        if data.dim() == 3:
            data = data.transpose(0, 2).contiguous().view(data.shape[2], -1)
        else:
            data = data.transpose(0, 1).contiguous().view(data.shape[1], -1)
        return data.std()
    def backward_extensions(self):
        extensions = [BackwardInputExtension()]
        return extensions


