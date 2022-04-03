from unittest.mock import patch

import pytest
from bashtable import BashTable
from pytest_unordered import unordered


@pytest.fixture
def bash_table():
    sample_data = BashTable(capacity=100)
    sample_data["hola"] = "hello"
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data


def test_should_always_pass():
    assert 2 + 2 == 4


def test_should_create_bashtable():
    assert BashTable(capacity=100) is not None


def test_should_report_length_of_empty_hash_table():
    assert len(BashTable(capacity=100)) == 0


def test_should_create_empty_pair_slots():
    assert BashTable(capacity=3)._slots == [None, None, None]


def test_should_insert_key_value_pairs():
    bash_table = BashTable(capacity=100)

    bash_table["hola"] = "hello"
    bash_table[98.6] = 37
    bash_table[False] = True

    assert ("hola", "hello") in bash_table.pairs
    assert (98.6, 37) in bash_table.pairs
    assert (False, True) in bash_table.pairs

    assert len(bash_table) == 3


def test_should_grow_when_adding_elements():
    bash_table = BashTable(capacity=100)
    assert len(bash_table) == 0

    bash_table["hola"] = "hello"
    bash_table[98.6] = 37
    bash_table[False] = True
    assert len(bash_table) == 3


def test_should_insert_none_value():
    bash_table = BashTable(capacity=100)
    bash_table["key"] = None
    assert ("key", None) in bash_table.pairs


def test_should_find_value_by_key(bash_table):
    assert bash_table["hola"] == "hello"
    assert bash_table[98.6] == 37
    assert bash_table[False] is True


def test_should_raise_error_on_missing_key():
    bash_table = BashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        bash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_find_key(bash_table):
    assert "hola" in bash_table


def test_should_not_find_key(bash_table):
    assert "missing_key" not in bash_table


def test_should_get_value(bash_table):
    assert bash_table.get("hola") == "hello"


def test_should_not_contain_none_value_when_create():
    assert None not in BashTable(capacity=100).values


def test_should_get_none_when_missing_key(bash_table):
    assert bash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(bash_table):
    assert bash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(bash_table):
    assert bash_table.get("hola", "default") == "hello"


def test_should_delete_key_value_pair(bash_table):
    assert ("hola", "hello") in bash_table.pairs
    assert len(bash_table) == 3

    del bash_table["hola"]

    assert ("hola", "hello") not in bash_table.pairs
    assert len(bash_table) == 2


def test_should_raise_key_error_when_deleting(bash_table):
    with pytest.raises(KeyError) as exception_info:
        del bash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_update_value(bash_table):
    assert bash_table["hola"] == "hello"

    bash_table["hola"] = "hallo"

    assert bash_table["hola"] == "hallo"
    assert bash_table[98.6] == 37
    assert bash_table[False] is True
    assert len(bash_table) == 3


def test_should_return_copy_of_pairs(bash_table):
    assert bash_table.pairs is not bash_table.pairs


def test_should_not_include_blank_pairs(bash_table):
    assert None not in bash_table.pairs


def test_should_return_duplicate_values():
    bash_table = BashTable(capacity=100)
    bash_table["Alice"] = 24
    bash_table["Bob"] = 42
    bash_table["Joe"] = 42
    assert [24, 42, 42] == sorted(bash_table.values)


def test_should_get_values(bash_table):
    assert unordered(bash_table.values) == ["hello", 37, True]


def test_should_get_values_of_empty_hash_table():
    assert BashTable(capacity=100).values == []


def test_should_return_copy_of_values(bash_table):
    assert bash_table.values is not bash_table.values


def test_should_get_keys(bash_table):
    assert bash_table.keys == {"hola", 98.6, False}


def test_should_get_keys_of_empty_hash_table():
    assert BashTable(capacity=100).keys == set()


def test_should_return_copy_of_keys(bash_table):
    assert bash_table.keys is not bash_table.keys


def test_should_return_pairs(bash_table):
    assert bash_table.pairs == {("hola", "hello"), (98.6, 37), (False, True)}


def test_should_get_pairs_of_empty_hash_table():
    assert BashTable(capacity=100).pairs == set()


