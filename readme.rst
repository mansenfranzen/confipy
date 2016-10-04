.. image:: https://coveralls.io/repos/github/mansenfranzen/confipy/badge.svg
    :target: https://coveralls.io/github/mansenfranzen/confipy

.. image:: https://travis-ci.org/mansenfranzen/confipy.svg?branch=master
    :target: https://travis-ci.org/mansenfranzen/confipy

confipy
=======
A convenient config file reader

Why confipy?
============
Pythons configparser lacks builtin list and nested data support.
YAML and json lack variable substitution and the including of referenced config files.

confipy reads YAML, configparser and json files while adding support for variable substitution and the automatic insertion of referenced config files.
confipy supports config objects with dot notation instead of bracketing access.
