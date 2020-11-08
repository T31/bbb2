import http
import json

from api.util import ApiErrorResponse
from Bbb2Error import ApiParseError
from Bbb2Error import BadRequestError
from Bbb2Error import UnauthorizedError

class AuthorizeResult:
    account_id = None
    auth_token = None
    api_url = None
    download_url = None
    min_part_size_bytes = None
    rec_part_size_bytes = None

    def __init__(self, account_id, auth_token, api_url, download_url,
                 min_part_size_bytes, rec_part_size_bytes):
        self.account_id = account_id
        self.auth_token = auth_token
        self.api_url = util.http.Url.from_string(api_url)
        self.download_url = util.http.Url.from_string(download_url)
        self.min_part_size_bytes = min_part_size_bytes
        self.rec_part_size_bytes = rec_part_size_bytes

    @staticmethod
    def from_http_response(response):
        if (http.HTTPStatus.OK == response.status_code):
            json_body = json.loads(response.resp_body)
            try:
                return AuthorizeResult(resp_json["accountId"],
                                       resp_json["authorizationToken"],
                                       resp_json["apiUrl"],
                                       resp_json["downloadUrl"],
                                       resp_json["absoluteMinimumPartSize"],
                                       resp_json["recommendedPartSize"])
            except (json.JSONDecodeError, KeyError) as e:
                raise Bbb2Error.ApiParseError(str(response)) from e

        api.util.raise_appropriate_error(response)

class CancelLargeFileResult:
    file_id = None
    account_id = None
    bucket_id = None
    file_name = None

    def __init__(self, http_response):
        if (http.HTTPStatus.OK == response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.file_id = json_body["fileId"]
                
                self.bucket_id = json_body["bucketId"]
                self.file_name = json_body["fileName"]
                return
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(response))

        api.util.raise_appropriate_error(http_response)

class DownloadFileByIdResult:
    file_id = None
    content_len = None
    sha1 = None
    payload = None

    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                self.file_id = http_response.resp_headers["x-bz-file-id"]
                self.content_len = http_response.resp_headers["Content-Length"]
                self.sha1 = http_response.resp_headers["x-bz-content-sha1"]
                self.payload = http_response.resp_body
            except KeyError as e:
                raise ApiParseError(str(response)) from e

        err = ApiErrorResponse(str(http_response.resp_body))

class UploadPart:
    part_num = None
    content_len = None
    sha1 = None

    def __init__(self, part_num, content_len, sha1):
        self.part_num = part_num
        self.content_len = content_len
        self.sha1 = sha1

class ListPartsResult:
    upload_parts = None
    next_part = None

    def __init__(self, upload_parts, next_part):
        self.upload_parts = upload_parts
        self.next_part = next_part

class UnfinishedLargeFile:
    file_id = None
    file_name = None

    def __init__(self, file_id, file_name):
        self.file_id = file_id
        self.file_name = file_name

class ListUnfinishedLargeFilesResult:
    unfinished_files = None
    next_file = None

    def __init__(self, unfinished_files, next_file):
        self.unfinished_files = unfinished_files
        self.next_file = next_file
