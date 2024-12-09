import os

import pytest

from fildapi.config import Cfg


@pytest.fixture(scope='module', autouse=True)
def init_config():
    Cfg.initialize(
        config_file=f'{os.path.dirname(__file__)}/etc/config.yaml',
        local_config=f'{os.path.dirname(__file__)}/etc/local.yaml',
    )
    yield
    Cfg.initialize()


def test_config_value():
    assert Cfg.App.url == 'test_url'


def test_config_section_value():
    assert Cfg.Section.sub_sec.string_value == 'temp'


def test_config_section_override():
    assert Cfg.Section.sub_sec.int_value == 2


def test_get_item():
    assert Cfg['App']['url'] == 'test_url'


def test_str():
    assert str(Cfg.App) == str({'url': 'test_url'})


def test_contains():
    assert 'url' in Cfg.App


def test_not_contain():
    assert 'test_url' not in Cfg.App


def test_len():
    assert len(Cfg.Section.sub_sec) == 2


def test_keys():
    assert list(Cfg.App.keys()) == ['url']


def test_values():
    assert list(Cfg.Section.sub_sec.values()) == ['temp', 2]


def test_items():
    assert list(Cfg.App.items()) == [('url', 'test_url')]


def test_update_config():
    Cfg.App.extra_url = 'extra'
    assert Cfg.App.extra_url == 'extra'


def test_update_new_section():
    Cfg.Section.extra_sec = {'new_item': 0}
    assert Cfg.Section.extra_sec.new_item == 0


def test_update_existing_section():
    Cfg.Section.sub_sec.new_string = 'second_string'
    assert Cfg.Section.sub_sec.new_string == 'second_string'


def test_update_add_key():
    Cfg.App['one_more_url'] = 'new_url'
    assert Cfg.App.one_more_url == 'new_url'


def test_get_with_default():
    assert Cfg.App.get('not_exsiting', 'default') == 'default'


def test_get_existing_key():
    assert Cfg.App.get('url') == 'test_url'
