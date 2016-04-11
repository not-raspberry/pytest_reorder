"""A pre-specified hook to reorder test functions and its building blocks."""
import re


# Default regular expressions match varying paths - for example the unit tests re matches:
# tests/unit/...
# test_unit.py
# app/tests/unit/....
# tests/test_unit
# unit
# But won't match (e.g.):
# some_unit
# abc_test_unit
DEFAULT_ORDER = (
    r'(^|.*/)(test_)?unit',
    None,  # None - no match.
    r'(^|.*/)(test_)?integration',
    r'(^|.*/)(test_)?ui',
)


class PytestReorderError(Exception):
    """Raised when trying to make a reorder hook with wrong arguments."""


class EmptyTestsOrderList(PytestReorderError):
    """Raised when the passed list defining tests order is empty."""


class UndefinedUnmatchedTestsOrder(PytestReorderError):
    """Raised when the list defining tests order does not specify the order for unmatched tests."""


def unpack_test_ordering(ordering):
    """
    Build a list of compiled regexes and the order of tests they match; get unmatched tests order.

    >>> unpack_test_ordering(['a.*', 'b.*', None, 'k.*'])
    ([(re.compile(r'a.*'), 0), (re.compile(r'b.*'), 1), (re.compile(r'k.*'), 3)], 2)

    :param list ordering: a list of re strings matching test nodeids in desired order,
        One None is required in the list to specify the position of tests not matching any
        of the regexes.
    :raise EmptyTestsOrderList: if the ``ordering`` list is empty
    :raise UndefinedUnmatchedTestsOrder: if ``ordering`` does not specify the order of unmatched
        tests
    :rtype: tuple
    :return: 2-tuple of a list of tuples of compiled regexes and positions of the tests that match
        them and an int of the position of the tests that don't match any of the regular
        expressions.
    """
    if len(ordering) == 0:
        raise EmptyTestsOrderList('The ordering list is empty.')

    re_to_order = [(re.compile(regex), index) for index, regex in enumerate(ordering)
                   if regex is not None]
    try:
        unmatched_order = ordering.index(None)
    except ValueError:
        raise UndefinedUnmatchedTestsOrder(
            'The list does not specify the order of unmatched tests.')

    return re_to_order, unmatched_order


def make_reordering_hook(ordered_re_strings_matching_tests):
    """
    Given a list of ordered regexps matching tests, return a hook to arrange tests in that order.

    The tests will be sorted depending on which regular expressions they match.
    This list should contain one None for unmatched tests.

    :param list ordered_re_strings_matching_tests: a list of regular expression strings that match
        nodeids of tests (sample nodeid: 'tests/ui/test_some_ui.py::test_something_ui') and one None
        to specify the order of tests that don't match any of the regular expressions.
        E.g.: ``[r'*.unit', None, r'.*integration']`` - will make the hook place unit tests first,
        then unmatched tests, and integration tests at the end.
    :raise EmptyTestsOrderList: if the ``ordered_re_strings_matching_tests`` list is empty
    :raise UndefinedUnmatchedTestsOrder: if ``ordered_re_strings_matching_tests`` does not contain
        one None, thus does not define the order of unmatched tests
    :rtype: function
    :return: a valid ``pytest_collection_modifyitems`` hook to reorder collected tests
    """
    re_to_order, unmatched_order = unpack_test_ordering(ordered_re_strings_matching_tests)

    def pytest_collection_modifyitems(session, config, items):
        """Reorder tests according to the list %r.""" % (ordered_re_strings_matching_tests,)
        def sort_key(item):
            """
            Get the sort key for tests reordering.

            All items matching the same regular expression will get the same key. This is OK since
            `list.sort`` is stable.

            :rtype: int
            :return sort key dependent on the matched regex; integer starting from zero
            """
            for regex, order in re_to_order:
                if regex.match(item.nodeid):
                    return order
            return unmatched_order

        items.sort(key=sort_key)

    return pytest_collection_modifyitems


default_reordering_hook = make_reordering_hook(DEFAULT_ORDER)
