import os
from unittest import mock

import pytest
from dtPyAppFramework.settings.settings_reader import SettingsReader


# Test that __init__ sets the attributes correctly
def test_init():
    settings_reader = SettingsReader('/path/to/settings', 5)
    assert settings_reader.priority == 5
    assert settings_reader.settings_file == '/path/to/settings/config.yaml'


# Test that load_yaml_file loads a YAML file correctly
@mock.patch('yaml.safe_load', return_value={'key': 'value'})
def test_load_yaml_file(mock_safe_load):
    settings_reader = SettingsReader('/path/to/settings', 5)
    settings_reader.load_yaml_file()
    assert settings_reader.get('key') == 'value'


# Test that __getitem__ can retrieve data correctly using dot notation
def test_getitem():
    settings_reader = SettingsReader('/path/to/settings', 5)

    data = {
        'key': 'value',
        'nested': {
            'key': 'nested value'
        }
    }

    settings_reader.update(data)

    assert settings_reader.__getitem__('nested.key') == 'nested value'
    assert settings_reader.__getitem__('key') == 'value'


# Test that methods that are not implemented raise a NotImplementedError
def test_not_implemented_methods():
    settings_reader = SettingsReader('/path/to/settings', 5)

    with pytest.raises(NotImplementedError):
        settings_reader.clear()

    with pytest.raises(NotImplementedError):
        settings_reader.popitem()

    with pytest.raises(NotImplementedError):
        settings_reader.__setitem__('key', 'value')

    with pytest.raises(NotImplementedError):
        settings_reader.pop('key')
