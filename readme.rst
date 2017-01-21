.. image:: https://coveralls.io/repos/github/mansenfranzen/confipy/badge.svg
    :target: https://coveralls.io/github/mansenfranzen/confipy

.. image:: https://travis-ci.org/mansenfranzen/confipy.svg?branch=master
    :target: https://travis-ci.org/mansenfranzen/confipy

What is confipy?
================
confipy is a convenient config file reader which supports different formats including yaml, json and cfg/ini.

Why use confipy?
================
Python's builtin configparser package falls short on list and nested data structures support.

Json and yaml files are excellent in this regard. However, one may require variable substitution and the including of other config files. Both, python's builtin json and the 3rd library pyyaml packages do not meet this requirement.

Confipy is a simple wrapper around those great packages to support variable substitution and the including of other config files, as described below:

Variable substitution:
    It is a common use case to define paths for configurational purposes. Let's say you have a base path like */home/user/* which defines the root of a project. All project relevant files are relative to the project's root and should therefore automatically be prepended with the base path:

    **Plain YAML**
    .. code::
        base: /home/user/
        images: /home/user/images/
        downloads: /home/user/downloads/
        python: /home/user/python/

    **Confipy YAML**
    .. code::
        base: /home/user/
        images: $base + images/
        downloads: $base + downloads/
        python: $base + python/


Including config files:
    Complex and large configs are more readable when partioned into smaller config files with concrete responsibilites. However, you don't want to load all different config files but rather just one index config file that includes references to other configs.

    **index.yaml**:
    .. code::
        base: /home/user/
        paths: $include paths.cfg

    **paths.yaml**:
    .. code::
        images: $base + images/
        downloads: $base + downloads/
        python: $base + python/


    Using confipy, you only need to load the index.yaml. The paths.yaml is automatically included via the *paths* namespace. Note that the referenced paths.yaml is able to access the ``base`` attribute of the index.yaml.

Basic Usage
===========
Using confipy is straightforward:
.. code:: python
    import confipy
    cfg = confipy.load("index.yaml")
    path_default = cfg["paths"]["images"] # using default bracketing access
    path_confipy = cfg.paths.images # using confipy's convenient dot notation
 
 
