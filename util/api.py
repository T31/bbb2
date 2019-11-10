import http
import json

from BackblazeB2Error import BackblazeB2Error
import util.http

def send_request(url, method, headers, body):
    response = util.http.send_request(url, method, headers, body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        return json.loads(str(object=response.resp_body, encoding='utf-8'))
    except JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
