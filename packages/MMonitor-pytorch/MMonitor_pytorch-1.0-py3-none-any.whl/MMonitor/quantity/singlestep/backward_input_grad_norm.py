from .base_class import SingleStepQuantity
from ...extensions import BackwardInputExtension


class BackwardInputSndNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input_grad
        return data.norm(2)

    def backward_extensions(self):
        extensions = [BackwardInputExtension()]
        return extensions


