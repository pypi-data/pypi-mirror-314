from .base_class import SingleStepQuantity
from ...extensions import BackwardOutputExtension


class BackwardOutputGradSndNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        return data.norm(2)

    def backward_extensions(self):
        extensions = [BackwardOutputExtension()]
        return extensions


