import http
import json

from Bbb2Error import BadRequestError
import util.http

def send_request(url, method, headers, body,
                 good_status_codes = [http.HTTPStatus.OK]):
    try:
        response = util.http.send_request(url, method, headers, body)

        if response.status_code in good_status_codes:
            return response
        elif http.HTTPStatus.UNAUTHORIZED == response.status_code:
            resp_body = json.loads(str(object=response.resp_body,
                                       encoding='utf-8'))
            if "expired_auth_token" == resp_body["code"]:
                raise Bbb2Error.ExpiredAuthError(str(response))
            else:
                raise Bbb2Error.UnauthorizedError(str(response))
        elif http.HTTPStatus.BAD_REQUEST == response.status_code:
            raise Bbb2Error.BadRequestError(str(response))
        elif http.HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code:
            raise Bbb2Error.RemoteError(str(response))
        else:
            msg = "Unhandled HTTP response status code."
            msg += " StatusCode=" + str(response.status_code)
            msg += ", Response=\"" + str(response) + "\"."
            raise Bbb2Error.ApiParseError(msg)
    except (json.JSONDecodeError, KeyError) as e:
        raise Bbb2Error.ApiParseError(str(response)) from e

def raise_appropriate_error(http_response):
    code = None
    try:
        code = json.loads(str(http_response.resp_body))["code"]
    except (json.JSONDecodeError, KeyError) as e:
        raise Bbb2Error.ApiParseError(json_str) from e

    if ((http.HTTPStatus.BAD_REQUEST == http_response.status_code)
        or (http.HTTPStatus.FORBIDDEN == http_response.status_code)
        or (http.HTTPStatus.NOT_FOUND == http_response.status_code)):
        raise BadRequestError(str(http_response))
    elif (http.HTTPStatus.UNAUTHORIZED == http_response.status_code):
        elif ("unsupported" == code):
            raise BadRequestError(str(http_response))
        elif ("expired_auth_token" == code):
            raise ExpiredAuthError(str(http_response))
        else:
            raise UnauthorizedError(str(http_response))
    else:
        raise ApiParseError(str(response))
