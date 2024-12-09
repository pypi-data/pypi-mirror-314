from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
from MMonitor.extensions import ForwardInputExtension


class ForwardInputSndNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        return data.norm(2) 

    def forward_extensions(self):
        extensions = [ForwardInputExtension()]
        return extensions

