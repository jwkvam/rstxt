========
spellrst
========

|Build Status| |PyPI version| |PyPI| |codecov| |black|

Spell check reStructuredText.

Install
-------

Install with pip::

   pip install spellrst

And download the `spaCy model <https://spacy.io/models>`__ you want to use e.g. ``en_core_web_md``::

   python -m spacy download en_core_web_md

Usage
-----

After installing you can run ``spellrst`` from the command line::

   $ spellrst --help
   Usage: spellrst [OPTIONS] [FILES]...

     Spell check reStructuredText.

   Options:
     -d, --dictionary TEXT  spaCy language model (spacy.io/models), e.g.
                            en_core_web_md
     -c, --config TEXT      Configuration file for a whitelist e.g. spellrst.toml
     --help                 Show this message and exit.

For example, to check all rst files contained in a directory (fish)::

   spellrst **.rst

Whitelist
---------

Add a whitelist

.. |Build Status| image:: https://travis-ci.org/jwkvam/spellrst.svg?branch=master
   :target: https://travis-ci.org/jwkvam/spellrst
.. |PyPI version| image:: https://badge.fury.io/py/spellrst.svg
   :target: https://badge.fury.io/py/spellrst
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/spellrst.svg
   :target: https://pypi.python.org/pypi/spellrst/
.. |codecov| image:: https://codecov.io/gh/jwkvam/spellrst/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jwkvam/spellrst
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
