.. image:: https://coveralls.io/repos/github/mansenfranzen/confipy/badge.svg
    :target: https://coveralls.io/github/mansenfranzen/confipy

.. image:: https://travis-ci.org/mansenfranzen/confipy.svg?branch=master
    :target: https://travis-ci.org/mansenfranzen/confipy

What is confipy?
================
confipy is a convenient config file reader which supports different formats including yaml, json and cfg/ini. In addition, it provides optional dot notation access for better readability.

Why use confipy?
================
Python's builtin configparser package falls short on list and nested data structures support.

Json and yaml files are excellent in this regard. However, you may require **string concatenation** and **config files composition**. Both, python's builtin json module and the PyYAML package do not meet these requirements out of the box.

Confipy is a simple wrapper around these packages to provide this functionality, as described below:

String concatenation:
    It is a common use case to define file system paths for configurational purposes. Let's say you have a base path like */home/user/* which defines the root of a project. All project relevant files are relative to the project's root and should therefore automatically be prepended with the base path:

    **Plain YAML**: ::
    
        base: /home/user/
        images: /home/user/images/
        downloads: /home/user/downloads/
        python: /home/user/python/

    **Confipy YAML**: ::

        base: /home/user/
        images: $base + images/
        downloads: $base + downloads/
        python: $base + python/


Config files composition:
    Complex and large configs are more readable when partitioned into smaller config files with concrete responsibilites. However, you don't want to load all different config files but rather just one index config file that includes references to other configs.

    **index.yaml**: ::

        base: /home/user/
        paths: $include paths.yaml

    **paths.yaml**: ::

        images: $base + images/
        downloads: $base + downloads/
        python: $base + python/


    You only need to load the index.yaml. The paths.yaml is automatically included under the *paths* namespace. Note that the referenced paths.yaml is able to access the ``base`` attribute of the index.yaml.

Basic Usage
===========
Using confipy is straightforward. Consider the above example for the following show case: ::

    import confipy
    cfg = confipy.load("index.yaml")
    path_default = cfg["paths"]["images"] # using default bracketing access
    path_confipy = cfg.paths.images # using confipy's convenient dot notation
    
    print(path_default) # "/home/user/images"
    print(path_default == path_confipy) # True


 
 
