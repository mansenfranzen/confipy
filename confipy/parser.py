"""This module contains the config parser functions."""

import os
import confipy.reader

ERR_CFG_NOT_FOUND = "Cannot find referenced config '{}'."


def _flatten_dict(cfg_dict, parent=None):
    """Convert nested dictionary into a flattened dict of key-chain
    value pairs where the key-chain is a tuple of nested keys.

    For example, {"key1": {"key11":{"key111": "value1"}}}
    evaluates to  {("key1", "key11", "key111"): "value1"}.

    By doing so, other functions can operate on a non-nested dictionary more
    easily.

    Parameters
    ----------
    cfg_dict: dict
        Dictionary containing config data.
    parent: None, optional
        For nested, recursive calls, remembers the parent the current level
        originated from.

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
            flattened.update(_flatten_dict(value, key_level))
        else:
            key_chain = tuple(key_level)
            flattened[key_chain] = value

    return flattened


def include(flattened_dict, source_path, marker="$include"):
    """Scan config dictionary for include statements. Load and insert
    referenced config files under corresponding keys namespace.

    Parameters
    ----------
    flattened_dict: dict
        Flattened dictionary containing config data.
    source_path: str
        Path to original config file.

    Return
    ------
    parsed_dict: dict

    """

    cwd = os.path.dirname(source_path)
    parsed_dict = {}

    for key_chain, value in flattened_dict.items():
        if not value.startswith(marker):
            parsed_dict[key_chain] = value
            continue

        absolute_path = value.replace(marker, "").lstrip().rstrip()
        relative_path = os.path.join(cwd, absolute_path)

        if os.path.exists(relative_path):
            path = relative_path
        elif os.path.exists(absolute_path):
            path = absolute_path
        else:
            raise AssertionError(ERR_CFG_NOT_FOUND.format(absolute_path))

        include_cfg = confipy.reader.read_config(path)
        include_flattened = _flatten_dict(include_cfg, list(key_chain))
        include_included = include(include_flattened, path)
        parsed_dict.update(include_included)


    return parsed_dict


def substitute(to_parse, parsed=None, splitter=" + ", marker="$"):
    """Find keys identified by splitter and marker signs. Only values
    containing the splitter are taken into account. Splitted values must have
    keys which begin with the marker sign. Otherwise, keys are ignored.

    Function calls itself recursively until to_parse is empty.

    Parameters
    ----------
    to_parse: dict
        Dictionary with items to be parsed.
    parsed: dict
        Dictionary with valid lookup items for substitution usage.
    splitter: str
        The splitter to identify possible keys.
    marker: str
        The marker to identify correct keys.

    Return
    ------
    parsed: dict

    """

    # return result if to_parse is empty
    if not to_parse:
        return parsed

    # if there's nothing yet, find all non-subs items
    if not parsed:
        parsed = {key:value for key, value in to_parse.items()
                  if not _contains(value, splitter)}
        to_parse = {key: value for key, value in to_parse.items()
                    if key in set(parsed) ^ set(to_parse)}

    # iterate items to be parsed; distinguish strings and lists
    for key, value in to_parse.copy().items():
        if isinstance(value, str):
            valid = _substitue_value(value, parsed, splitter, marker)
        else:
            valid = []
            for element in value:
                if not _contains(element, splitter):
                    valid.append(element)
                    continue

                complete = _substitue_value(element, parsed, splitter, marker)
                if not complete:
                    valid = False
                    break
                valid.append(complete)
        if valid:
            del to_parse[key]
            parsed[key] = valid

    return substitute(to_parse, parsed)


def _substitue_value(value, parsed, splitter, marker):
    """Substitute keys of a singular string. Returns False if one key could
    not successfully be replaced.

    Parameters
    ----------
    value: str
        String value containing keys to be substituted.
    parsed: dict
        Dictionary with valid lookup items for substitution usage.
    splitter: str
        The splitter to identify possible keys.
    marker: str
        The marker to identify correct keys.

    Return
    ------
    parsed_item: str, None

    """

    parsed_item = ""
    for part in value.split(splitter):
        if not part.startswith(marker):
            parsed_item += part
            continue

        key_chain = _convert_key_chain(part[1:])
        parsed_value = parsed.get(key_chain)

        if not parsed_value:
            return False

        parsed_item += parsed_value

    return parsed_item


def _contains(values, splitter):
    """Check presence of marker in values.

    Parameters
    ----------
    values: str, iterable
        Either a single value or a list of values.
    splitter: str
        The target to be searched for.

    Return
    ------
    boolean

    """

    if isinstance(values, str):
        values = (values,)

    if any([splitter in x for x in values]):
        return True
    else:
        return False


def _convert_key_chain(key_string):
    """Convert dot notation to tupled key chain notation"""

    return tuple(key_string.split("."))
