import http
import json

from BackblazeB2Error import BackblazeB2Error
import util.http

def send_request(url, method, headers, body, partial=False):
    try:
        response = util.http.send_request(url, method, headers, body)
        json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))

        if http.HTTPStatus.UNAUTHORIZED == response.status_code:
            if "expired_auth_token" == json_body["code"]:
                raise BackblazeB2ExpiredAuthError(str(response))

        if partial:
            if ((http.HTTPStatus.OK != response.status_code)
                and (http.HTTPStatus.PARTIAL_CONTENT != response.status_code)):

                msg = "Bad HTTP response status code "
                msg += str(reponse.status_code) + "."
                raise BackblazeB2Error(msg)
        else:
            if http.HTTPStatus.OK != response.status_code:
                msg = "Bad HTTP response status code "
                msg += str(reponse.status_code) + "."
                raise BackblazeB2Error(msg)

        return json_body
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Missing key from response. " + str(response)
        raise BackblazeB2Error(msg) from e
