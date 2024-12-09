# fild-api-hub

The FILD Api Hub is a set of tools enabling using FILD described contracts
in tests. 

Configure your project with yaml files in `etc/config.yaml` containing
```yaml
App:
  url: http://localhost:8000
MockServer:
  host: localhost
  port: 8088
```

Override any local configuration variables by adding `etc/local.yaml`
```yaml
MockServer:
  port: 8080
```

Use `ApiMethod` to describe the API 
```python
from fild.sdk import Dictionary, Int, String, Uuid
from fildapi import ApiMethod, HttpMethod


SERVICE = 'customer_api'
BASE_URL = 'http://mydomain.customerapi'


class CreateUserRequest(Dictionary):
    Name = String(name='name')
    Email = String(name='email')
    Age = Int(name='age', min_val=18, max_val=120)

    
class CreateUserResponse(Dictionary):
    Id = Uuid(name='id')

    
class CreateUser(ApiMethod):
    method = HttpMethod.POST
    url = 'api/users'
    req_body = CreateUserRequest
    resp_body = CreateUserResponse
```

Use `ApiMethod` for mocking and verifying integrations
```python
from customer_api import CreateUser


def test_failed_to_create_user():
    CreateUser.reply(status=400)
    # Test action to check error


def test_verify_call_to_customer_api():
    CreateUser.reply()
    # Some test action
    CreateUser.verify_called()
```

Use `ApiCaller` to test the api:
```python
from fildapi import ApiCaller
from customer_api import CreateUser


class CreateUserCall(ApiCaller):
    method = CreateUser


def test_create_user():
    CreateUserCall().request().verify_response()
```
