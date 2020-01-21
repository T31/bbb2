import http
import json

import BackblazeB2Api
from BackblazeB2Error import BackblazeB2BadRequestError
from BackblazeB2Error import BackblazeB2Error
import util.http

def list_all_parts(creds, file_id):
    result_list = [BackblazeB2Api.list_parts(creds, file_id)]

    while None != result_list[-1].next_part:
        result = BackblazeB2Api.list_parts(creds, file_id,
                                           result_list[-1].next_part)
        result_list.append(result)

    all_upload_parts = dict()
    for result in result_list:
        for part_num in result.upload_parts:
            all_upload_parts[part_num] = result.upload_parts[part_num]

    return BackblazeB2Api.ListPartsResult(all_upload_parts, None)

def list_all_unfinished_large_files(creds, bucket_id):
    list_of_lists = [BackblazeB2Api.list_unfinished_large_files(creds,
                                                                bucket_id)]

    while None != list_of_lists[-1].next_file:
        next_file_id = list_of_lists[-1].next_file
        new_list = BackblazeB2Api.list_unfinished_large_files(creds, bucket_id,
                                                              next_file_id)
        list_of_lists.append(new_list)

    complete_list = []
    for inner_list in list_of_lists:
        for unfinished_large_file in inner_list.unfinished_files:
            complete_list.append(unfinished_large_file)

    return BackblazeB2Api.ListUnfinishedLargeFilesResult(complete_list, None)

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
            if http.HTTPStatus.BAD_REQUEST == response.status_code:
                msg = "Bad request sent."
                msg += " " + str(response)
                raise BackblazeB2BadRequestError(msg)
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
