import json

import requests

from fild.process import dictionary
from fild.sdk import Field

from fildapi.deepdiff import compare_data
from fildapi.mock.data import JsonFilter, MatchType, StringFilter
from fildapi.schema import Schema, HttpMethod


class ApiMethod(Schema):
    @classmethod
    def call(cls, req_body=None, session=None, path_params=None, headers=None,
             params=None, cookies=None):
        session = session or requests.Session()

        if params is None:
            params = cls.params().value

        if req_body is None:
            req_body = cls.req_body().value

        if req_body is not None:
            req_body = json.dumps(req_body)

        url = cls.get_request_url(path_params=path_params)
        headers = headers or {}
        headers = dictionary.merge_with_updates(headers, {
            'Content-Type': 'application/json',
        })

        return session.request(
            str(cls.method),
            url,
            headers=headers,
            params=params,
            data=req_body,
            cookies=cookies
        )

    @classmethod
    def reply(cls, path_params=None, params=None, req_body=None, body=None,
              status=200, reset=False, cookies=None, headers=None, times=1,
              no_prefix=False, substr_filter=None, strict=False,
              default_headers=False):
        from fildapi.mock.service import MockServer   # pylint: disable=cyclic-import
        reply_body = body

        if default_headers and headers is None:
            headers = cls.fe_headers()

        headers = headers or {'Content-Type': 'application/json',}

        if reply_body is None:
            reply_body = cls.resp_body and cls.resp_body() # pylint: disable=not-callable

        if reply_body not in [None, {}, '']:
            reply_body = reply_body.value
            reply_body = json.dumps(reply_body)

        if req_body:
            req_body = JsonFilter().with_values({
                JsonFilter.Json.name: req_body,
                JsonFilter.MatchType.name:
                    MatchType.Strict if strict else MatchType.Partial
            })
        elif substr_filter:
            req_body = StringFilter().with_values({
                StringFilter.String.name: substr_filter
            })

        if no_prefix:
            prefix = ''
        else:
            prefix = f'/mockserver/{cls.get_service_name()}'

        return MockServer().reply(
            method=cls.method,
            url=f'{prefix}{cls.get_relative_url(path_params)}',
            params=params,
            req_body=req_body,
            body=reply_body,
            status=status,
            reset=reset,
            headers=headers or {},
            cookies=cookies,
            times=times
        )

    @classmethod
    def reply_corse_options(cls, allow_headers, reset=False, no_prefix=False,
                            path_params=None, params=None, req_body=None):
        from fildapi.mock.service import MockServer   # pylint: disable=cyclic-import
        headers = cls.fe_headers(
            content_type='Access-Control-Allow-Headers',
        )
        headers['Access-Control-Allow-Headers'] = ','.join(allow_headers)

        if no_prefix:
            prefix = ''
        else:
            prefix = f'/mockserver/{cls.get_service_name()}'

        return MockServer().reply(
            method=HttpMethod.OPTIONS,
            url=f'{prefix}{cls.get_relative_url(path_params)}',
            params=params,
            req_body=req_body,
            body=None,
            reset=reset,
            headers=headers
        )

    @classmethod
    def verify_called(cls, expected=None, normalize=False, normalize_keys=None,
                      path_params=None, timeout=None, body=None, headers=None,
                      latest=False, params=None, rules=None, header_rules=None):
        from fildapi.mock.service import MockServer  # pylint: disable=cyclic-import

        expected_value = expected

        if isinstance(expected_value, Field):
            expected_value = expected_value.value
        if isinstance(params, Field):
            params = params.value

        if body:
            if isinstance(body, str):
                body = StringFilter().with_values({
                    StringFilter.String.name: body
                })

        actual_value, actual_headers, actual_params = MockServer().catch(
            method=cls.method,
            url=(f'/mockserver/{cls.get_service_name()}'
                 f'{cls.get_relative_url(path_params=path_params)}'),
            body=body,
            timeout=timeout,
            latest=latest
        )

        if normalize or normalize_keys:
            actual_value = dictionary.normalize(
                actual_value, expected_value, keys=normalize_keys
            )
        compare_data(
            actual_data=actual_value,
            expected_data=expected_value,
            rules=rules or None,
            target_name='api request'
        )

        if headers:
            filtered_headers = {}

            for key in headers:
                filtered_headers[key] = actual_headers.get(key)

            compare_data(
                actual_data=filtered_headers,
                expected_data=headers,
                rules=header_rules or None,
                target_name='api request headers'
            )

        #FIXME parse into object + verify all together

        if params:
            compare_data(
                actual_data=actual_params,
                expected_data=params,
                target_name='api request params'
            )
