pytest_reorder |status|
=======================

.. |status| image:: https://travis-ci.org/not-raspberry/pytest_reorder.svg?branch=master
    :target: https://travis-ci.org/not-raspberry/pytest_reorder

Reorder tests depending on their paths.

Normally tests are sorted alphabetically. That makes integration tests run before unit.

With **pytest_reorder** you can install a hook that will change the order of tests in the suite.
By default **pytest_reorder** will seek for *unit*, *integration* and *ui* tests and put them in
the following order:

#. *unit*
#. all tests with names beginning with something else
#. *integration*
#. *ui*

The default regular expressions can find unit, integration and UI tests both laid flat and deeply
nested. You can also specify your custom order.


Pythons supported
-----------------
CPythons 2.7, 3.2, 3.3, 3.4, 3.5, 3.5-dev, nightly. PyPy and PyPy3.

HOWTO
-----

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

Passed regular expressions match tests' nodeids strings py.test displays for each test case - like
``test/test_prefix_reordering.py::test_reordering_default[test_names5-expected_test_order5]``.
If more than one regex matches one test, the first one wins.


Without pytest_reorder
----------------------

.. code::

    sample_test_suites/flat/test_sample.py ...
    sample_test_suites/flat/integration/test_some_integration.py ..
    sample_test_suites/flat/ui/test_some_ui.py .
    sample_test_suites/flat/unit/test_some_unit.py ..

.. code::

    sample_test_suites/nested/app_1/tests/integration/test_some_integration.py ..
    sample_test_suites/nested/app_1/tests/ui/test_some_ui.py .
    sample_test_suites/nested/app_1/tests/unit/test_some_unit.py ..
    sample_test_suites/nested/app_2/tests/test_sth.py ...
    sample_test_suites/nested/app_2/tests/test_unit.py .


With pytest_reorder
-------------------

.. code::

    sample_test_suites/flat/unit/test_some_unit.py ..
    sample_test_suites/flat/test_sample.py ...
    sample_test_suites/flat/integration/test_some_integration.py ..
    sample_test_suites/flat/ui/test_some_ui.py .

.. code::

    sample_test_suites/nested/app_1/tests/unit/test_some_unit.py ..
    sample_test_suites/nested/app_2/tests/test_unit.py .
    sample_test_suites/nested/app_2/tests/test_sth.py ...
    sample_test_suites/nested/app_1/tests/integration/test_some_integration.py ..
    sample_test_suites/nested/app_1/tests/ui/test_some_ui.py .
