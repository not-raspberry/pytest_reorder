pytest_reorder
==============

Reorder tests depending on their paths.

Normally tests are sorted alphabetically. That makes integration tests run before unit.

With **pytest_reorder** you can install a hook that will change the order of tests in the suite.
By default **pytest_reorder** will seek for *unit*, *integration* and *ui* tests and put them in
the following order:

#. *unit*
#. all tests with names beginning with something else
#. *integration*
#. *ui*

You can also specify your custom order.

**pytest_reorder** assumes the paths of all test modules begin with a common prefix. Most projects
keep their tests in a separate ``tests`` directory and therefore meet this assumption.
The ordering depends on what's left after the prefix is stripped. For details see the docstring and
the code of ``pytest_reorder.make_reordering_hook``.

Django projects that store tests in Django-style 'apps' will not work with pytest-reorder.

HOWTO
-----

Modify your main conftest file (e.g. ``tests/conftest.py``) to include:

.. code:: python

    from pytest_reorder import pytest_collection_modifyitems  # add noqa here if you use pyflakes

or specify a custom test order:

.. code:: python

    from pytest_reorder import make_reordering_hook
    # Make unit tests run before 'db' tests, which run before 'web' tests. Other tests will run at
    # the very beginning of the suite:
    pytest_collection_modifyitems = make_reordering_hook([None, 'unit', 'db', 'web'])


Without pytest_reorder
----------------------

.. code::

    sample_test_suite/test_sample.py ...
    sample_test_suite/integration/test_some_integration.py ..
    sample_test_suite/ui/test_some_ui.py .
    sample_test_suite/unit/test_some_unit.py ..

With pytest_reorder
-------------------

.. code::

    sample_test_suite/unit/test_some_unit.py ..
    sample_test_suite/test_sample.py ...
    sample_test_suite/integration/test_some_integration.py ..
    sample_test_suite/ui/test_some_ui.py .


Status
------

.. image:: https://travis-ci.org/not-raspberry/pytest_reorder.svg?branch=master
    :target: https://travis-ci.org/not-raspberry/pytest_reorder
