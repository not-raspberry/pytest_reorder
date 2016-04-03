"""A pre-specified hook to reorder functions and its building blocks."""
from functools import reduce


DEFAULT_ORDER = ('unit', None, 'integration', 'ui')  # None - no prefix matched.


class PytestReorderError(Exception):
    """Raised when trying to make a reorder hook with wrong arguments."""


class EmptyTestsOrderList(PytestReorderError):
    """Raised when the passed list defining tests order is empty."""


class UndefinedUnmatchedTestsOrder(PytestReorderError):
    """Raised when the list defining tests order does not specify the order for unmatched tests."""


def get_common_prefix(s1, s2):
    """
    Return common prefix of the strings.

    :param str s1:
    :param str s2:
    :return: common prefix of s1 and s2, possibly an empty string
    :rtype: str
    """
    for i in range(1, min(len(s1), len(s2))):
        if s1[:i] != s2[:i]:
            return s1[:i - 1]

    return s1


def unpack_test_ordering(ordering):
    """
    Build a map of test names substrings to the order of tests that match them.

    >>> unpack_test_ordering(['a', 'b', None, 'k'])
    ({'a': 0, 'b': 1, 'k': 3}, 2)

    :param list ordering: a list of substrings of test names in desired order,
        One None is required in the list to designate any test not matching any of the strings.
    :raise EmptyTestsOrderList:
    :raise UndefinedUnmatchedTestsOrder:
    :rtype: tuple
    :return: 2-tuple of a mapping of substrings to their positions in ordering and an int of
        the position of the tests that don't match any of the substrings.
    """
    if len(ordering) == 0:
        raise EmptyTestsOrderList('The ordering list is empty.')

    substring_to_order = {substring: index for index, substring in enumerate(ordering)
                          if substring is not None}
    try:
        unmatched_order = ordering.index(None)
    except ValueError:
        raise UndefinedUnmatchedTestsOrder(
            'The list does not specify the order of unmatched tests.')

    return substring_to_order, unmatched_order


def make_flat_reordering_hook(prefixes_order):
    """
    Given a list of ordered prefixes, return a reorder hook to arrange the tests in that order.

    The tests names will be stripped from the common prefix, leaving out the varying parts:

        'tests/unit...', 'tests/integration/...' -> 'unit...', 'integration/...'
        (common prefix - 'tests/')

    The tests will be sorted depending on what their varying parts start with.
    The ``prefixes_order`` list specifies how to arrange the tests. This list should contain
    prefixes of the varying parts in desired order and None for unmatched tests.

    :param list prefixes_order: a list of prefixes of varying parts of test names in desired order,
        as strings.  One None is required in the list to designate any test not matched with any of
        the prefixes.  E.g. ['unit', None, 'db', 'integration', 'webqa'] - this makes tests with
        varying parts of names beginning with 'unit' run first, then unmatched, then 'db', etc.
    :raise EmptyTestsOrderList:
    :raise UndefinedUnmatchedTestsOrder:
    :rtype: function
    :return: a valid ``pytest_collection_modifyitems`` hook to reorder collected tests
    """
    prefix_to_order, unmatched_order = unpack_test_ordering(prefixes_order)

    def pytest_collection_modifyitems(session, config, items):
        """Reorder tests according to the list %r.""" % (prefixes_order,)
        if items == []:
            return

        nodeids = [i.nodeid for i in items]
        common_prefix = reduce(get_common_prefix, nodeids)

        def sort_key(item):
            """
            Get the sort key for tests reordering.

            The key depends exclusively on the prefix. Therefore all strings with varying parts
            starting with the same prefix will have the same key. This is OK, since ``list.sort``
            is stable.

            :rtype: int
            :return sort key dependent on the test prefix; integer starting from zero
            """
            varying_nodeid_part = item.nodeid[len(common_prefix):]
            for prefix, order in prefix_to_order.items():
                if varying_nodeid_part.startswith(prefix):
                    return order
            return unmatched_order

        items.sort(key=sort_key)

    return pytest_collection_modifyitems


default_flat_reordering_hook = make_flat_reordering_hook(DEFAULT_ORDER)
