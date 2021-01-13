import http
import json

from Bbb2Error import ApiParseError
from Bbb2Error import BadRequestError
from Bbb2Error import InternalError
from Bbb2Error import UnauthorizedError
from util.http import Url

class AuthorizeAccountResult:
    def __init__(self, http_response):
        self.account_id = None
        self.auth_token = None
        self.api_url = None
        self.download_url = None
        self.min_part_size_bytes = None
        self.rec_part_size_bytes = None

        if (None == http_response):
            return

        if (http.HTTPStatus.OK == http_response.status_code):
            json_body = json.loads(http_response.resp_body)
            try:
                self.account_id = json_body["accountId"]
                self.auth_token = json_body["authorizationToken"]
                self.api_url = Url.from_string(json_body["apiUrl"])
                self.download_url = Url.from_string(json_body["downloadUrl"])
                self.min_part_size_bytes = json_body["absoluteMinimumPartSize"]
                self.rec_part_size_bytes = json_body["recommendedPartSize"]
            except (InternalError, json.JSONDecodeError, KeyError) as e:
                raise Bbb2Error.ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class CancelLargeFileResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.file_id = json_body["fileId"]
                self.bucket_id = json_body["bucketId"]
                self.file_name = json_body["fileName"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response))
        else:
            api.util.raise_appropriate_error(http_response)

class DownloadFileByIdResult:
    def __init__(self, http_response):
        if ((http.HTTPStatus.OK == http_response.status_code)
            or (http.HTTPStatus.PARTIAL_CONTENT == http_response.status_code)):
            try:
                self.file_id = http_response.resp_headers["x-bz-file-id"]
                self.content_len = http_response.resp_headers["Content-Length"]
                self.sha1 = http_response.resp_headers["x-bz-content-sha1"]
                self.payload = http_response.resp_body
            except KeyError as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropraite_error(http_response)

class FinishLargeFileResult:
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

class GetUploadPartUrlResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.upload_part_url = Url.from_string(json_body["uploadUrl"])
                self.upload_part_auth_token = json_body["authorizationToken"]
                self.file_id = json_body["fileId"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class GetUploadUrlResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.bucket_id = json_body["bucketId"]
                self.upload_url = Url.from_string(json_body["uploadUrl"])
                self.upload_auth_token = json_body["authorizationToken"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class ListBucketsResult:
    def __init__(self, http_response):
        self.buckets = dict()

        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                for bucket in json_body["buckets"]:
                    self.buckets[bucket["bucketId"]] = bucket["bucketName"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class FileNameEntry:
    def __init__(self, file_name, file_id, content_length):
        self.file_name = file_name
        self.file_id = file_id
        self.content_length = content_length

class ListFileNamesResult:
    def __init__(self, http_response):
        self.file_names = []

        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                for file_entry in json_body["files"]:
                    new_entry = FileNameEntry(file_entry["fileName"],
                                              file_entry["fileId"],
                                              file_entry["contentLength"])
                    self.file_names.append(new_entry)
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class UploadPart:
    def __init__(self, part_num, content_len, sha1):
        self.part_num = part_num
        self.content_len = content_len
        self.sha1 = sha1

class ListPartsResult:
    def __init__(self, http_response = None):
        self.upload_parts = dict()
        self.next_part = None

        if None == http_response:
            return

        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.next_part = json_body["nextPartNumber"]
                for part in json_body["parts"]:
                    new_part = UploadPart(part["partNumber"],
                                          part["contentLength"],
                                          part["contentSha1"])
                    self.upload_parts[new_part.part_num] = new_part
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class UnfinishedLargeFile:
    def __init__(self, file_id, file_name):
        self.file_id = file_id
        self.file_name = file_name

class ListUnfinishedLargeFilesResult:
    def __init__(self, http_response = None):
        self.unfinished_files = []
        self.next_file = None

        if None == http_response:
            return

        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.next_file = json_body["nextFileId"]
                for cur_file in json_body["files"]:
                    new_file = UnfinishedLargeFile(cur_file["fileId"],
                                                   cur_file["fileName"])
                    self.unfinished_files.append(new_file)
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class StartLargeFileResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.file_id = json_body["fileId"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class UploadFileResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.file_id = json_body["fileId"]
                self.file_name = json_body["fileName"]
                self.sha1 = json_body["contentSha1"]
                self.bucket_id = json_body["bucketId"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)

class UploadPartResult:
    def __init__(self, http_response):
        if (http.HTTPStatus.OK == http_response.status_code):
            try:
                json_body = json.loads(http_response.resp_body)
                self.part_number = json_body["partNumber"]
                self.sha1 = json_body["contentSha1"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ApiParseError(str(http_response)) from e
        else:
            api.util.raise_appropriate_error(http_response)
