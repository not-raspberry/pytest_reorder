"""Tests for functionality common for all reordering algorithms."""
import pytest
from pytest_reorder import (
    unpack_test_ordering, make_reordering_hook,
    EmptyTestsOrderList, UndefinedUnmatchedTestsOrder
)


@pytest.mark.parametrize('function', [
    unpack_test_ordering,
    make_reordering_hook
])
def test_bad_ordering(function):
    """Check what happens when a malformed list is passed to the function."""
    with pytest.raises(EmptyTestsOrderList):
        function([])

    with pytest.raises(UndefinedUnmatchedTestsOrder):
        function(['sth', 'sth_else', 'etc'])
