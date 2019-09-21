=====
rstxt
=====

|Build Status| |PyPI version| |PyPI| |codecov| |black|

Extract text from reStructuredText.

Install
-------

Install with pip::

   pip install rstxt

Usage
-----

After installing you can run ``rstxt`` from the command line::

   $ rstxt --help
   Usage: rstxt [OPTIONS] [FILES]...

     Extract text from reStructuredText.

   Options:
     --help                 Show this message and exit.

For example, to extract text from all rst files contained in a directory (fish shell)::

   rstxt **.rst

Text can also be piped in::

   cat README.rst | rstxt

Use this to spell check reStructuredText::

   rstxt **.rst | hunspell -d en_US -l

.. |Build Status| image:: https://travis-ci.org/jwkvam/rstxt.svg?branch=master
   :target: https://travis-ci.org/jwkvam/rstxt
.. |PyPI version| image:: https://badge.fury.io/py/rstxt.svg
   :target: https://badge.fury.io/py/rstxt
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/rstxt.svg
   :target: https://pypi.python.org/pypi/rstxt/
.. |codecov| image:: https://codecov.io/gh/jwkvam/rstxt/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jwkvam/rstxt
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
