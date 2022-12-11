import typing as t

import numpy as np
from scipy.stats import f


def hotelling_two_sample_test(
    X, Y, p_v=0.01
) -> t.Tuple[np.ndarray, float, float, list]:
    nx, p = X.shape
    ny, q = Y.shape

    assert p == q, "X and Y must have the same dimensionality"

    dof = nx + ny - p - 1

    assert dof > 0, "X and Y must have at least p + 1 samples"

    g = dof / p / (nx + ny - 2) * (nx * ny) / (nx + ny)

    x_mean = np.mean(X, axis=0)
    y_mean = np.mean(Y, axis=0)
    delta = x_mean - y_mean

    x_cov = np.cov(X, rowvar=False)
    y_cov = np.cov(Y, rowvar=False)
    pooled_cov = ((nx - 1) * x_cov + (ny - 1) * y_cov) / (nx + ny - 2)

    # Compute the F statistic from the Hotelling T^2 statistic
    statistic = g * delta.transpose() @ np.linalg.inv(pooled_cov) @ delta
    f_pdf = f(p, dof)
    p_value = 1 - f_pdf.cdf(statistic)

    # Compute the map of the stacks that are significantly different
    fs = f_pdf.ppf(1 - p_v)
    ws = pooled_cov.diagonal() * fs / g
    m = [(d**2 - w >= 0) for d, w in zip(delta, ws)]

    return delta, statistic, p_value, m
