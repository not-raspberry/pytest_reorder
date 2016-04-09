"""A hook to add the '--reorder' argument to py.test."""
from pytest_reorder import DEFAULT_ORDER, make_reordering_hook


def pytest_addoption(parser):
    """Add the '--reorder' argument to the py.test invocation."""
    group = parser.getgroup('tests reordering', 'reordering', after='general')
    group.addoption(
        '--reorder', type=str, nargs='*',
        help=(
            "A list of regular expressions matching test nodeids and one '*' to specify the order "
            'of unmatched tests. The tests will be reordered according to these specs. If no '
            'arguments are passed, default ordering will be applied (unit tests, unmatched tests, '
            'integration tests, ui tests). \n'
            'E.g. `--reorder "(^|.*/)(test_)?unit" "*" "(^|.*/)(test_)?db" "(^|.*/)(test_)?web"`.'
         )
    )


def pytest_collection_modifyitems(session, config, items):
    """Reorder tests if the '--reorder' command line option was added."""
    reordering_request = config.getoption('reorder')
    if reordering_request is None:
        return  # Test reordering not requested.
    elif reordering_request == []:
        ordering = DEFAULT_ORDER
    else:
        # An asterisk means 'unmatched tests'. Replace it with None for `make_reordering_hook`.
        ordering = [s if s != '*' else None for s in reordering_request]

    hook = make_reordering_hook(ordering)
    hook(session, config, items)
