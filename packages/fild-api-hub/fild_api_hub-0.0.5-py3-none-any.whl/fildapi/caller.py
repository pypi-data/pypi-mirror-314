from fild.process import dictionary
from fild.sdk import Field

from fildapi.deepdiff import compare_data
from fildapi.method import ApiMethod


class ApiCaller:
    method: ApiMethod

    def __init__(self, req_body=None, path_params=None, headers=None,
                 params=None, cookies=None, updates=None):
        self.req_body = req_body
        self.response = None
        self.path_params = path_params
        self.headers = headers
        self.params = params
        self.cookies = cookies
        self.updates = updates

    def request(self):
        req_body = self.req_body
        params = self.params

        if req_body is None:
            pass
        elif isinstance(self.req_body, Field):
            req_body = self.req_body.value

        if self.updates:
            req_body = dictionary.merge_with_updates(req_body, self.updates)

        if params is None:
            pass
        elif isinstance(self.params, Field):
            params = self.params.value

        self.response = self.method.call(
            req_body=req_body,
            path_params=self.path_params,
            headers=self.headers,
            params=params,
            cookies=self.cookies
        )

        return self

    def verify_response(self, error_code=None, resp_body=None, normalize=False,
                        normalize_keys=None, parse_response=None,
                        ignore_order=None, rules=None):
        if error_code:
            assert self.response.status_code == error_code, (
                f'Unexpected code: {self.response.status_code}\n'
                f'Response text: {self.response.text}'
            )
        else:
            assert self.response.status_code == 200, (
                f'Unexpected response code: {self.response.status_code}'
                f'\nResponse text: {self.response.text}'
            )

        if resp_body is not None or isinstance(resp_body, Field):
            content_type = self.response.headers.get('Content-Type')

            if content_type == 'text/csv':
                result_data = self.response.text

                if parse_response and callable(parse_response):
                    result_data = parse_response(result_data)
            else:
                result_data = self.response.text and self.response.json()

            if isinstance(resp_body, Field):
                resp_body = resp_body.value

            if normalize or normalize_keys:
                resp_body = dictionary.normalize(resp_body, result_data, keys=normalize_keys)

            compare_data(
                expected_data=resp_body,
                actual_data=result_data,
                ignore_order=ignore_order,
                rules=rules,
                target_name='api response'
            )

        return self
