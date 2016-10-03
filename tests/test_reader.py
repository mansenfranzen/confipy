"""This module tests the confipy reader."""

import pytest
import confipy.reader

test_dict = {
    "DummySection1":
        {
            "key1": "value1",
            "key2": "value2",
            "list_int": [1, 2, 3, 4],
            "list_str": ["A", "B", "C"]
        },

    "DummySection2":
        {
            "key1": "value1",
            "key2": "value2"
        }
}


def test_cfg_reader():
    cfg = confipy.reader.read_config("material/dummy.cfg")

    # as lists are not supported here, they need to be converted
    list_int = list(map(int, cfg["DummySection1"]["list_int"].split(",")))
    list_str = cfg["DummySection1"]["list_str"].split(",")

    cfg["DummySection1"]["list_int"] = list_int
    cfg["DummySection1"]["list_str"] = list_str

    assert cfg == test_dict


def test_ini_reader():
    cfg = confipy.reader.read_config("material/dummy.ini")

    # as lists are not supported here, they need to be converted
    list_int = list(map(int, cfg["DummySection1"]["list_int"].split(",")))
    list_str = cfg["DummySection1"]["list_str"].split(",")

    cfg["DummySection1"]["list_int"] = list_int
    cfg["DummySection1"]["list_str"] = list_str

    assert cfg == test_dict


def test_yaml_reader():
    cfg = confipy.reader.read_config("material/dummy.yaml")
    assert cfg == test_dict


def test_json_reader():
    cfg = confipy.reader.read_config("material/dummy.json")
    assert cfg == test_dict


def test_auto_read():
    with open("material/dummy.yaml", "r") as file:
        cfg = confipy.reader.read_config(file)

    assert cfg == test_dict


    with open("material/dummy.json", "r") as file:
        cfg = confipy.reader.read_config(file)

    assert cfg == test_dict


def test_auto_read_fail():
    with pytest.raises(IOError):
        with open("material/dummy_bad.cfg", "r") as file:
            cfg = confipy.reader.read_config(file)



if __name__ == "__main__":
    test_cfg_reader()
    test_ini_reader()
    test_yaml_reader()
    test_json_reader()
    test_auto_read()
    test_auto_read_fail()
