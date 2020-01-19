import http
import json

from BackblazeB2Error import BackblazeB2Error
import util.http

def list_all_unfinished_large_files(creds, bucket_id):
    file_list = BackblazeB2Api.list_unfinished_large_files(creds, bucket_id)
    file_lists = [file_list]

    while "next_file_id" not in file_lists[-1]:
        next_file_id = file_lists[-1]["next_file_id"]
        file_list = BackblazeB2Api.list_unfinished_large_files(creds, bucket_id,
                                                               next_file_id)
        unfinished_upload_chunks.append(file_list)

    ret_val = []
    for file_list in file_lists:
        for file in file_list:
            ret_val.append(file)
    return ret_val

def send_request(url, method, headers, body, download_part=False):
    try:
        response = util.http.send_request(url, method, headers, body)

        if http.HTTPStatus.UNAUTHORIZED == response.status_code:
            resp_body = json.loads(str(object=response.resp_body,
                                       encoding='utf-8'))
            if "expired_auth_token" == resp_body["code"]:
                raise BackblazeB2ExpiredAuthError(str(response))

        if download_part:
            if ((http.HTTPStatus.OK != response.status_code)
                and (http.HTTPStatus.PARTIAL_CONTENT != response.status_code)):

                msg = "Bad HTTP response status code "
                msg += str(response.status_code) + "."
                msg += " " + str(response)
                raise BackblazeB2Error(msg)
        else:
            if http.HTTPStatus.OK != response.status_code:
                msg = "Bad HTTP response status code "
                msg += str(response.status_code) + "."
                msg += " " + str(response)
                raise BackblazeB2Error(msg)

        if download_part:
            return response.resp_body
        else:
            return json.loads(str(object=response.resp_body, encoding='utf-8'))
    except json.JSONDecodeError as e:
        msg = "Malformed JSON response. " + str(response)
        raise BackblazeB2Error(msg) from e
    except KeyError as e:
        msg = "Missing key from response. " + str(response)
        raise BackblazeB2Error(msg) from e
