import pytest

from fildapi.config import Cfg


@pytest.fixture(scope='module', autouse=True)
def reset_config():
    Cfg.initial_dict = None
    yield
    Cfg.initialize()


def test_config_initialized():
    assert Cfg.App is not None
