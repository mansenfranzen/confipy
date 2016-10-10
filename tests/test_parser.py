"""This module contains tests"""

import pytest
import confipy.converter
import confipy.notation
import confipy.reader
import confipy.parser
import os


def get_file(path):
    cur_dir = os.path.dirname(__file__)
    return os.path.join(cur_dir, path)


test_flattened_dict = {("level1", "level2", "level3", "key1"): "value1",
                       ("level1", "level2", "level3", "key2"): "value2"}

test_incl = {("Key1",): "Value1",
             ("Key2", "level1", "level2", "level3", "key1"): "value1",
             ("Key2", "level1", "level2", "level3", "key2"): "value2"}

test_incl_recursive = {("Lvl1", "Key1",): "Value1",
                       ("Lvl1", "Key2", "level1", "level2", "level3",
                        "key1"): "value1",
                       ("Lvl1", "Key2", "level1", "level2", "level3",
                        "key2"): "value2"}

level3 = {"level3": {"key1": "value1", "key2": "value2"}}
test_incl_lvl2_unflattend = {"Lvl1": {"Key1": "Value1",
                                      "Key2": {"level1": {"level2": level3}}}}

test_subs = {("key1",): "value1", ("key2",): "value2",
             ("list1",): ["value1value2", "prevalue1suf"],
             ("lvl1", "lvl2", "key1"): "value3rd", ("check",): "value3rd.txt"}


def test_flatten_dict():
    test_file = get_file("material/parser_flatten_dict.yaml")
    cfg = confipy.reader.read_config(test_file)
    flattened = confipy.converter._flat_dict(cfg)

    assert flattened == test_flattened_dict


def test_include():
    test_file = get_file("material/parser_include.yaml")
    cfg = confipy.reader.read_config(test_file)
    flattened = confipy.converter._flat_dict(cfg)
    included = confipy.parser.include(flattened, test_file)

    assert included == test_incl


def test_include_recursive():
    test_file = get_file("material/parser_include_recursive.yaml")
    cfg = confipy.reader.read_config(test_file)
    flattened = confipy.converter._flat_dict(cfg)
    included = confipy.parser.include(flattened, test_file)

    assert included == test_incl_recursive


def test_include_fail():
    file = get_file("material/parser_include_raiseError.yaml")
    cfg = confipy.reader.read_config(file)
    flattened = confipy.converter._flat_dict(cfg)

    with pytest.raises(AssertionError):
        included = confipy.parser.include(flattened, file)


def test_substitute():
    test_file = get_file("material/parser_substitute.yaml")
    cfg = confipy.reader.read_config(test_file)
    flattened = confipy.converter._flat_dict(cfg)
    subs = confipy.parser.substitute(flattened)

    assert subs == test_subs


def test_unflatten():
    unflatten = confipy.converter._unflat_dict(test_incl_recursive)
    assert unflatten == test_incl_lvl2_unflattend


def test_unflatten_dot():
    unflatten = confipy.converter._unflat_dict(test_incl_recursive,
                                               notation="dot")

    assert isinstance(unflatten, confipy.notation.DotNotation) == True
    assert unflatten.Lvl1.Key1 == "Value1"


if __name__ == "__main__":
    test_flatten_dict()
    test_include()
    test_include_recursive()
    test_include_fail()
    test_substitute()
    test_unflatten()
    test_unflatten_dot()
