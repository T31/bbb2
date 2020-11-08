import http
import json

from tests.test_errors import BadMockRequestError
import util.http

API_VERSION = "v2"

AUTH_URL = util.http.Url(util.http.Protocol.HTTPS,
                         util.http.Domain(["api", "backblazeb2", "com"]),
                         util.http.Path(["b2api", API_VERSION,
                                         "b2_authorize_account"]))

def send_request(url, method, headers, body):
    if (url == AUTH_URL) and (util.http.Method.GET == method):
        resp_body = dict()
        resp_body["accountId"] = "someAccountId"
        resp_body["authorizationToken"] = "someAuthToken"
        resp_body["apiUrl"] = "someApiUrl"
        resp_body["downloadUrl"] = "someDownloadUrl"
        resp_body["absoluteMinimumPartSize"] = "someMinPartSize"
        resp_body["recommendedPartSize"] = "someRecPartSize"

        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    else:
        msg = "Bad request to mock send_request." \
              + " Url=" + str(url) \
              + ", Method=" + method.name \
              + ", Headers=" + str(headers) \
              + ", Body=" + str(body)
        raise BadMockRequestError(msg)
