import base64
import http

from BackblazeB2Error import BackblazeB2Error
import util.http

API_VERSION = "v2"
AUTH_URL = util.http.Url(util.http.Protocol.HTTP,
                         util.http.Domain(["api", "backblazeb2", "com"]),
                         util.http.Path(["b2api", API_VERSION,
                                         "b2_authorize_account"]))

def authorize(account_id, application_id):
    auth = account_id + ":" + application_id
    auth = auth.encode(encoding='utf-8')
    auth = base64.b64encode(auth)
    auth = "Basic" + str(object=auth, encoding='utf-8')

    headers = dict()
    headers["Authorization"] = auth

    response = util.http.send_request(AUTH_URL, util.http.Method.GET, headers,
                                      None)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status was not OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        return json.loads(str(object=response.resp_body, encoding='utf-8'))
    except json.JSONDecodeError as e:
        msg = ("HTTP response JSON parse failed. " + str(response))
        raise BackblazeB2Error(msg)

if "__main__" == __name__:
    authorize("asdf", "asdf")
