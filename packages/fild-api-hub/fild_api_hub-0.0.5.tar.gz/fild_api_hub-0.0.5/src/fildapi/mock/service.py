import waiting

from fild.sdk import Field
from waiting.exceptions import TimeoutExpired

from fildapi.caller import ApiCaller
from fildapi.config import Cfg
from fildapi.method import ApiMethod
from fildapi.mock.data import (
    Command, ExpectationBody, HttpRequest, HttpResponse, ObjectType, Params,
    PathParams, RetrieveBody, RetrieveHttpRequest, Times, UnaddressedRequest,
)
from fildapi.schema import HttpMethod


def get_mockserver_url():
    if 'MockServer' in Cfg:
        return f'http://{Cfg.MockServer.host}:{Cfg.MockServer.port}'

    return None


BASE_URL = get_mockserver_url()


class RunCommand(ApiMethod):
    method = HttpMethod.PUT
    url = 'mockserver/{command}'
    path_params = PathParams


class MockClient(ApiCaller):
    method = RunCommand

    def __init__(self, command, params=None, headers=None, body=None):
        super().__init__(
            headers=headers,
            path_params=PathParams().with_values({
                PathParams.Command.name: command,
            }),
            params=params,
            req_body=body
        )


class MockServer:
    @staticmethod
    def _get_client(command, params=None, headers=None, body=None):
        return MockClient(command, params, headers, body).request()

    def reset(self):
        self._get_client(command=Command.Reset, headers={})

    def reply(self, method, url, body, status=200, params=None, req_body=None,
              headers=None, cookies=None, times=1, reset=True):
        if reset:
            self.reset()

        self._get_client(
            command=Command.Expectation,
            headers=headers,
            body=ExpectationBody().with_values({
                ExpectationBody.HttpRequest.name: {
                    HttpRequest.Method.name: method,
                    HttpRequest.Path.name: url,
                    HttpRequest.Params.name: params,
                    HttpRequest.Body.name: req_body,
                },
                ExpectationBody.HttpResponse.name: {
                    HttpResponse.StatusCode.name: status,
                    HttpResponse.Headers.name: headers,
                    HttpResponse.Cookies.name: cookies,
                    HttpResponse.Body.name: body
                },
                ExpectationBody.Times.name: {
                    Times.RemainingTimes.name: times,
                    Times.Unlimited.name: False,
                }
            })
        )

    def catch(self, url, body=None, method=None, timeout=None,
              latest=False):
        req_body = body

        if isinstance(req_body, Field):
            req_body = req_body.value

        def catch_request():
            return self._get_client(
                command=Command.Retrieve,
                params=Params().with_values({
                    Params.Type.name: ObjectType.Requests,
                }),
                body=RetrieveBody().with_values({
                    RetrieveBody.HttpRequest.name:
                        RetrieveHttpRequest().with_values({
                            RetrieveHttpRequest.Method.name: method,
                            RetrieveHttpRequest.Path.name: url,
                            RetrieveHttpRequest.Body.name: req_body,
                        }),
                })
            ).response.json()

        if timeout is None:
            caught = catch_request()
        else:
            caught = waiting.wait(
                catch_request,
                timeout_seconds=timeout,
                sleep_seconds=0,
                waiting_for='request'
            )

        assert caught, 'No requests received'

        if latest:
            incoming = caught[0]
        else:
            assert len(caught) == 1, 'More than one request are caught'
            incoming = caught[0]

        headers = incoming.get('headers')
        body = incoming.get('body')
        params = incoming.get('queryStringParameters')

        if isinstance(body, dict) and 'json' in body:
            body = body['json']

        return body, headers, params

    def get_unaddressed_requests(self):
        response = self._get_client(
            command=Command.Retrieve,
            params=Params().with_values({
                Params.Type.name: ObjectType.ActiveExpectations,
            })
        ).response.json()

        return [UnaddressedRequest().with_values(resp) for resp in response]

    def wait_for_mocks_to_be_called(self, timeout_seconds=1):
        try:
            return waiting.wait(
                lambda: not self.get_unaddressed_requests(),
                sleep_seconds=0,
                timeout_seconds=timeout_seconds,
                waiting_for='mocks to be called',
            )
        except TimeoutExpired:
            return None

    def verify_all_mocks_called(self, timeout_seconds=1):  # pylint:disable=inconsistent-return-statements
        try:
            return waiting.wait(
                lambda: not self.get_unaddressed_requests(),
                sleep_seconds=0,
                timeout_seconds=timeout_seconds,
                waiting_for='mocks to be called',
            )
        except TimeoutExpired:
            pass

        requests = self.get_unaddressed_requests()
        parsed_reqs = ''

        for req in requests:
            body = req.HttpRequest.Body.value

            if body and 'json' in body:
                body = body['json']

            parsed_reqs += (
                f'\n{req.HttpRequest.Method.value} '
                f'{req.HttpRequest.Path.value} {body}'
                f'\nTimes: {req.Times.RemainingTimes.value}'
            )

        assert not requests, f'There are unused mocks: {parsed_reqs}'
