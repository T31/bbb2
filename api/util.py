import http
import json

from Bbb2Error import BadRequestError

def raise_appropriate_error(http_response):
    bb_code = None
    try:
        bb_code = json.loads(str(http_response.resp_body))["code"]
    except (json.JSONDecodeError, KeyError) as e:
        raise Bbb2Error.ApiParseError(json_str) from e

    http_code = http_response.status_code

    if ((http.HTTPStatus.BAD_REQUEST == http_code)
        or (http.HTTPStatus.NOT_FOUND == http_code)
        or (http.HTTPStatus.METHOD_NOT_ALLOWED == http_code)
        or (http.HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE == http_code)):
        raise BadRequestError(str(http_response))
    elif (http.HTTPStatus.UNAUTHORIZED == http_code):
        if ("unsupported" == bb_code):
            raise BadRequestError(str(http_response))
        elif ("expired_auth_token" == bb_code):
            raise ExpiredAuthError(str(http_response))
        else:
            raise UnauthorizedError(str(http_response))
    elif (http.HTTPStatus.FORBIDDEN == http_code):
        raise RemoteResourceLimitError(str(http_response))
    elif (http.HTTPStatus.REQUEST_TIMEOUT == http_code):
        raise ConnectError(str(http_response))
    elif (http.HTTPStatus.SERVICE_UNAVAILABLE == http_code):
        raise RemoteError(str(http_response))
    else:
        raise ApiParseError(str(http_response))
