import torch
import torch.linalg as linalg


def cal_cov_matrix(input):
    if input.dim() == 2:
        return torch.cov(input.T)
    if input.dim() == 3:
        input = input.transpose(0, 2).contiguous().view(input.shape[2], -1)
        return torch.cov(input)
    if input.dim() == 4:
        x = input.view(input.shape[0], input.shape[1], -1)  # 形状为 (batch_size, channels, height * width)
        x = x.transpose(0, 1)  # 形状为 (channels, batch_size, height * width)
        x = x.reshape(x.shape[0], -1)  # 形状为 (channels, batch_size * height * width)
        mean = torch.mean(x, dim=1, keepdims=True)
        centered_input = x - mean
        cov_matrix = centered_input @ centered_input.t() / (x.shape[1] - 1)
        return cov_matrix


def cal_eig(input):

    try:
        _, eigvals, _ = linalg.svd(input.float())
    except Exception as e:
        lens = min(input.shape)
        eigvals = torch.tensor([1.1 for i in range(lens)])
        eigvals[lens-1] = 111
    return eigvals

def cal_eig_not_sym(input):
    try:
        _, eigvals, _ = linalg.svd(input.float())
    except Exception as e:
        lens = min(input.shape)
        eigvals = torch.tensor([1.1 for i in range(lens)])
        eigvals[lens-1] = 111
    return eigvals
