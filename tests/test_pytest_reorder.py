"""Pytest-reorder test suite."""
import pytest
import subprocess
from mock import Mock
from pytest_reorder import (
    default_reordering_hook, unpack_test_ordering, make_reordering_hook,
)
from pytest_reorder.reorder import (
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


@pytest.mark.parametrize('test_names, expected_test_order', [
    ([
      'tests/test_sample.py',
      'tests/integration/test_some_integration.py',
      'tests/ui/test_some_ui.py',
      'tests/unit/test_some_unit.py',
     ],
     [
      'tests/unit/test_some_unit.py',
      'tests/test_sample.py',
      'tests/integration/test_some_integration.py',
      'tests/ui/test_some_ui.py',
     ]),

    (['test_other.py', 'test_integration.py', 'test_ui.py', 'test_unit.py'],
     ['test_unit.py', 'test_other.py', 'test_integration.py', 'test_ui.py']),

    # Tests deeply nested:
    ([
      'users/tests/test_sample.py',
      'users/tests/test_ui.py',
      'users/tests/integration/test_some_integration.py',
      'accounts/tests/ui/test_some_ui.py',
      'stats/tests/unit/test_some_unit.py',
     ],
     [
      'stats/tests/unit/test_some_unit.py',
      'users/tests/test_sample.py',
      'users/tests/integration/test_some_integration.py',
      'users/tests/test_ui.py',
      'accounts/tests/ui/test_some_ui.py',
     ]),

    # No common prefix:
    (['other/test_sth.py', 'integration/test_sth.py', 'ui/test_sth.py', 'unit/test_sth.py'],
     ['unit/test_sth.py', 'other/test_sth.py', 'integration/test_sth.py', 'ui/test_sth.py']),

    # No integration tests:
    (['test_other.py', 'test_ui.py', 'test_unit.py'],
     ['test_unit.py', 'test_other.py', 'test_ui.py']),

    # No other (name not matched) tests:
    (['test_integration.py', 'test_ui.py', 'test_unit.py'],
     ['test_unit.py', 'test_integration.py', 'test_ui.py']),

    # No ui tests:
    (['test_other.py', 'test_integration.py', 'test_unit.py'],
     ['test_unit.py', 'test_other.py', 'test_integration.py']),

    # No unit tests:
    (['test_other.py', 'test_integration.py', 'test_ui.py'],
     ['test_other.py', 'test_integration.py', 'test_ui.py']),

    # No tests at all:
    ([], []),
])
def test_reordering_default(test_names, expected_test_order):
    """Call library's ``pytest_collection_modifyitems`` function and check resulting tests order."""
    test_items = [Mock(nodeid=test_name) for test_name in test_names]

    default_reordering_hook(None, None, test_items)

    reordered_test_names = [item.nodeid for item in test_items]
    assert reordered_test_names == expected_test_order


def test_reordering_custom_test_order():
    """Test reordering with a custom hook."""
    tests_names = [
        'test_suite/test_aaa.py',
        'test_suite/test_bbb.py',
        'test_suite/test_ccc.py',
        'test_suite/test_fff.py',
    ]
    test_items = [Mock(nodeid=test_name) for test_name in tests_names]

    reorder_hook = make_reordering_hook(['.*/test_c', '.*/test_b', '.*/test_a', None])
    reorder_hook(None, None, test_items)
    reordered_test_names = [item.nodeid for item in test_items]

    assert reordered_test_names == [
        'test_suite/test_ccc.py',
        'test_suite/test_bbb.py',
        'test_suite/test_aaa.py',
        'test_suite/test_fff.py',
    ]


@pytest.mark.parametrize('pytest_invocation, expected_test_order', [
    (
        ['py.test', 'tests/sample_test_suites/flat/'],
        [
            b'tests/sample_test_suites/flat/unit/test_some_unit.py',
            b'tests/sample_test_suites/flat/test_sample.py',
            b'tests/sample_test_suites/flat/integration/test_some_integration.py',
            b'tests/sample_test_suites/flat/ui/test_some_ui.py',
        ]
    ),
    (
        ['py.test', 'tests/sample_test_suites/nested/'],
        [

            b'tests/sample_test_suites/nested/app_1/tests/unit/test_some_unit.py',
            b'tests/sample_test_suites/nested/app_2/tests/test_unit.py',
            b'tests/sample_test_suites/nested/app_2/tests/test_sth.py',
            b'tests/sample_test_suites/nested/app_1/tests/integration/test_some_integration.py',
            b'tests/sample_test_suites/nested/app_1/tests/ui/test_some_ui.py',
        ]
    ),
    (
        # No `--reorder` argument - no reordering.
        ['py.test', 'tests/sample_test_suites/flat_hook_not_imported/'],
        [
            b'tests/sample_test_suites/flat_hook_not_imported/test_sample.py',
            b'tests/sample_test_suites/flat_hook_not_imported/integration/test_some_integration.py',
            b'tests/sample_test_suites/flat_hook_not_imported/ui/test_some_ui.py',
            b'tests/sample_test_suites/flat_hook_not_imported/unit/test_some_unit.py',
        ]
    ),
    (
        # `--reorder` with no extra args default order.
        ['py.test', 'tests/sample_test_suites/flat_hook_not_imported/', '--reorder'],
        [
            b'tests/sample_test_suites/flat_hook_not_imported/unit/test_some_unit.py',
            b'tests/sample_test_suites/flat_hook_not_imported/test_sample.py',
            b'tests/sample_test_suites/flat_hook_not_imported/integration/test_some_integration.py',
            b'tests/sample_test_suites/flat_hook_not_imported/ui/test_some_ui.py',
        ]
    ),
    (
        # `--reorder` with no custom ordering.
        [
            'py.test', 'tests/sample_test_suites/flat_hook_not_imported/',
            '--reorder', '*', '(test_|.*/)unit', '(test_|.*/)ui', '(test_|.*/)integration',
        ],
        [
            b'tests/sample_test_suites/flat_hook_not_imported/test_sample.py',
            b'tests/sample_test_suites/flat_hook_not_imported/unit/test_some_unit.py',
            b'tests/sample_test_suites/flat_hook_not_imported/ui/test_some_ui.py',
            b'tests/sample_test_suites/flat_hook_not_imported/integration/test_some_integration.py',
        ]
    ),
])
def test_reordering_invoke_test_suite(pytest_invocation, expected_test_order):
    """Check the order of a sample test suite, invoked in a separate process."""
    output = subprocess.check_output(pytest_invocation)
    lines_with_test_modules = [line for line in output.split(b'\n')
                               if line.startswith(b'tests/sample_test_suites/')]
    test_modules = [line.split()[0] for line in lines_with_test_modules]
    assert test_modules == expected_test_order


def test_commandline_reorder_option_no_unmatched_tests_order():
    """Test invoking pytest with the '--reorder' option."""
    with pytest.raises(subprocess.CalledProcessError) as bad_call:
        subprocess.check_output([
            'py.test', 'tests/sample_test_suites/flat_hook_not_imported/',
            '--reorder', 'match_a', 'match_b', 'match_c',
        ])

    assert (b'UndefinedUnmatchedTestsOrder: The list does not specify the order of unmatched tests.'
            in bad_call.value.output)
