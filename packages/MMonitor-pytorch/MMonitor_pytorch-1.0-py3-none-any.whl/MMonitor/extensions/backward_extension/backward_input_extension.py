from sympy import Q
from ..extension import Extension


class BackwardInputExtension(Extension):
    def __init__(self):
        self._name = 'input_grad'

    def _default(self, module, grad_input, grad_output):
        # grad_input 是一个元组，需要逐个处理
        input = tuple(t.clone() if t is not None else None for t in grad_input)
        print(input,input[0])
        return input[0] if input else None  # 确保存在有效梯度


    def _Linear(self, module, grad_input, grad_output):
        input = tuple(t.clone() if t is not None else None for t in grad_input)
        return input[0] if input else None

    def _Conv2d(self, module, grad_input, grad_output):
        input = tuple(t.clone() if t is not None else None for t in grad_input)
        return input[0] if input else None


