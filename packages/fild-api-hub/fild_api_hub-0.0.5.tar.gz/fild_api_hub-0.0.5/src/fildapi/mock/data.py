from fild.sdk import Bool, Dictionary, Enum, Int, Raw, String

from fildapi.schema import HttpMethod


class JsonMatcher(Enum):
    IGNORE_KEY = '${json-unit.ignore-element}'


class HttpRequest(Dictionary):
    Method = String(name='method')
    Path = String(name='path')
    Params = Raw(name='queryStringParameters', required=False)
    Body = Raw(name='body', required=False)


class HttpResponse(Dictionary):
    StatusCode = Int(name='statusCode')
    Headers = Raw(name='headers', required=False)
    Cookies = Raw(name='cookies', required=False)
    Body = Raw(name='body', required=False)


class Command(Enum):
    Expectation = 'expectation'
    Reset = 'reset'
    Retrieve = 'retrieve'


class ObjectType(Enum):
    Requests = 'REQUESTS'
    ActiveExpectations = 'active_expectations'


class Params(Dictionary):
    Type = String(name='type', required=False)


class PathParams(Dictionary):
    Command = Command(name='command')


class Times(Dictionary):
    RemainingTimes = Int(name='remainingTimes')
    Unlimited = Bool(name='unlimited', required=False)


class ExpectationBody(Dictionary):
    HttpRequest = HttpRequest(name='httpRequest')
    HttpResponse = HttpResponse(name='httpResponse')
    Times = Times(name='times')


class RetrieveHttpRequest(Dictionary):
    Method = HttpMethod(name='method', required=False)
    Body = Raw(name='body', required=False)
    Path = String(name='path')


class RetrieveBody(Dictionary):
    HttpRequest = RetrieveHttpRequest(name='httpRequest')


class DataResponse(Dictionary):
    Data = Raw(name='data')


class MatchType(Enum):
    Strict = 'STRICT'
    Partial = 'ONLY_MATCHING_FIELDS'


class JsonFilter(Dictionary):
    Type = String(name='type', default='JSON')
    Json = Raw(name='json')
    MatchType = MatchType(name='matchType', default=MatchType.Partial)


class StringFilter(Dictionary):
    Type = String(name='type', default='STRING')
    String = String(name='string')
    SubString = Bool(name='subString', default=True)


class TimeToLive(Dictionary):
    Unlimited = Bool(name='unlimited')


class UnaddressedRequest(Dictionary):
    HttpRequest = HttpRequest(name='httpRequest')
    HttpResponse = HttpResponse(name='httpResponse', required=False)
    Id = String(name='id')
    Priority = Int(name='priority')
    TimeToLive = TimeToLive(name='timeToLive')
    Times = Times(name='times', required=False)
