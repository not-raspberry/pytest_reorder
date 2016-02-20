pytest_reorder
==============

Reorder tests depending on their names.

Normally tests are sorted alphabetically. That makes integration tests run before unit.

With pytest_reorder tests with names beginning with *unit* are put first, then others, then
*integration*, then *ui*.


Without pytest_reorder
----------------------

    sample_test_suite/test_sample.py ...
    sample_test_suite/integration/test_some_integration.py ..
    sample_test_suite/ui/test_some_ui.py .
    sample_test_suite/unit/test_some_unit.py ..

With pytest_reorder
-------------------

    sample_test_suite/unit/test_some_unit.py ..
    sample_test_suite/test_sample.py ...
    sample_test_suite/integration/test_some_integration.py ..
    sample_test_suite/ui/test_some_ui.py .


Status
------

.. image:: https://travis-ci.org/not-raspberry/pytest_reorder.svg?branch=master
    :target: https://travis-ci.org/not-raspberry/pytest_reorder
