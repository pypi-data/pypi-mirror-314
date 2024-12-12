import math

import numpy as np

from casm.bset.cluster_functions import (
    make_orthonormal_discrete_functions,
)


def point_sum(x, phi):
    sum = 0.0
    for i in range(len(x)):
        sum += x[i] * phi[i]
    return sum


def pair_sum(x, phi):
    sum = 0.0
    for i in range(len(x)):
        for j in range(len(x)):
            sum += x[i] * x[j] * phi[i] * phi[j]
    return sum


def triplet_sum(x, phi):
    sum = 0.0
    for i in range(len(x)):
        for j in range(len(x)):
            for k in range(len(x)):
                sum += x[i] * x[j] * x[j] * phi[i] * phi[j] * phi[k]
    return sum


def binary_checks(x, phi_expected):
    abs_tol = 1e-10
    phi = make_orthonormal_discrete_functions(x, abs_tol=abs_tol)
    assert np.allclose(phi, phi_expected, atol=abs_tol)
    assert math.isclose(point_sum(x, phi[1, :]), 0.0, abs_tol=abs_tol)
    assert math.isclose(pair_sum(x, phi[1, :]), 0.0, abs_tol=abs_tol)
    assert math.isclose(triplet_sum(x, phi[1, :]), 0.0, abs_tol=abs_tol)


def test_discrete_functions_1():
    ## binary (checks vs CASM v1)

    x = [1.0, 0.0]
    binary_checks(x, np.array([[1.0, 1.0], [0.0, 1.0]]))

    x = [0.5, 0.5]
    binary_checks(x, np.array([[1.0, 1.0], [-1.0, 1.0]]))

    x = [0.45, 0.55]
    binary_checks(x, np.array([[1.0, 1.0], [1.08386, -0.886796]]))

    x = [0.4, 0.6]
    binary_checks(x, np.array([[1.0, 1.0], [1.13389, -0.755929]]))

    x = [0.3, 0.7]
    binary_checks(x, np.array([[1.0, 1.0], [1.15079, -0.493197]]))

    x = [0.25, 0.75]
    binary_checks(x, np.array([[1.0, 1.0], [1.13389, -0.377964]]))

    x = [0.2, 0.8]
    binary_checks(x, np.array([[1.0, 1.0], [1.1094, -0.27735]]))

    x = [0.1, 0.9]
    binary_checks(x, np.array([[1.0, 1.0], [1.05337, -0.117041]]))

    x = [0.0, 1.0]
    binary_checks(x, np.array([[1.0, 1.0], [1.0, 0.0]]))

    ## ternary

    # composition [1.0, 0.0, 0.0]
    # [0., 1., 0.]
    # [0., 0., 1.]
    phi = make_orthonormal_discrete_functions([1.0, 0.0, 0.0], abs_tol=1e-10)
    assert np.allclose(
        phi, np.array([[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    )

    # composition [0.0, 1.0, 0.0]
    # [0., 1., 0.]
    # [0., 0., 1.]
    phi = make_orthonormal_discrete_functions([0.0, 1.0, 0.0], abs_tol=1e-10)
    assert np.allclose(
        phi, np.array([[1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    )

    # composition [0.0, 0.0, 1.0]
    # [0., 1., 0.]
    # [0., 0., 1.]
    phi = make_orthonormal_discrete_functions([0.0, 0.0, 1.0], abs_tol=1e-10)
    assert np.allclose(
        phi, np.array([[1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    )

    # composition [1/3., 1/3., 1/3.]
    # [-1., 1.]
    phi = make_orthonormal_discrete_functions(
        [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], abs_tol=1e-10
    )
    assert np.allclose(
        phi,
        np.array(
            [
                [1.0, 1.0, 1.0],
                [-1.22474487, 0.0, 1.22474487],
                [-0.70710678, 1.41421356, -0.70710678],
            ]
        ),
    )
