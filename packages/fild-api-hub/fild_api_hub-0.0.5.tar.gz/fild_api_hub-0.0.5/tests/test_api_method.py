from fild.sdk import Dictionary

from fildapi import HttpMethod
from fildapi.config import Cfg
from fildapi.mock.data import (
    Command, ExpectationBody, JsonFilter,  HttpRequest, HttpResponse,
    MatchType, RetrieveBody, RetrieveHttpRequest, PathParams, StringFilter,
    Times,
)
from fildapi.mock.service import RunCommand
from tests.data.dummy_api import CheckCall, CheckCallReq


def test_call_result(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    result = CheckCall.call()

    assert result.status_code == 200


def test_call_mock_called(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    CheckCall.call()

    assert requests_mock.called


def test_call_mock_call_count(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    CheckCall.call()

    assert requests_mock.call_count == 1


def test_call_mocked_method(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    CheckCall.call()

    assert requests_mock.last_request.method == CheckCall.method


def test_call_mocked_url(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    CheckCall.call()

    assert requests_mock.last_request.url == CheckCall.get_request_url()


def test_call_request_body(requests_mock):
    req_body = CheckCallReq().value
    requests_mock.post(CheckCall.get_request_url(), json={})
    CheckCall.call(req_body=req_body)

    assert requests_mock.last_request.json() == req_body


def test_reply(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply()

    assert requests_mock.called


def test_reset(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Reset,
        })
    ))
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply(reset=True)

    assert requests_mock.call_count == 2


def test_reply_with_filter(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply(req_body={'test': 'filter'})

    assert requests_mock.last_request.json() == ExpectationBody().with_values({
        ExpectationBody.HttpRequest.name: {
            HttpRequest.Method.name: CheckCall.method,
            HttpRequest.Path.name: (
                f'/mockserver/{CheckCall.get_service_name()}'
                f'{CheckCall.get_relative_url()}'
            ),
            HttpRequest.Body.name: JsonFilter().with_values({
                JsonFilter.Json.name: {'test': 'filter'},
                JsonFilter.MatchType.name: MatchType.Partial,
            })
        },
        ExpectationBody.HttpResponse.name: {
            HttpResponse.Body.name: '{}',
            HttpResponse.Headers.name: {'Content-Type': 'application/json'},
            HttpResponse.StatusCode.name: 200,
        },
        ExpectationBody.Times.name: {
            Times.RemainingTimes.name: 1,
            Times.Unlimited.name: False,
        }
    }).value


def test_reply_with_substr_filter_no_prefix(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply(substr_filter='substring', no_prefix=True)

    assert requests_mock.last_request.json() == ExpectationBody().with_values({
        ExpectationBody.HttpRequest.name: {
            HttpRequest.Method.name: CheckCall.method,
            HttpRequest.Path.name: CheckCall.get_relative_url(),
            HttpRequest.Body.name: StringFilter().with_values({
                StringFilter.String.name: 'substring',
            })
        },
        ExpectationBody.HttpResponse.name: {
            HttpResponse.Body.name: '{}',
            HttpResponse.Headers.name: {'Content-Type': 'application/json'},
            HttpResponse.StatusCode.name: 200,
        },
        ExpectationBody.Times.name: {
            Times.RemainingTimes.name: 1,
            Times.Unlimited.name: False,
        }
    }).value


def test_reply_with_default_headers(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply(default_headers=True)

    assert requests_mock.last_request.json() == ExpectationBody().with_values({
        ExpectationBody.HttpRequest.name: {
            HttpRequest.Method.name: CheckCall.method,
            HttpRequest.Path.name: (
                f'/mockserver/{CheckCall.get_service_name()}'
                f'{CheckCall.get_relative_url()}'
            ),
        },
        ExpectationBody.HttpResponse.name: {
            HttpResponse.Body.name: '{}',
            HttpResponse.Headers.name: {
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Origin': Cfg.App.url,
                'Content-Type': 'application/json'
            },
            HttpResponse.StatusCode.name: 200,
        },
        ExpectationBody.Times.name: {
            Times.RemainingTimes.name: 1,
            Times.Unlimited.name: False,
        }
    }).value


def test_reply_with_corse_options(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply_corse_options(allow_headers=['first', 'second'])

    assert requests_mock.last_request.json() == ExpectationBody().with_values({
        ExpectationBody.HttpRequest.name: {
            HttpRequest.Method.name: HttpMethod.OPTIONS,
            HttpRequest.Path.name: (
                f'/mockserver/{CheckCall.get_service_name()}'
                f'{CheckCall.get_relative_url()}'
            ),
        },
        ExpectationBody.HttpResponse.name: {
            HttpResponse.Headers.name: {
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'first,second',
                'Access-Control-Allow-Origin': Cfg.App.url,
                'Content-Type': 'Access-Control-Allow-Headers'
            },
            HttpResponse.StatusCode.name: 200,
        },
        ExpectationBody.Times.name: {
            Times.RemainingTimes.name: 1,
            Times.Unlimited.name: False,
        }
    }).value


def test_reply_with_corse_options_no_prefix(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Expectation
        })
    ))
    CheckCall.reply_corse_options(
        allow_headers=['first', 'second'], no_prefix=True
    )

    assert requests_mock.last_request.json() == ExpectationBody().with_values({
        ExpectationBody.HttpRequest.name: {
            HttpRequest.Method.name: HttpMethod.OPTIONS,
            HttpRequest.Path.name: CheckCall.get_relative_url()
        },
        ExpectationBody.HttpResponse.name: {
            HttpResponse.Headers.name: {
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'first,second',
                'Access-Control-Allow-Origin': Cfg.App.url,
                'Content-Type': 'Access-Control-Allow-Headers'
            },
            HttpResponse.StatusCode.name: 200,
        },
        ExpectationBody.Times.name: {
            Times.RemainingTimes.name: 1,
            Times.Unlimited.name: False,
        }
    }).value


def test_verify_called(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[{'body': {}, 'queryStringParameters': {}}])
    CheckCall.verify_called(expected=Dictionary(), params=Dictionary())

    assert requests_mock.called


def test_verify_called_filtered(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[{'body': {'json': {}}, 'queryStringParameters': {}}])
    CheckCall.verify_called(
        expected=Dictionary(),
        params=Dictionary(),
        body='test_string',
        timeout=1,
        latest=1
    )

    assert requests_mock.last_request.json() == RetrieveBody().with_values({
        RetrieveBody.HttpRequest.name: RetrieveHttpRequest().with_values({
            RetrieveHttpRequest.Body.name: StringFilter().with_values({
                StringFilter.String.name: 'test_string'
            }),
            RetrieveHttpRequest.Method.name: CheckCall.method,
            RetrieveHttpRequest.Path.name:  (
                f'/mockserver/{CheckCall.get_service_name()}'
                f'{CheckCall.get_relative_url()}'
            ),
        }),
    }).value


def test_verify_called_normalize_and_headers(requests_mock):
    requests_mock.put(RunCommand.get_request_url(
        path_params=PathParams().with_values({
            PathParams.Command: Command.Retrieve
        }),
    ), json=[{
        'body': {},
        'queryStringParameters': {'qTy': 12},
        'headers': {'TestHeader': 'some_test_value'}
    }])
    CheckCall.verify_called(
        expected=Dictionary(),
        params={'qTy': 12},
        headers={'TestHeader': 'some_test_value'},
        normalize=True
    )

    assert requests_mock.called
