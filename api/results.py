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

    def __init__(self, http_response):
        if (http.HTTPStatus.OK == response.status_code):
            json_body = json.loads(response.resp_body)
            try:
                self.account_id = json_body["accountId"]
                self.auth_token = json_body["authorizationToken"]
                self.api_url = json_body["apiUrl"]
                self.download_url = json_body["downloadUrl"]
                self.min_part_size_bytes = json_body["absoluteMinimumPartSize"]
                self.rec_part_size_bytes = json_body["recommendedPartSize"]
            except (json.JSONDecodeError, KeyError) as e:
                raise Bbb2Error.ApiParseError(str(response)) from e
        else:
            api.util.raise_appropriate_error(response)
            assert False

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
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(response))
        else:
            api.util.raise_appropriate_error(http_response)
            assert False

class DownloadFileByIdResult:
    file_id = None
    content_len = None
    sha1 = None
    payload = None

    def __init__(self, http_response):
        if ((http.HTTPStatus.OK == http_response.status_code)
            or (http.HTTPStatus.PARTIAL_CONTENT == http_response.status_code)):
            try:
                self.file_id = http_response.resp_headers["x-bz-file-id"]
                self.content_len = http_response.resp_headers["Content-Length"]
                self.sha1 = http_response.resp_headers["x-bz-content-sha1"]
                self.payload = http_response.resp_body
            except KeyError as e:
                raise ApiParseError(str(response)) from e
        else:
            api.util.raise_appropraite_error(http_response)
            assert False

class FinishLargeFileResult:
    account_id = None
    bucket_id = None
    file_id = None

    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.account_id = json_body["accountId"]
                self.bucket_id = json_body["bucketId"]
                self.file_id = json_body["fileId"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)
            assert False

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
