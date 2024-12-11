from numba import jit, njit, vectorize
import numpy as np

@vectorize
def calc_slope(x1,y1,x2,y2):
    xd = x2-x1
    if xd == 0:
        slope = 0
    else:
        slope = (y2-y1) / (xd)
    return slope

@njit
def siegel_repeated_medians(x,y):
    n_total = x.size
    slopes = np.empty((n_total), dtype=y.dtype)
    ints = np.empty((n_total), dtype=y.dtype)
    slopes_sub = np.empty((n_total-1), dtype=y.dtype)
    for i in range(n_total):
        for j in range(n_total):
            if i == j:
                continue
            slopes_sub[j] = calc_slope(x[i],y[i],x[j],y[j])
        slopes[i] = np.median(slopes_sub)
        ints[i] = y[i] - slopes[i]*x[i]
    trend = x * np.median(slopes) + np.median(ints)
    return trend

@jit
def lasso_nb(X, y, alpha, tol=0.001, maxiter=10000):
    n, p = X.shape
    beta = np.zeros(p)
    R = y.copy()
    norm_cols_X = (X ** 2).sum(axis=0)
    resids = []
    prev_cost = 10e10
    for n_iter in range(maxiter):
        for ii in range(p):
            beta_ii = beta[ii]
            if beta_ii != 0.:
                R += X[:, ii] * beta_ii
            #contiguous_X = np.ascontiguousarray(X[:, ii])
            #contiguous_R = np.ascontiguousarray(R)
            #tmp = np.dot(contiguous_X, contiguous_R)
            tmp = np.dot(X[:, ii], R)
            beta[ii] = fsign(tmp) * max(abs(tmp) - alpha, 0) / (.00001 + norm_cols_X[ii])
            if beta[ii] != 0.:
                R -= X[:, ii] * beta[ii]
        cost = (np.sum((y - X @ beta)**2) + alpha * np.sum(np.abs(beta))) / n
        resids.append(cost)
        if prev_cost - cost < tol:
            break
        else:
            prev_cost = cost
    return beta

@njit
def fsign(f):
    if f == 0:
        return 0
    elif f > 0:
        return 1.0
    else:
        return -1.0
