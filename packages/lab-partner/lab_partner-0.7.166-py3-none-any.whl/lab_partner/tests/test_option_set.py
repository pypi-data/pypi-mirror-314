import pytest
from lab_partner.option_set import KeyValueOption, Option, OptionSet, ValueOption


def test_equal_options_replace_each_other():
    option_set = OptionSet()
    option1 = Option('--o')
    option2 = Option('--o')
    id2 = id(option2)

    option_set.put(option1)
    option_set.put(option2)

    assert len(option_set) == 1, 'Only a single option should be in the set'
    assert id2 == id(option_set.to_list().pop()), 'ID of option should equal to option 2'

def test_equal_value_options_replace_each_other():
    option_set = OptionSet()
    option1 = ValueOption('--o', 'dog')
    option2 = ValueOption('--o', 'dog')
    id2 = id(option2)

    option_set.put(option1)
    option_set.put(option2)
    assert len(option_set) == 1, 'Only a single value option should be in the set'
    assert id2 == id(option_set.to_list().pop()), 'ID of option should equal to option 2'

def test_no_duplicate_value_options_different_values():
    option_set = OptionSet()
    option1 = ValueOption('--o', 'dog')
    option2 = ValueOption('--o', 'cat')

    option_set.put(option1)
    option_set.put(option2)
    assert len(option_set) == 1, 'Only a single value option should be in the set'
    assert option2 == option_set.to_list().pop(), 'option in set should equal to option 2'

def test_different_value_options_coexist():
    option_set = OptionSet()
    option1 = ValueOption('--o', 'dog')
    option2 = ValueOption('--p', 'dog')

    option_set.put(option1)
    option_set.put(option2)
    assert option1 in option_set
    assert option2 in option_set

def test_equal_key_value_options_replace_each_other():
    option_set = OptionSet()
    option1 = KeyValueOption('--o', 'dog', 'rover')
    option2 = KeyValueOption('--o', 'dog', 'rover')
    id2 = id(option2)

    option_set.put(option1)
    option_set.put(option2)
    assert len(option_set) == 1, 'Only a single key value option should be in the set'
    assert id2 == id(option_set.to_list().pop()), 'ID of option should equal to option 2'

def test_no_duplicate_key_value_options_different_values():
    option_set = OptionSet()
    option1 = KeyValueOption('--o', 'dog', 'rover')
    option2 = KeyValueOption('--o', 'dog', 'rex')

    option_set.put(option1)
    option_set.put(option2)
    assert len(option_set) == 1, 'Only a single key value option should be in the set'
    assert option2 == option_set.to_list().pop(), 'option in set should equal to option 2'

def test_different_key_value_options_coexist():
    option_set = OptionSet()
    option1 = KeyValueOption('--o', 'dog', 'rover')
    option2 = KeyValueOption('--p', 'dog', 'rover')

    option_set.put(option1)
    option_set.put(option2)
    assert option1 in option_set
    assert option2 in option_set

def test_same_key_value_option_with_different_key_coexist():
    option_set = OptionSet()
    option1 = KeyValueOption('--o', 'dog', 'rover')
    option2 = KeyValueOption('--o', 'animal', 'rover')

    option_set.put(option1)
    option_set.put(option2)
    assert option1 in option_set
    assert option2 in option_set

def test_all_option_types_coexist():
    option_set = OptionSet()
    option1 = Option('--o')
    option2 = ValueOption('--o', 'animal')
    option3 = KeyValueOption('--o', 'animal', 'rover')

    option_set.put(option1)
    option_set.put(option2)
    option_set.put(option3)
    assert option1 in option_set
    assert option2 in option_set
    assert option3 in option_set

def test_exclusive_options():
    option_set = OptionSet()
    option1 = Option('--o')
    option2 = ValueOption('--p', 'animal')
    option3 = KeyValueOption('--q', 'animal', 'rover')

    option_set.add_mutually_exclusive_options(set([option1, option2, option3]))

    option_set.put(option2)
    with pytest.raises(ValueError):
        option_set.put(option1)



