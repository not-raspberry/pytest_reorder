pytest_reorder |status| |version| |pythons| |coverage|
======================================================

.. |status| image:: https://travis-ci.org/not-raspberry/pytest_reorder.svg?branch=master
    :target: https://travis-ci.org/not-raspberry/pytest_reorder

.. |version| image:: https://img.shields.io/pypi/v/pytest_reorder.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/pytest-reorder

.. |pythons| image:: https://img.shields.io/pypi/pyversions/pytest_reorder.svg?maxAge=2592000

.. |coverage| image:: https://coveralls.io/repos/github/not-raspberry/pytest_reorder/badge.svg?branch=master
    :target: https://coveralls.io/github/not-raspberry/pytest_reorder?branch=master

Reorder tests depending on their nodeids (strings of test file path plus test name plus
parametrization, like:
``test/test_prefix_reordering.py::test_reordering_default[test_names5-expected_test_order5]``).

Normally tests are sorted alphabetically. That makes integration tests run before unit tests.

With **pytest_reorder** you can install a hook that will change the order of tests in the suite.
By default **pytest_reorder** will seek for *unit*, *integration* and *ui* tests and put them in
the following order:

#. *unit*
#. all tests with names not indicating unit, integration, nor UI tests
#. *integration*
#. *ui*

The default regular expressions can find unit, integration and UI tests both laid flat and **deeply
nested**. You can also specify your custom order.


HOWTO
-----

It's possible to customize the ordering. To do so, you have to specify your custom tests order
by passing a list of regular expresions that match tests' nodeids. If more than one regex matches
some test nodeid, the first one wins.

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

**pytest_reorder** hooks in a ``--reorder`` command line option that takes zero arguments or an
ordering spec list.

#. If no arguments are given, default reordering will be applied.
#. If a list is passed, e.g. ``--reorder '(^|.*/)(test_)?unit' '*' '(^|.*/)(test_)?web'``, tests
   are reordered to go as the matches in the list do. Regular list items are treated as Python
   regexes. The special ``'*'`` match is required and specifies where to put tests that don't
   match any of the regexes. A single asterisk was chosen for that because it's not a valid regular
   expression.

Programmatic interface
~~~~~~~~~~~~~~~~~~~~~~

Modify your main conftest file (e.g. ``tests/conftest.py``) to include:

.. code:: python

    from pytest_reorder import default_reordering_hook as pytest_collection_modifyitems  # add noqa here if you use pyflakes

or specify a custom test order:

.. code:: python

    from pytest_reorder import make_reordering_hook
    # Make unit tests run before 'db' tests, which run before 'web' tests. Other tests will run at
    # the very beginning of the suite:
    pytest_collection_modifyitems = make_reordering_hook(
        [None, r'(^|.*/)(test_)?unit', r'(^|.*/)(test_)?db', r'(^|.*/)(test_)?web'])


Without pytest_reorder
----------------------

Flat:

.. code::

    sample_test_suites/flat/test_sample.py ...
    sample_test_suites/flat/integration/test_some_integration.py ..
    sample_test_suites/flat/ui/test_some_ui.py .
    sample_test_suites/flat/unit/test_some_unit.py ..


Nested:

.. code::

    sample_test_suites/nested/app_1/tests/integration/test_some_integration.py ..
    sample_test_suites/nested/app_1/tests/ui/test_some_ui.py .
    sample_test_suites/nested/app_1/tests/unit/test_some_unit.py ..
    sample_test_suites/nested/app_2/tests/test_sth.py ...
    sample_test_suites/nested/app_2/tests/test_unit.py .


With pytest_reorder
-------------------

Flat:

.. code::

    sample_test_suites/flat/unit/test_some_unit.py ..
    sample_test_suites/flat/test_sample.py ...
    sample_test_suites/flat/integration/test_some_integration.py ..
    sample_test_suites/flat/ui/test_some_ui.py .


Nested:

.. code::

    sample_test_suites/nested/app_1/tests/unit/test_some_unit.py ..
    sample_test_suites/nested/app_2/tests/test_unit.py .
    sample_test_suites/nested/app_2/tests/test_sth.py ...
    sample_test_suites/nested/app_1/tests/integration/test_some_integration.py ..
    sample_test_suites/nested/app_1/tests/ui/test_some_ui.py .
