import base64
import copy
import http
import hashlib
import json

from BackblazeB2Error import BackblazeB2Error
import util.api
import util.http
import util.util

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

API_VERSION = "v2"
AUTH_URL = util.http.Url(util.http.Protocol.HTTPS,
                         util.http.Domain(["api", "backblazeb2", "com"]),
                         util.http.Path(["b2api", API_VERSION,
                                         "b2_authorize_account"]))

def authorize(key_id, application_key):
    auth = key_id + ":" + application_key
    auth = auth.encode(encoding='utf-8')
    auth = base64.b64encode(auth)
    auth = "Basic" + str(object=auth, encoding='utf-8')

    headers = {"Authorization" : auth}

    response = util.api.send_request(AUTH_URL, util.http.Method.GET, headers,
                                     None)
    try:
        return {"account_id" : response["accountId"],
                "auth_token" : response["authorizationToken"],
                "api_url" : response["apiUrl"],
                "download_url" : response["downloadUrl"],
                "min_part_size_bytes" : response["absoluteMinimumPartSize"],
                "rec_part_size_bytes" : response["recommendedPartSize"]}
    except KeyError as e:
        msg = "Response missing key."
        raise BackblazeB2Error(msg) from e

def cancel_large_file(creds, file_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_cancel_large_file"])

    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id})
    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)

def copy_file(api_url, auth_token, src_file_id, dst_bucket_id, dst_file_name):
    local_api_url = copy.deepcopy(api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION, "b2_copy_file"])

    headers = {"Authorization" : auth_token}

    body = {"sourceFileId" : src_file_id,
            "fileName" : dst_file_name}
    if None != dst_bucket_id:
        body["destinationBucketId"] = dst_bucket_id
    body = json.dumps(body)

    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)

def download_file_by_id(creds, file_id, start_idx_inc, end_idx_inc):
    local_download_url = copy.deepcopy(creds.download_url)

    local_download_url.path \
    = util.http.Path(["b2api", API_VERSION,
                      "b2_download_file_by_id?fileId=" + file_id])

    range_str = "bytes=" + str(start_idx_inc) + "-" + str(end_idx_inc)
    headers = {"Authorization" : creds.auth_token, "Range" : range_str}
    body = json.dumps({"fileId" : file_id})
    return util.api.send_request(local_download_url, util.http.Method.POST,
                                 headers, body, True)

def download_file_by_name(download_url, auth_token, bucket_name, file_name,
                          start_idx_inc, end_idx_inc):
    local_download_url = copy.deepcopy(download_url)
    local_download_url.path = util.http.Path(["file", bucket_name, file_name])

    range_str = "bytes=" + str(start_idx_inc) + "-" + str(end_idx_inc)
    headers = {"Authorization" : auth_token, "Range" : range_str}
    return util.api.send_request(local_download_url, util.http.Method.GET,
                                 headers, None, True)

def finish_large_file(creds, file_id, sha1_part_hashes):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_finish_large_file"])
    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id, "partSha1Array" : sha1_part_hashes})
    util.api.send_request(local_api_url, util.http.Method.POST, headers, body)

def get_upload_part_url(creds, file_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_get_upload_part_url"])

    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"fileId" : file_id})
    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)
    try:
        return {"upload_part_url" : response["uploadUrl"],
                "upload_part_auth_token" : response["authorizationToken"],
                "file_id" : response["fileId"]}
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e

