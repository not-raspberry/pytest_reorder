"""Pytest-reorder test suite."""
import pytest
import subprocess
from mock import Mock
from pytest_reorder import get_common_prefix, pytest_collection_modifyitems


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
def test_reordering(test_names, expected_test_order):
    """Call library's ``pytest_collection_modifyitems`` function and check resulting tests order."""
    test_items = [Mock(nodeid=test_name) for test_name in test_names]

    pytest_collection_modifyitems(None, None, test_items)

    reordered_test_names = [item.nodeid for item in test_items]
    assert reordered_test_names == expected_test_order


def test_invoke_test_suite():
    """Check the order of a sample test suite, invoked in a separate process."""
    output = subprocess.check_output(['py.test', 'sample_test_suite'])
    lines_with_test_modules = [line for line in output.split('\n')
                               if line.startswith('sample_test_suite/')]
    test_modules = [line.split()[0] for line in lines_with_test_modules]
    assert test_modules == [
        'sample_test_suite/unit/test_some_unit.py',
        'sample_test_suite/test_sample.py',
        'sample_test_suite/integration/test_some_integration.py',
        'sample_test_suite/ui/test_some_ui.py',
    ]
