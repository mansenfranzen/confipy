"""This module contains tests"""

import pytest
import confipy.reader
import confipy.parser

test_flattened_dict = {("level1", "level2", "level3", "key1"): "value1",
                       ("level1", "level2", "level3", "key2"): "value2"}

test_incl = {("Key1",): "Value1",
             ("Key2", "level1", "level2", "level3", "key1"): "value1",
             ("Key2", "level1", "level2", "level3", "key2"): "value2"}

test_incl_lvl2 = {("Lvl1", "Key1",): "Value1",
                  ("Lvl1", "Key2", "level1", "level2", "level3",
                   "key1"): "value1",
                  ("Lvl1", "Key2", "level1", "level2", "level3",
                   "key2"): "value2"}

level3 = {"level3":{"key1":"value1", "key2": "value2"}}
test_incl_lvl2_unflattend = {"Lvl1":{"Key1":"Value1",
                                     "Key2":{"level1": {"level2":level3}}}}

test_subs = {("key1",): "value1", ("key2",): "value2",
             ("list1",): ["value1value2", "prevalue1suf"],
             ("lvl1", "lvl2", "key1"): "value3rd", ("check",): "value3rd.txt"}


def test_flatten_dict():
    cfg = confipy.reader.read_config("material/skeleton_dummy.yaml")
    skeleton = confipy.parser._flatten_dict(cfg)

    assert skeleton == test_flattened_dict


def test_include():
    file = "material/include_dummy.yaml"
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.parser._flatten_dict(cfg)
    included = confipy.parser.include(skeleton, file)

    assert included == test_incl


def test_include_lvl2():
    file = "material/include_dummy_lvl2.yaml"
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.parser._flatten_dict(cfg)
    included = confipy.parser.include(skeleton, file)

    assert included == test_incl_lvl2


def test_include_fail():
    file = "material/include_fail.yaml"
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.parser._flatten_dict(cfg)

    with pytest.raises(AssertionError):
        included = confipy.parser.include(skeleton, file)


def test_substitute():
    file = "material/substitute_dummy.yaml"
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.parser._flatten_dict(cfg)
    subs = confipy.parser.substitute(skeleton)

    assert subs == test_subs


def test_unflatten():
    unflatten = confipy.parser._unflatten_dict(test_incl_lvl2)
    assert unflatten == test_incl_lvl2_unflattend

if __name__ == "__main__":
    test_flatten_dict()
    test_include()
    test_include_lvl2()
    test_include_fail()
    test_substitute()
    test_unflatten()
