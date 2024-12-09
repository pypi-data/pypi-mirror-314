import torch
import torch.linalg as linalg 


def cal_cov_matrix(input):
    if input.dim() == 2:
        return torch.cov(input.T) 

    if input.dim() == 3:

        input = input.transpose(0, 2).contiguous().view(input.shape[2], -1)

        return torch.cov(input)


def cal_eig(input):
    eigvals = linalg.eigvals(input)
    return eigvals

