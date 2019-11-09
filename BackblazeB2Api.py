import base64
import http

from BackblazeB2Error import BackblazeB2Error
import util.http
import util.util

API_VERSION = "v2"
AUTH_URL = util.http.Url(util.http.Protocol.HTTP,
                         util.http.Domain(["api", "backblazeb2", "com"]),
                         util.http.Path(["b2api", API_VERSION,
                                         "b2_authorize_account"]))

def authorize(account_id, application_id):
    auth = account_id + ":" + application_id
    auth = auth.encode(encoding='utf-8')
    auth = base64.b64encode(auth)
    auth = "Basic" + str(object=auth, encoding='utf-8')

    headers = dict()
    headers["Authorization"] = auth

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
    headers = dict()
    headers["Authorization"] = auth_token

    body = dict()
    body["bucketId"] = bucket_id

    response = util.http.send_request(api_url, util.http.Method.POST, headers,
                                      body)

    if http.HTTPStatus.OK != response.status_code:
        msg = "HTTP response status wasn't OK(200). " + str(response)
        raise BackblazeB2Error(msg)

    json_body = json.loads(str(object=response.resp_body, encoding='utf-8'))
    return (json_body["bucketId"], json_body["uploadUrl"],
            json_body["authorizationToken"])

def upload_file(upload_url, upload_auth_token, dst_file_name, src_file_path,
                src_file_sha1=None):
    headers = dict()
    headers["Authorization"] = upload_auth_token
    headers["X-Bz-File-Name"] = dst_file_name
    headers["Content-Type"] = "application/octet-stream"
    headers["Content-Length"] = util.util.get_file_len(src_file_path)
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

if "__main__" == __name__:
    authorize("asdf", "asdf")