def get_upload_url(api_url, auth_token, bucket_id):
    local_api_url = copy.deepcopy(api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_get_upload_url"])

    headers = {"Authorization" : auth_token}
    body = json.dumps({"bucketId" : bucket_id})
    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)
    try:
        return {"bucket_id" : response["bucketId"],
                "upload_url" : response["uploadUrl"],
                "upload_auth_token" : response["authorizationToken"]}
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def list_buckets(creds, bucket_name = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_buckets"])

    headers = {"Authorization" : creds.auth_token}

    body = {"accountId" : creds.account_id}
    if None != bucket_name:
        body["bucketName"] = bucket_name
    body = json.dumps(body)

    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)
    try:
        ret_val = dict()
        for bucket in response["buckets"]:
            ret_val[bucket["bucketName"]] = bucket["bucketId"]
        return ret_val
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def list_file_names(creds, bucket_id):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_file_names"])
    headers = {"Authorization" : creds.auth_token}
    body = json.dumps({"bucketId" : bucket_id})
    try:
        response = util.api.send_request(local_api_url, util.http.Method.POST,
                                         headers, body)
        ret_val = dict()
        for file in response["files"]:
            entry = {"contentLength" : file["contentLength"],
                     "fileId" : file["fileId"]}
            ret_val[file["fileName"]] = entry
        return ret_val
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def list_parts(creds, file_id, start_part = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION, "b2_list_parts"])

    headers = {"Authorization" : creds.auth_token}

    body = {"fileId" : file_id}
    if None != start_part:
        body["startPartNumber"] = start_part
    body = json.dumps(body)

    try:
        response = util.api.send_request(local_api_url, util.http.Method.POST,
                                         headers, body)
        upload_parts = dict()

        for part in response["parts"]:
            upload_part = UploadPart(part["partNumber"], part["contentLength"],
                                     part["contentSha1"])
            upload_parts[int(part["partNumber"])] = upload_part

        return ListPartsResult(upload_parts, response["nextPartNumber"])
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def list_unfinished_large_files(creds, bucket_id, start_file_id = None):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_unfinished_large_files"])

    headers = {"Authorization" : creds.auth_token}

    body = {"bucketId" : bucket_id}
    if None != start_file_id:
        body["startFileId"] = start_file_id
    body = json.dumps(body)

    try:
        response = util.api.send_request(local_api_url, util.http.Method.POST,
                                         headers, body)

        file_list = []
        for file in response["files"]:
            file_list.append(UnfinishedLargeFile(file["fileId"],
                                                  file["fileName"]))

        return ListUnfinishedLargeFilesResult(file_list, response["nextFileId"])
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def start_large_file(creds, bucket_id, dst_file_name):
    local_api_url = copy.deepcopy(creds.api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_start_large_file"])

    headers = {"Authorization" : creds.auth_token}

    body = {"bucketId" : bucket_id,
            "fileName" : dst_file_name,
            "contentType" : "application/octet-stream"}
    body = json.dumps(body)

    response = util.api.send_request(local_api_url, util.http.Method.POST,
                                     headers, body)
    try:
        return response["fileId"]
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def upload_file(upload_url, upload_auth_token, dst_file_name, src_file_path,
                src_file_sha1=None):
    file_len = str(util.util.get_file_len_bytes(src_file_path))

    headers = {"Authorization" : upload_auth_token,
               "X-Bz-File-Name" : dst_file_name,
               "Content-Type" : "application/octet-stream",
               "Content-Length" : file_len}
    if None != src_file_sha1:
        headers["X-Bz-Content-Sha1"] = src_file_sha1
    else:
        headers["X-Bz-Content-Sha1"] = util.util.calc_sha1_file(src_file_path)

    body = util.util.get_entire_file(src_file_path)

    response = util.api.send_request(upload_url, util.http.Method.POST,
                                     headers, body)
    try:
        return {"bucket_id" : response["bucketId"],
                "hash_sha1" : response["contentSha1"],
                "file_id" : response["fileId"],
                "file_name" : response["fileName"]}
    except KeyError as e:
        msg = "Failed to find key in response. " + str(response)
        raise BackblazeB2Error(msg) from e

def upload_part(upload_url, auth_token, part_num, part):
    hasher = hashlib.sha1()
    hasher.update(part)

    headers = {"Authorization" : auth_token,
               "X-Bz-Part-Number" : str(part_num),
               "Content-Length" : str(len(part)),
               "X-Bz-Content-Sha1" : hasher.hexdigest()}
    body = part

    response = util.api.send_request(upload_url, util.http.Method.POST, headers,
                                     body)
    try:
        return {"part_number" : response["partNumber"],
                "sha1_hash" : hasher.hexdigest()}
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
