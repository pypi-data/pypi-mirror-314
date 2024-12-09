from tests.data.dummy_api import CheckCall, CheckParamsCall, PathParams


def test_schema_relative_url():
    assert CheckCall.get_relative_url() == '/dummyurl/api/check_call'


def test_schema_relative_parametrized_url():
    url = CheckParamsCall.get_relative_url(
        path_params=PathParams().with_values({
            PathParams.Id.name: 1,
            PathParams.Param.name: 'temp'
        })
    )
    assert url == '/dummyurl/api/1/get/temp'


def test_get_service_name():
    assert CheckCall.get_service_name() == 'dummy'


def test_get_base_url():
    assert CheckCall.get_base_url() == 'http://baseurl'


def test_api_base_url():
    assert CheckCall.get_api_base_url() == 'dummyurl/'


def test_request_url():
    assert CheckCall.get_request_url() == (
        'http://baseurl/dummyurl/api/check_call'
    )


def test_get_fe_headers():
    assert CheckCall.fe_headers() == {
        'Access-Control-Allow-Origin': 'http://localhost:9000',
        'Access-Control-Allow-Credentials': 'true',
        'Content-Type': 'application/json'
    }


def test_get_full_fe_headers():
    assert CheckCall.fe_headers(content_type='json', set_cookie=True) == {
        'Access-Control-Allow-Origin': 'http://localhost:9000',
        'Access-Control-Allow-Credentials': 'true',
        'Content-Type': 'json',
        'Set-Cookie': True,
    }
