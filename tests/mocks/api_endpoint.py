from api.results import AuthorizeAccountResult
import enum
import http
import json
import pathlib
import util.http

class Bucket:
    def __init__(self, bucket_id, name):
        self.id = bucket_id
        self.name = name
        self.file_ids = set()

class BucketStore:
    def __init__(self):
        self.buckets_by_id = {}
        self.bucket_name_to_id = {}

    def get_by_id(self, bucket_id):
        if (None == bucket_id) or (bucket_id not in self.buckets_by_id):
            return None

        return self.buckets_by_id[bucket_id]

    def get_by_name(self, name):
        if (None == name) or (name not in self.bucket_name_to_id):
            return None

        return self.get_by_id(self.bucket_name_it_id[name])

class File:
    def __init__(self, file_id, path, data):
        self.id = file_id
        self.bucket_id = None
        self.path = pathlib.Path(path)
        self.data = data
        self.complete = True

class FileStore:
    def __init__(self):
        self.files_by_id = {}
        self.files_by_path = {}

API_VERSION = "v2"

AUTH_URL = util.http.Url(util.http.Protocol.HTTPS,
                         util.http.Domain(["api", "backblazeb2", "com"]),
                         util.http.Path(["b2api", API_VERSION,
                                         "b2_authorize_account"]))

class ApiEndpoint:
    def __init__(self):
        self.bucket_store = BucketStore()
        self.files_by_id = {}
        self.api_url = "https://api000.backblazeb2.com"
        self.download_url = "https://f000.backblazeb2.com"
        self.absoluteMinPartSizeBytes = 1024
        self.recommendedPartSizeBytes = 4096

    def handle_request(self, url, method, headers, body):
        if (url == AUTH_URL) and (util.http.Method.GET == method):
            resp_body = dict()
            resp_body["accountId"] = "mockAccountId"
            resp_body["authorizationToken"] = "mockAuthToken"
            resp_body["apiUrl"] = self.api_url
            resp_body["downloadUrl"] = self.download_url
            resp_body["absoluteMinimumPartSize"] = self.absoluteMinPartSizeBytes
            resp_body["recommendedPartSize"] = self.recommendedPartSizeBytes

            return util.http.Response(url, headers, body, http.HTTPStatus.OK,
                                      {}, json.dumps(resp_body))

        elif ((url.path == util.http.Path(["b2api", API_VERSION,
                                           "b2_cancel_large_file"]))
              and (util.http.Method.POST == method)):
            req_body = json.loads(body)
            file_id = req_body["fileId"]

            if ((file_id not in self.files_by_id)
                or (self.files_by_id[file_id].complete)):
                resp_body = {"code" : "bad_request"}
                return util.http.Response(url, headers, body,
                                          http.HTTPStatus.BAD_REQUEST, {},
                                          json.dumps(resp_body))

            bucket_id = self.files_by_id[file_id].bucket_id
            file_name = self.files_by_id[file_id].path.name
            del files_by_id[file_id]

            resp_body = {"fileId" : file_id,
                         "bucketId" : bucket_id,
                         "fileName" : file_name}

            return util.http.Response(url, headers, body, http.HTTPStatus.OK,
                                      {}, json.dumps(resp_body))
