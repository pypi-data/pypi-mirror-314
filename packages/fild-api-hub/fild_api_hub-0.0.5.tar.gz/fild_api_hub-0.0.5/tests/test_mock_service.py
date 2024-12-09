import os

import pytest

from fildapi import MockServer
from fildapi.config import Cfg
from fildapi.mock import service
from fildapi.mock.data import (
    Command, HttpRequest, PathParams, UnaddressedRequest
)
from fildapi.mock.service import RunCommand


@pytest.fixture
def reset_config():
    Cfg.initialize(
        config_file=f'{os.path.dirname(__file__)}/etc/config_no_mock.yaml',
    )
    yield
    Cfg.initialize()


def test_no_url(reset_config):  # pylint: disable=unused-argument,redefined-outer-name
    assert service.get_mockserver_url() is None


def test_verify_called_filtered(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[])
    MockServer().get_unaddressed_requests()

    assert requests_mock.last_request.json() == {}


def test_wait_for_mocks_to_be_called(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[])
    MockServer().wait_for_mocks_to_be_called()

    assert requests_mock.last_request.json() == {}


def test_wait_for_mocks_to_be_called_timeout(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[UnaddressedRequest().value])
    result = MockServer().wait_for_mocks_to_be_called(timeout_seconds=0)

    assert result is None


def test_verify_all_mocks_are_called(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[])
    MockServer().verify_all_mocks_called()

    assert requests_mock.last_request.json() == {}


def test_verify_not_all_mocks_are_called(requests_mock):
    unused_mock = UnaddressedRequest().with_values({
        UnaddressedRequest.HttpRequest.name: {
            HttpRequest.Body.name: {'json': 'test'}
        }
    })
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[unused_mock.value])
    error_message = (
        f'There are unused mocks: '
        f'\n{unused_mock.HttpRequest.Method.value} '
        f'{unused_mock.HttpRequest.Path.value} test'
        f'\nTimes: None'
    )

    with pytest.raises(AssertionError, match=error_message):
        MockServer().verify_all_mocks_called(timeout_seconds=0)
