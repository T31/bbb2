"""
These are the exact calls of the BackblazeB2 REST API. Some of these are
annoying to use without the convenience methods in api/api.py
"""

import base64
import copy
import hashlib
import http
import json

from api.results import AuthorizeResult
from api.results import CancelLargeFileResult
from api.results import DownloadFileByIdResult
from api.results import FinishLargeFileResult
from api.results import GetUploadPartUrlResult
from api.results import GetUploadUrlResult
from api.results import ListBucketsResult
from api.results import ListFileNamesResult
from api.results import ListPartsResult
from api.results import ListUnfinishedLargeFilesResult
from api.results import StartLargeFileResult
from api.results import UploadFileResult
from api.results import UploadPartResult
import api.util
import Bbb2Error
import util.http
import util.util

API_VERSION = "v2"

def authorize(key_id: str, application_key: str) -> AuthorizeResult:
    auth = key_id + ":" + application_key
    auth = auth.encode(encoding='utf-8')
    auth = base64.b64encode(auth)
    auth = "Basic" + str(object=auth, encoding='utf-8')

    headers = {"Authorization" : auth}

    AUTH_URL = util.http.Url(util.http.Protocol.HTTPS,
                             util.http.Domain(["api", "backblazeb2", "com"]),
                             util.http.Path(["b2api", API_VERSION,
                                             "b2_authorize_account"]))

    response = util.http.send_request(AUTH_URL, util.http.Method.GET, headers,
                                      None)

    return AuthorizeResult(response)

def cancel_large_file(creds, file_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_cancel_large_file"])

    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id})

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return CancelLargeFileResult(response)

def download_file_by_id(creds, file_id, start_idx_inc, end_idx_inc):
    local_download_url = copy.deepcopy(creds.download_url)

    local_download_url.path \
    = util.http.Path(["b2api", API_VERSION,
                      "b2_download_file_by_id?fileId=" + file_id])

    range_str = "bytes=" + str(start_idx_inc) + "-" + str(end_idx_inc)
    headers = {"Authorization" : creds.auth_token, "Range" : range_str}
    body = json.dumps({"fileId" : file_id})
    response = util.http.send_request(local_download_url, util.http.Method.POST,
                                      headers, body)

    return DownloadFileByIdResult(response)

def finish_large_file(creds, file_id, sha1_part_hashes):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_finish_large_file"])
    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id,
                       "partSha1Array" : sha1_part_hashes})

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return FinishLargeFileResult(response)

def get_upload_part_url(creds, file_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_get_upload_part_url"])

    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id})

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return GetUploadPartUrlResult(response)

def get_upload_url(creds, bucket_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_get_upload_url"])

    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"bucketId" : bucket_id})
    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return GetUploadUrlResult(response)

def list_buckets(creds, bucket_name = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_buckets"])

    headers = {"Authorization" : creds.auth_token}

    body = {"accountId" : creds.account_id}
    if None != bucket_name:
        body["bucketName"] = bucket_name
    body = json.dumps(body)

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)
    
    return ListBucketsResult(response)

def list_file_names(creds, bucket_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_file_names"])
    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"bucketId" : bucket_id})

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return ListFileNamesResult(respones)

def list_parts(creds, file_id, start_part = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION, "b2_list_parts"])

    headers = {"Authorization" : creds.auth_token}

    body = {"fileId" : file_id}
    if None != start_part:
        body["startPartNumber"] = start_part
    body = json.dumps(body)

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return ListPartsResult(response)

def list_unfinished_large_files(creds, bucket_id, start_file_id = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_unfinished_large_files"])

    headers = {"Authorization" : creds.auth_token}

    body = {"bucketId" : bucket_id}
    if None != start_file_id:
        body["startFileId"] = start_file_id
    body = json.dumps(body)

    response = api.util.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)

    return ListUnfinishedLargeFilesResult(response)

def start_large_file(creds, bucket_id, dst_file_name):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_start_large_file"])

    headers = {"Authorization" : creds.auth_token}

    body = {"bucketId" : bucket_id,
            "fileName" : dst_file_name,
            "contentType" : "application/octet-stream"}
    body = json.dumps(body)

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    return StartLargeFileResult(response)

def upload_file(upload_url, upload_auth_token, dst_file_name,
                src_file_path, src_file_sha1 = None):
    file_len = str(util.util.get_file_len_bytes(src_file_path))

    headers = {"Authorization" : upload_auth_token,
               "X-Bz-File-Name" : dst_file_name,
               "Content-Type" : "application/octet-stream",
               "Content-Length" : file_len}
    if None != src_file_sha1:
        headers["X-Bz-Content-Sha1"] = src_file_sha1
    else:
        headers["X-Bz-Content-Sha1"] \
        = util.util.calc_sha1_file(src_file_path)

    body = util.util.get_entire_file(src_file_path)

    response = util.http.send_request(upload_url, util.http.Method.POST,
                                      headers, body)

    return UploadFileResult(response)

def upload_part(upload_url, auth_token, part_num, part):
    hasher = hashlib.sha1()
    hasher.update(part)

    headers = {"Authorization" : auth_token,
               "X-Bz-Part-Number" : str(part_num),
               "Content-Length" : str(len(part)),
               "X-Bz-Content-Sha1" : hasher.hexdigest()}
    body = part

    response = util.http.send_request(upload_url, util.http.Method.POST,
                                      headers, body)

    return UploadPartResult(response)
