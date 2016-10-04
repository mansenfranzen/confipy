"""This module contains converter functions."""

class DotNotation(object):
    """Enables dot notation for accessing config properties. This class does
    not inherit from dict on purpose in order to prevent namespace clashes.
    Therefore, only operator overloading methods are used which are unlikely
    to clash with variable names from config files.

    """

    def __setitem__(self, key, value):
        """Support bracketing attribute setting."""
        setattr(self, key, value)

    def __call__(self, ret="val", key=None, default=None):
        """Return specific attributes of the DotNotation instance.

        Parameters
        ----------
        ret: {"val", "dot", "dict", "get"}
            Define the return value. 'val' refers to attributes which are not
            DotNotation instances (therefore being str/lists by default).
            'dot' refers to attributes which are DotNotation instances. 'dict'
            provides the possibility to return itself as a dictionary. 'get'
            mimics the default dict.get() method. It returns the attribute if
            present. Otherwise returns the 'default' parameter.

        """

        if ret == "val":
            return {key: value for key, value in vars(self).items()
                    if not isinstance(value, DotNotation)}

        elif ret == "dot":
            return {key: value for key, value in vars(self).items()
                    if isinstance(value, DotNotation)}

        elif ret == "dict":
            res_dict = {}
            for key, value in vars(self).items():
                if isinstance(value, self.__class__):
                    res_dict[key] = value("dict")
                    continue
                res_dict[key] = value
            return res_dict

        elif ret == "get":
            if hasattr(self, key):
                return getattr(self, key)
            else:
                return default


    def __repr__(self):
        """Return string representation."""
        tpl = "CfgNode: {} nodes ({}) / {} values ({})"
        nodes = self("dot").keys()
        values = self("val").keys()
        return tpl.format(len(nodes), nodes, len(values), values)


def _unflat_dict(flat_dict, unflat_dict=None, default_type=dict):
    """Convert flattened dict back to nested dict structure.

    Parameters
    ----------
    flat_dict: dict
        See _flatten_dict() for more information.
    unflat_dict: None, dict
        Parameter is used as parent dictionary.

    Return
    ------
    unflattend_dict: dict

    """
    print(flat_dict)
    if not unflat_dict:
        unflat_dict = default_type()

    # iterate, begin with lowest depth
    sorted_items = sorted(flat_dict.items(), key=lambda x: len(x[0]))
    for key_chain, value in sorted_items:
        this_key = key_chain[0]
        # directly set value, if only one key is present
        if len(key_chain)== 1:
            unflat_dict[this_key] = value
            continue

        # if key exists, do not create again
        try:
            key_exists = unflat_dict.get(this_key)
        except AttributeError:
            key_exists = unflat_dict("get", this_key)

        if key_exists:
            _unflat_dict({key_chain[1:]: value}, key_exists, default_type)
            continue

        unflat_dict[this_key] = _unflat_dict({key_chain[1:]: value},
                                             default_type=default_type)

    return unflat_dict


def _flat_dict(cfg_dict, parent=None):
    """Convert nested dictionary into flattened dict of key-chain
    value pairs where the key-chain is a tuple of nested keys.

    For example, {"key1": {"key11":{"key111": "value1"}}}
    evaluates to  {("key1", "key11", "key111"): "value1"}.

    Simplifies dictionary operations for other parser functions.

    Parameters
    ----------
    cfg_dict: dict
        Dictionary containing config data.
    parent: None, optional
        For nested, recursive calls remembers the parent of current level.

    Return
    ------
    flattened: dict

    """

    if not parent:
        parent = []

    flattened = {}
    for key, value in cfg_dict.items():
        key_level = parent + [key]
        if isinstance(value, dict):
            flattened.update(_flat_dict(value, key_level))
        else:
            key_chain = tuple(key_level)
            flattened[key_chain] = value

    return flattened