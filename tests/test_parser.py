"""This module contains tests"""

import pytest
import confipy.converter
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
    cfg = confipy.reader.read_config(get_file("material/skeleton_dummy.yaml"))
    skeleton = confipy.converter._flat_dict(cfg)

    assert skeleton == test_flattened_dict


def test_include():
    file = get_file("material/include_dummy.yaml")
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.converter._flat_dict(cfg)
    included = confipy.parser.include(skeleton, file)

    assert included == test_incl


def test_include_lvl2():
    file = get_file("material/include_dummy_lvl2.yaml")
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.converter._flat_dict(cfg)
    included = confipy.parser.include(skeleton, file)

    assert included == test_incl_lvl2


def test_include_fail():
    file = get_file("material/include_fail.yaml")
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.converter._flat_dict(cfg)

    with pytest.raises(AssertionError):
        included = confipy.parser.include(skeleton, file)


def test_substitute():
    file = get_file("material/substitute_dummy.yaml")
    cfg = confipy.reader.read_config(file)
    skeleton = confipy.converter._flat_dict(cfg)
    subs = confipy.parser.substitute(skeleton)

    assert subs == test_subs


def test_unflatten():
    unflatten = confipy.converter._unflat_dict(test_incl_lvl2)
    assert unflatten == test_incl_lvl2_unflattend


def test_unflatten_dot():
    def_type = confipy.converter.DotNotation
    unflatten = confipy.converter._unflat_dict(test_incl_lvl2,
                                               default_type=def_type)

    assert isinstance(unflatten, def_type) == True
    assert unflatten.Lvl1.Key1 == "Value1"


if __name__ == "__main__":
    test_flatten_dict()
    test_include()
    test_include_lvl2()
    test_include_fail()
    test_substitute()
    test_unflatten()
    test_unflatten_dot()

