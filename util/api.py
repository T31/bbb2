import http
import json

from BackblazeB2Error import BackblazeB2Error
import util.http

def send_request(url, method, headers, body, download_part=False):
    try:
        response = util.http.send_request(url, method, headers, body)

        if http.HTTPStatus.UNAUTHORIZED == response.status_code:
            resp_body = json.loads(str(object=response.resp_body,
                                       encoding='utf-8'))
            if "expired_auth_token" == resp_body["code"]:
                raise BackblazeB2ExpiredAuthError(str(response))

        if download_part:
            if ((http.HTTPStatus.OK != response.status_code)
                and (http.HTTPStatus.PARTIAL_CONTENT != response.status_code)):

                msg = "Bad HTTP response status code "
                msg += str(response.status_code) + "."
                msg += " " + str(response)
                raise BackblazeB2Error(msg)
        else:
            if http.HTTPStatus.OK != response.status_code:
                msg = "Bad HTTP response status code "
                msg += str(response.status_code) + "."
                msg += " " + str(response)
                raise BackblazeB2Error(msg)

        if download_part:
            return response.resp_body
        else:
            return json.loads(str(object=response.resp_body, encoding='utf-8'))
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Missing key from response. " + str(response)
        raise BackblazeB2Error(msg) from e
