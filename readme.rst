confipy
=======
A convenient config file reader

Why confipy?
============
Pythons configparser lacks builtin list and nested data support.
YAML and json lack variable substitution and the including of referenced config files.

confipy reads YAML, configparser and json files while adding support for variable substitution and the automatic insertion of referenced config files.
confipy supports config objects with dot notation instead of bracketing access.