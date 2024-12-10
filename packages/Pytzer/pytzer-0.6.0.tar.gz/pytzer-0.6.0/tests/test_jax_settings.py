from jax import numpy as np


def test_jax_double_precision():
    """Does JAX have double precision enabled?"""
    x = np.array(1.0)
    assert x.dtype is np.dtype("float64")


# test_jax_double_precision()
