import jittor as jt
import jittor.linalg as linalg


def cal_cov_matrix(x):
    if x.dim() == 2:
        mean_x = jt.mean(x,dim=0)
        x_centered = x - mean_x
        cov_matrix = (x_centered.t() @ x_centered) / (x.shape[0]-1)
        return cov_matrix
    if x.dim() == 3:
        x = x.transpose(0,2).reshape(x.shape[2],-1)
        mean = jt.mean(x,dim=1,keepdims=True)
        centered_input = x - mean
        cov_matrix = centered_input @ centered_input.t() / (x.shape[1] - 1)
        return cov_matrix
    if x.dim() == 4:
        x = x.transpose(0, 2).reshape(x.shape[2], -1)
        mean = jt.mean(x, dim=1, keepdims=True)
        centered_input = x - mean
        cov_matrix = centered_input @ centered_input.t() / (x.shape[1] - 1)
        return cov_matrix
        

def cal_eig(input):
    eigvals, _ = linalg.eig(input)
    return eigvals


def cal_eig_not_sym(input):
    try:
        _, eigvals, _ = linalg.svd(input.float())
    except Exception as e:
        lens = min(input.shape)
        eigvals = jt.array([1.1 for _ in range(lens)])
        eigvals[lens - 1] = 111
    return eigvals
