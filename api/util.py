import http
import json

import Bbb2Error
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