def test_should_convert_to_dict(bash_table):
    dictionary = dict(bash_table.pairs)
    assert set(dictionary.keys()) == bash_table.keys
    assert set(dictionary.items()) == bash_table.pairs
    assert list(dictionary.values()) == unordered(bash_table.values)


def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        BashTable(capacity=0)


def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        BashTable(capacity=-100)


def test_should_report_length(bash_table):
    assert len(bash_table) == 3


def test_should_report_capacity_of_empty_hash_table():
    assert BashTable(capacity=100).capacity == 100


def test_should_report_capacity(bash_table):
    assert bash_table.capacity == 100


def test_should_iterate_over_keys(bash_table):
    for key in bash_table.keys:
        assert key in ("hola", 98.6, False)


def test_should_iterate_over_values(bash_table):
    for value in bash_table.values:
        assert value in ("hello", 37, True)


def test_should_iterate_over_pairs(bash_table):
    for key, value in bash_table.pairs:
        assert key in bash_table.keys
        assert value in bash_table.values


def test_should_iterate_over_instance(bash_table):
    for key in bash_table:
        assert key in ("hola", 98.6, False)


def test_should_use_dict_literal_for_str(bash_table):
    assert str(bash_table) in {
        "{'hola': 'hello', 98.6: 37, False: True}",
        "{'hola': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'hola': 'hello', False: True}",
        "{98.6: 37, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'hola': 'hello'}",
    }


def test_should_create_hashtable_from_dict():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    bash_table = BashTable.from_dict(dictionary)

    assert bash_table.capacity == len(dictionary) * 10
    assert bash_table.keys == set(dictionary.keys())
    assert bash_table.pairs == set(dictionary.items())
    assert unordered(bash_table.values) == list(dictionary.values())


def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    bash_table = BashTable.from_dict(dictionary, capacity=100)

    assert bash_table.capacity == 100
    assert bash_table.keys == set(dictionary.keys())
    assert bash_table.pairs == set(dictionary.items())
    assert unordered(bash_table.values) == list(dictionary.values())


def test_should_have_canonical_string_representation(bash_table):
    assert repr(bash_table) in {
        "BashTable.from_dict({'hola': 'hello', 98.6: 37, False: True})",
        "BashTable.from_dict({'hola': 'hello', False: True, 98.6: 37})",
        "BashTable.from_dict({98.6: 37, 'hola': 'hello', False: True})",
        "BashTable.from_dict({98.6: 37, False: True, 'hola': 'hello'})",
        "BashTable.from_dict({False: True, 'hola': 'hello', 98.6: 37})",
        "BashTable.from_dict({False: True, 98.6: 37, 'hola': 'hello'})",
    }


def test_should_compare_equal_to_itself(bash_table):
    assert bash_table == bash_table


def test_should_compare_equal_to_copy(bash_table):
    assert bash_table is not bash_table.copy()
    assert bash_table == bash_table.copy()


def test_should_compare_equal_different_key_value_order():
    h1 = BashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = BashTable.from_dict({"b": 2, "a": 1, "c": 3})
    assert h1 == h2


def test_should_compare_unequal(bash_table):
    other = BashTable.from_dict({"different": "value"})
    assert bash_table != other


def test_should_compare_unequal_another_data_type(bash_table):
    assert bash_table != 42


def test_should_copy_keys_values_pairs_capacity(bash_table):
    copy = bash_table.copy()
    assert copy is not bash_table
    assert set(bash_table.keys) == set(copy.keys)
    assert unordered(bash_table.values) == copy.values
    assert set(bash_table.pairs) == set(copy.pairs)
    assert bash_table.capacity == copy.capacity


def test_should_compare_equal_different_capacity():
    data = {"a": 1, "b": 2, "c": 3}
    h1 = BashTable.from_dict(data, capacity=50)
    h2 = BashTable.from_dict(data, capacity=100)
    assert h1 == h2


def test_should_detect_hash_collision():
    assert hash("foobar") not in [1, 2, 3]
    with patch("builtins.hash", side_effect=[1, 2, 3]):
        assert hash("foobar") == 1
        assert hash("foobar") == 2
        assert hash("foobar") == 3
