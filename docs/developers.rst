Information for developers
==========================

Dependencies
------------

Install the development dependencies::

   sudo apt install python3-nose2 python3-nose2-cov python3-sphinx

Tests
-----

To run the tests::

   PYTHONPATH=. make test

Development mode
----------------

To install the package in development mode, you can use::

   pip3 install -e .
