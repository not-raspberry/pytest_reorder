"""Pytest-reorder test suite."""
import pytest
import subprocess
from mock import Mock
from pytest_reorder import (
    get_common_prefix, default_prefix_reordering_hook,
    make_prefix_reordering_hook,
)


@pytest.mark.parametrize('s1, s2, prefix', [
    ('aaDD', 'aaFF', 'aa'),
    ('aa_aaaDD', 'aa_aaaFF', 'aa_aaa'),
    ('aaab', 'aabb', 'aa'),
    ('aaab', 'zzbb', ''),
    ('aaab', '', ''),
    ('', '', ''),
    ('aaab', 'aaab', 'aaab'),
])
def test_get_common_prefix(s1, s2, prefix):
    """Test common prefix extraction."""
    return get_common_prefix(s1, s2) == prefix


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
def test_prefix_reordering_default(test_names, expected_test_order):
    """Call library's ``pytest_collection_modifyitems`` function and check resulting tests order."""
    test_items = [Mock(nodeid=test_name) for test_name in test_names]

    default_prefix_reordering_hook(None, None, test_items)

    reordered_test_names = [item.nodeid for item in test_items]
    assert reordered_test_names == expected_test_order


def test_prefix_reordering_custom_test_order():
    """Test reordering with a custom hook."""
    tests_names = [
        'test_suite/test_aaa.py',
        'test_suite/test_bbb.py',
        'test_suite/test_ccc.py',
        'test_suite/test_fff.py',
    ]
    test_items = [Mock(nodeid=test_name) for test_name in tests_names]

    reorder_hook = make_prefix_reordering_hook(['c', 'b', 'a', None])
    reorder_hook(None, None, test_items)
    reordered_test_names = [item.nodeid for item in test_items]

    assert reordered_test_names == [
        'test_suite/test_ccc.py',
        'test_suite/test_bbb.py',
        'test_suite/test_aaa.py',
        'test_suite/test_fff.py',
    ]


def test_prefix_reordering_invoke_test_suite():
    """Check the order of a sample test suite, invoked in a separate process."""
    output = subprocess.check_output(['py.test', 'sample_test_suites/flat/'])
    lines_with_test_modules = [line for line in output.split(b'\n')
                               if line.startswith(b'sample_test_suites/flat/')]
    test_modules = [line.split()[0] for line in lines_with_test_modules]
    assert test_modules == [
        b'sample_test_suites/flat/unit/test_some_unit.py',
        b'sample_test_suites/flat/test_sample.py',
        b'sample_test_suites/flat/integration/test_some_integration.py',
        b'sample_test_suites/flat/ui/test_some_ui.py',
    ]
