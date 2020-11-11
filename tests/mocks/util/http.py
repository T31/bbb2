import http
import json

from tests.test_errors import BadMockRequestError
import util.http
import util.util

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
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_cancel_large_file"]))
          and (util.http.Method.POST == method)):
        req_body = json.loads(body)
        resp_body = dict()
        resp_body["fileId"] = req_body["fileId"]
        resp_body["bucketId"] = "someBucketId"
        resp_body["fileName"] = "someFileName"
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path[-1].find("b2_download_file_by_id?fileId=") != -1)
          and (util.http.Method.POST == method)):
        payload = bytes([0, 0, 0, 0])
        req_body = json.loads(body)
        resp_headers = dict()
        resp_headers["x-bz-file-id"] = req_body["fileId"]
        resp_headers["Content-Length"] = len(payload)
        resp_headers["x-bz-content-sha1"] = util.util.calc_sha1(payload)
        return util.http.Response(url, headers, body, http.HTTPStatus.OK,
                                  resp_headers, payload)
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_finish_large_file"]))
          and (util.http.Method.POST == method)):
        req_body = json.loads(body)
        resp_body = dict()
        resp_body["accountId"] = "someAccountId"
        resp_body["bucketId"] = "someBucketId"
        resp_body["fileId"] = req_body["fileId"]
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_get_upload_part_url"]))
          and (util.http.Method.POST == method)):
        resp_body = dict()
        resp_body["fileId"] = "someFileId"
        resp_body["authorizationToken"] = "someUploadAuthToken"
        resp_body["uploadUrl"] = "https://pod-000-1016-09.backblaze.com/b2api/"
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_get_upload_url"]))
          and (util.http.Method.POST == method)):
        req_body = json.loads(body)
        resp_body = dict()
        resp_body["bucketId"] = req_body["bucketId"]
        resp_body["uploadUrl"] = "https://url.backablaze.com/upload"
        resp_body["authorizationToken"] = "someAuthToken"
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    else:
        msg = "Bad request to mock send_request." \
              + " Url=" + str(url) \
              + ", Method=" + method.name \
              + ", Headers=" + str(headers) \
              + ", Body=" + str(body)
        raise BadMockRequestError(msg)
