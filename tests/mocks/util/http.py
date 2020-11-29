import http
import json

from Bbb2Error import Bbb2Error
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
    elif (url.path
          and (url.path[-1].find("b2_download_file_by_id?fileId=") != -1)
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
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_list_buckets"]))
          and (util.http.Method.POST == method)):
        resp_body = dict()
        resp_body["buckets"] = [{"bucketId" : "someBucketId",
                                 "bucketName" : "someBucketName"},
                                {"bucketId" : "anotherBucketId",
                                 "bucketName" : "anotherBucketName"}]
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_list_file_names"]))
          and (util.http.Method.POST == method)):
        resp_body = dict()
        resp_body["files"] = [{"fileName" : "someFileName",
                               "fileId" : "someFileId",
                               "contentLength" : 100},
                              {"fileName" : "someOtherFileName",
                               "fileId" : "someOtherFileId",
                               "contentLength" : 200}]
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION, "b2_list_parts"]))
          and (util.http.Method.POST == method)):
        resp_body = dict()
        parts = [{"partNumber" : 0,
                  "contentSha1" : util.util.calc_sha1(bytes([0, 1])),
                  "contentLength" : 2},
                 {"partNumber" : 1,
                  "contentSha1" : util.util.calc_sha1(bytes([1])),
                  "contentLength" : 1}]
        resp_body["parts"] = parts
        resp_body["nextPartNumber"] = 3
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_list_unfinished_large_files"]))
          and (util.http.Method.POST == method)):
        resp_body = dict()
        resp_body["files"] = [{"fileId" : "someFileId",
                               "fileName" : "someFileName"},
                              {"fileId" : "someOtherFileId",
                               "fileName" : "someOtherFileName"}]
        resp_body["nextFileId"] = "nextUnfinishedFileId"
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                       "b2_start_large_file"]))
          and (util.http.Method.POST == method)):
        resp_body = {"fileId" : "someFileId"}
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ("X-Bz-File-Name" in headers):
        resp_body = {"fileId" : "someFileId",
                     "fileName" : "someFileName",
                     "contentSha1" : util.util.calc_sha1(bytes([6, 3])),
                     "bucketId" : "someBucketId"}
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    elif ("X-Bz-Part-Number" in headers):
        resp_body = {"partNumber" : headers["X-Bz-Part-Number"],
                     "contentSha1" : util.util.calc_sha1(body)}
        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    else:
        msg = "Bad request to mock send_request." \
              + " Url=" + str(url) \
              + ", Method=" + method.name \
              + ", Headers=" + str(headers) \
              + ", Body=" + str(body)
        raise BadMockRequestError(msg)

def send_request_list_all_parts(url, method, headers, body):
    if ((url.path != util.http.Path(["b2api", API_VERSION, "b2_list_parts"]))
        or (util.http.Method.POST != method)):
        msg = "Bad request to mock send_request_list_all_parts." \
              + " Url=" + str(url) \
              + ", Method=" + method.name \
              + ", Headers=" + str(headers) \
              + ", Body=" + str(body)
        raise BadMockRequestError(msg)

    try:
        start_part = 1
        req_body_json = json.loads(body)
        if "startPartNumber" in req_body_json:
            start_part = req_body_json["startPartNumber"]

        resp_body = dict()

        parts = [{"partNumber" : start_part,
                  "contentSha1" : util.util.calc_sha1(bytes([0, 1])),
                  "contentLength" : 2},
                 {"partNumber" : start_part + 1,
                  "contentSha1" : util.util.calc_sha1(bytes([1])),
                  "contentLength" : 1}]
        resp_body["parts"] = parts

        if start_part > 10:
            resp_body["nextPartNumber"] = None
        else:
            resp_body["nextPartNumber"] = start_part + 2

        return util.http.Response(url, headers, body, http.HTTPStatus.OK, {},
                                  json.dumps(resp_body))
    except (Bbb2Error, KeyError) as e:
        msg = "Bad request to mock send_request_list_all_parts." \
              + " Url=" + str(url) \
              + ", Method=" + method.name \
              + ", Headers=" + str(headers) \
              + ", Body=" + str(body)
        raise BadMockRequestError(msg) from e
