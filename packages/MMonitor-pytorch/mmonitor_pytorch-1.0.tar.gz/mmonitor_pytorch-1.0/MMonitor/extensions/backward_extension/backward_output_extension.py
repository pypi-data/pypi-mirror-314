from ..extension import Extension


class BackwardOutputExtension(Extension):
    def __init__(self):
        self._name = 'output_grad'

    def _default(self, module, grad_input, grad_output):
        """
        默认处理：获取第一个输出梯度，并确保有效性。
        """
        if grad_output and grad_output[0] is not None:
            output = grad_output[0].clone()  # 克隆输出梯度，避免原地操作
        else:
            output = None
        return output  # 返回安全的输出梯度

    def _Linear(self, module, grad_input, grad_output):
        """
        Linear 模块的处理逻辑。
        """
        if grad_output and grad_output[0] is not None:
            output = grad_output[0].clone()  # 处理第一个输出梯度
            # 在这里可以添加特定于 Linear 的逻辑
        else:
            output = None
        return output

    def _Conv2d(self, module, grad_input, grad_output):
        """
        Conv2d 模块的处理逻辑。
        """
        if grad_output and grad_output[0] is not None:
            output = grad_output[0].clone()  # 处理第一个输出梯度
            # 在这里可以添加特定于 Conv2d 的逻辑
        else:
            output = None
        return output



