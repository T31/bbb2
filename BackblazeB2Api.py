import base64
import copy
import json
import http

from BackblazeB2Error import BackblazeB2Error
import util.http
import util.util

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

    response = util.http.send_request(AUTH_URL, util.http.Method.GET, headers,
                                      None)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status was not OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        return json.loads(str(object=response.resp_body, encoding='utf-8'))
    except json.JSONDecodeError as e:
        msg = ("HTTP response JSON parse failed. " + str(response))
        raise BackblazeB2Error(msg)

def cancel_large_file(api_url, auth_token, file_id):
    headers = dict()
    headers["Authorization"] = auth_token

    body = dict()
    body["fileId"] = file_id
    body = json.dumps(body)

    response = util.http.send_request(api_url, util.http.Method.POST, headers,
                                      body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

def get_upload_url(api_url, auth_token, bucket_id):
    local_api_url = copy.deepcopy(api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_get_upload_url"])

    headers = {"Authorization" : auth_token}
    body = json.dumps({"bucketId" : bucket_id})
    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))
        ret_val = dict()
        ret_val["bucket_id"] = json_body["bucketId"]
        ret_val["upload_url"] = json_body["uploadUrl"]
        ret_val["upload_auth_token"] = json_body["authorizationToken"]
        return ret_val
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
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
        headers["X-Bz-Content-Sha1"] = util.util.calc_sha1(src_file_path)

    body = util.util.get_entire_file(src_file_path)

    response = util.http.send_request(upload_url, util.http.Method.POST,
                                      headers, body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))
        ret_val = dict()
        ret_val["bucket_id"] = json_body["bucketId"]
        ret_val["hash_sha1"] = json_body["contentSha1"]
        ret_val["file_id"] = json_body["fileId"]
        ret_val["file_name"] = json_body["fileName"]
        return ret_val
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e

def list_buckets(api_url, auth_token, account_id, bucket_name=None):
    local_api_url = copy.deepcopy(api_url)
    local_api_url.path = util.http.Path(["b2api", API_VERSION,
                                         "b2_list_buckets"])

    headers = {"Authorization" : auth_token}

    body = {"accountId" : account_id}
    if None != bucket_name:
        body["bucketName"] = bucket_name
    body = json.dumps(body)

    response = util.http.send_request(local_api_url, util.http.Method.POST,
                                      headers, body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))
        ret_val = []
        for bucket in json_body["buckets"]:
            ret_val.append((bucket["bucketName"], bucket["bucketId"]))
        return ret_val
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e

def start_large_file(api_url, auth_token, bucket_id, dst_file_name):
    local_api_url = copy.deepcopy(api_url)
    local_api_url.path = Path(["b2api", API_VERSION, "b2_start_large_file"])

    headers = {"Authorization" : auth_token}

    body = {"bucketId" : bucket_id,
            "fileName" : dst_file_name,
            "contentType" : "application/octet-stream"}
    body = json.dumps(body)

    response = util.http.send_request(local_api_url, util.http.Protocol.POST,
                                      headers, body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    try:
        json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))
        return json_body["fileId"]
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Failed to find key in JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
