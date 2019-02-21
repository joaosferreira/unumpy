import itertools
import typing

import hypothesis

from .arrays import *
from .naturals import *
from .naturals_test import naturals
from .vectors import *
from .vectors_test import assert_vector_is_list, list_of_naturals
from ..dispatch import *

T_box = typing.TypeVar("T_box", bound=Box)


def assert_arrays_eql(array: Array[T_box], shape: typing.List[int], content):
    """
    Asserts that the `array` has a certain shape and content, where the contentt
    is nested python lists.
    """
    array = replace(array)
    assert_vector_is_list(replace(array.shape), list(map(Natural, shape)))
    for indxs in itertools.product(*map(range, shape)):
        x = content
        for i in indxs:
            x = x[i]
        assert replace(array[Array.create_shape(*map(Natural, indxs))]) == x


@hypothesis.given(naturals())
def test_0d_array(x):
    assert_arrays_eql(Array.create_0d(x), [], x)


@hypothesis.given(list_of_naturals())
def test_1d_array(xs):
    assert_arrays_eql(Array.create_1d(Natural(), *xs), [len(xs)], xs)


@hypothesis.given(list_of_naturals())
def test_vec_to_array(xs):
    assert_arrays_eql(Array.from_vec(Vec.create_args(Natural(), *xs)), [len(xs)], xs)


@hypothesis.given(list_of_naturals())
def test_array_to_vec(xs):
    assert_vector_is_list(Array.create_1d(Natural(), *xs).to_vec(), xs)