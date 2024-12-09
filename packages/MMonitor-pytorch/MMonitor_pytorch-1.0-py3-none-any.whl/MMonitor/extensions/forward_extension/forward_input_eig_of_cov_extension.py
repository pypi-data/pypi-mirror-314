from MMonitor.extensions.extension import Extension


class ForwardInputEigOfCovExtension(Extension):

    def __init__(self):
        super(ForwardInputEigOfCovExtension, self).__init__()
        self._name = 'input_eig_data' 

    def _default(self, module, input, output):
        data = input[0]
        return data

    def _Linear(self, module, input, output):
        data = input[0]
        return data

    def _Conv2d(self, module, input, output):
        data = input[0]
        # import pdb
        # pdb.set_trace()
        # b, c, w, h = data.shape
        # data = data.transpose(0, 1).contiguous().view(-1, c)
        return data

