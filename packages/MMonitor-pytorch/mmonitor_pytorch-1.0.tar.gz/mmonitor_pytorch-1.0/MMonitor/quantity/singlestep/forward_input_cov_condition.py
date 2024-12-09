from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
from MMonitor.extensions import ForwardInputEigOfCovExtension
import torch
import numpy as np
import torch.linalg as linalg
from ..utils.calculation import *

class ForwardInputCovCondition(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input_eig_data
            cov = cal_cov_matrix(data) 
            eig_values = cal_eig(cov) 

            eig_values, _ = torch.sort(eig_values, descending=True)
            setattr(self._module, 'eig_values', (eig_values, global_step)) 
        eps = 1e-7
        condition = eig_values[0] / (torch.abs(eig_values[-1]) + eps)
        return condition

    def forward_extensions(self):
        extensions = [ForwardInputEigOfCovExtension()]
        return extensions