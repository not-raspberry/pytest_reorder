"""A pre-specified hook to reorder functions and its building blocks."""


ORDER = ['unit', None, 'integration', 'ui']  # None - no prefix matched.


PREFIXES_ORDER = {prefix: index for index, prefix in enumerate(ORDER) if prefix is not None}
UNMATCHED_ORDER = ORDER.index(None)


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


def pytest_collection_modifyitems(session, config, items):
    """Reorder tests according to the ORDER constant."""
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
        varying_nodeid_part = item.nodeid.partition(common_prefix)[-1]
        for prefix, order in PREFIXES_ORDER.iteritems():
            if varying_nodeid_part.startswith(prefix):
                return order
        return UNMATCHED_ORDER

    items.sort(key=sort_key)
