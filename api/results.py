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
        if (200 == response.status_code):
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

        err = ApiErrorResponse(str(response.resp_body))
        if (400 == response.status_code):
            raise BadRequestError(str(response))
        elif (401 == response.status_code):
            if ("unauthorized" == err.code):
                raise UnauthorizedError(str(response))
            elif ("unsupported" == err.code):
                raise BadRequestError(str(response))
            else:
                raise ApiParseError(str(response))
        elif ((403 == reponse.status_code)
              and ("transaction_cap_exceeded" == err.code)):
            raise BadRequestError(str(response))
        else:
            raise ApiParseError(str(response))

class CancelLargeFileResult:
    file_id = None
    account_id = None
    bucket_id = None
    file_name = None

    def __init__(self, http_response):
        if (200 == response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.file_id = json_body["fileId"]
                self.account_id = json_body["accountId"]
                self.bucket_id = json_body["bucketId"]
                self.file_name = json_body["fileName"]
                return
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(response))

        err = ApiErrorResponse(str(response.resp_body))
        if (400 == http_response.status_code):
            raise BadRequestError(str(response))
        elif (401 == http_response.status_code):
            if ("expired_auth_token" == err.code):
                raise ExpiredAuthError(str(response))
            else:
                raise UnauthorizedError(str(response))
        else:
            raise ApiParseError(str(response))

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

class DownloadFileByIdResult:
    file_id = None
    content_len = None
    sha1 = None
    payload = None

    def __init__(self, file_id, content_len, sha1, payload,):
        self.file_id = file_id
        self.content_len = content_len
        self.sha1 = sha1
        self.payload = payload
