import typing as t

import numpy as np
import numpy.typing as npt
from scipy.stats import f


def hotelling_two_sample_test(
    X: npt.NDArray[np.int32], Y: npt.NDArray[np.int32], p_v: float = 0.01
) -> t.Tuple[npt.NDArray[np.int32], float, float, list]:
    """Perform a two-sample Hotelling T^2 test on the given data.

    Parameters
    ----------
    X : np.ndarray
        The first sample data.
    Y : np.ndarray
        The second sample data.
    p_v : float, optional
        The p-value threshold for the test, by default 0.01.

    Returns
    -------
    np.ndarray
        The difference between the means of the two samples.
    float
        The F-statistic from the Hotelling T^2 test.
    float
        The p-value of the test.
    list[bool]
        A list of booleans indicating which features in the difference array
        are significantly different.
    """
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

    # Compute the array of the stacks that are significantly different
    fs = f_pdf.ppf(1 - p_v)
    ws = pooled_cov.diagonal() * fs / g
    m: list[bool] = [(d**2 >= w) for d, w in zip(delta, ws)]

    return delta, statistic, p_value, m
