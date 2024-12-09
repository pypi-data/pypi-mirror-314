import inspect

from fild.process.common import exclude_none_from_kwargs
from fild.sdk import Dictionary, Enum

from fildapi.config import Cfg


def get_default_app_url():
    if 'App' in Cfg:
        return Cfg.App.get('url')

    return None


class HttpMethod(Enum):
    POST = 'POST'
    GET = 'GET'
    HEAD = 'HEAD'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    PUT = 'PUT'
    TRACE = 'TRACE'
    OPTIONS = 'OPTIONS'


class Schema:
    """
      Additional configuration on module level:
      SERVICE: service name for mocking
      BASE_URL: application base url if not Cfg.App.url (default)
      API_URL: api base url
    """

    method: HttpMethod
    url: str
    path_params = Dictionary
    params = Dictionary
    req_body = Dictionary
    resp_body = Dictionary

    @classmethod
    def get_relative_url(cls, path_params=None):
        path_params = path_params or cls.path_params()
        formatted_url = cls.url.format(**path_params.value)
        return f'/{cls.get_api_base_url()}{formatted_url}'

    @classmethod
    def get_service_name(cls):
        parent_module = inspect.getmodule(cls)
        return getattr(parent_module, 'SERVICE', None)

    @classmethod
    def get_base_url(cls):
        parent_module = inspect.getmodule(cls)
        return getattr(parent_module, 'BASE_URL', get_default_app_url())

    @classmethod
    def get_api_base_url(cls):
        parent_module = inspect.getmodule(cls)
        return getattr(parent_module, 'API_URL', '')

    @classmethod
    def get_request_url(cls, path_params=None):
        return (
            f'{cls.get_base_url()}'
            f'{cls.get_relative_url(path_params=path_params)}'
        )

    @classmethod
    def fe_headers(cls, app_url=None, content_type='application/json',
                   set_cookie=None):
        return exclude_none_from_kwargs({
            'Access-Control-Allow-Origin': app_url or get_default_app_url(),
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': content_type,
            'Set-Cookie': set_cookie,
        })
