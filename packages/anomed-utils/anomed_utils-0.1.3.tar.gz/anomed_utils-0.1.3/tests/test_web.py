import numpy as np
import pytest

from anomed_utils import web


@pytest.fixture()
def empty_array():
    return np.array([])


@pytest.fixture()
def int_array():
    return np.arange(10)


@pytest.fixture()
def float_array():
    return np.arange(10) + 0.5


@pytest.fixture()
def object_array():
    return np.array(3 * ["foo", "bar", "baz"])


def test_array_to_bytes_conversion(empty_array, int_array, float_array, object_array):
    expected_result = dict(
        empty=empty_array, ints=int_array, floats=float_array, objs=object_array
    )
    result = web.bytes_to_named_ndarrays(web.named_ndarrays_to_bytes(expected_result))
    assert expected_result.keys() == result.keys()
    for key in expected_result.keys():
        assert np.array_equal(expected_result[key], result[key])
