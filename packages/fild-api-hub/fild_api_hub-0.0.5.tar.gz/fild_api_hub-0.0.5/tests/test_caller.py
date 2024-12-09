import json

from fild.sdk import Dictionary
from requests import Response

from fildapi import ApiCaller
from tests.data.dummy_api import CheckCall


class CheckCallCaller(ApiCaller):
    method = CheckCall


def test_verify_response():
    caller = CheckCallCaller()
    caller.response = Response()
    caller.response.status_code = 200
    caller.verify_response()


def test_verify_error_response():
    caller = CheckCallCaller()
    caller.response = Response()
    caller.response.status_code = 300
    caller.verify_response(error_code=300)


def test_verify_response_body():
    caller = CheckCallCaller()
    caller.response = Response()
    caller.response.status_code = 200
    caller.response._content = str.encode(json.dumps({}))  # pylint: disable=protected-access
    caller.verify_response(resp_body=Dictionary())


def test_verify_response_text():
    caller = CheckCallCaller()
    caller.response = Response()
    caller.response.status_code = 200
    caller.response.headers = {'Content-Type': 'text/csv'}
    caller.response._content = str.encode('test')  # pylint: disable=protected-access
    caller.verify_response(
        resp_body='test_parsed',
        parse_response=lambda x: f'{x}_parsed',
        normalize=True
    )


def test_request_updates(requests_mock):
    requests_mock.post(CheckCall.get_request_url(), json={})
    updates = {'test_key': 'test_value'}
    CheckCallCaller(updates=updates).request()

    assert requests_mock.last_request.json() == updates
