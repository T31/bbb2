import json
import os
import pathlib

import BackblazeB2Api
from BackblazeB2Error import BackblazeB2ConnectError
from BackblazeB2Error import BackblazeB2Error
from BackblazeB2Error import BackblazeB2ExpiredAuthError
import util

def get_cred_from_default_file():
    cred_file_path = pathlib.Path.home() / ".bbb2_cred.json"

    cred_file = None
    try:
        cred_file = open(file=str(cred_file_path), mode='r',
                         encoding='utf-8')
    except OSError as e:
        msg = ("Failed to open credential file."
               + " CredFilePath=\"" + str(cred_file_path) + "\".")
        raise BackblazeB2Error(msg) from e

    try:
        cred_file_contents = json.load(cred_file)
        return (cred_file_contents["keyId"],
                cred_file_contents["applicationKey"])
    except json.JSONDecodeError as e:
        msg = ("Failed to parse credential file."
               + " CredFilePath=\"" + str(cred_file_path) + "\".")
        raise BackblazeB2Error(msg)
    except KeyError as e:
        msg = ("Failed to find key in credential file."
               + " CredFilePath=\"" + str(cred_file_path) + "\".")
        raise BackblazeB2Error(msg) from e
    finally:
        cred_file.close()

def get_bucket_id_from_name(api_url, auth_token, account_id, bucket_name):
    buckets = BackblazeB2Api.list_buckets(api_url, auth_token, account_id,
                                          bucket_name)
    try:
        return buckets[bucket_name]
    except KeyError as e:
        raise BackblazeB2Error("No bucket ID found for bucket name \""
                               + bucket_name + "\".") from e

def upload_file_small(self, bucket_name, dst_file_name, src_file_path):
    bucket_id = util.client.get_bucket_id_from_name(self.api_url,
                                                    self.auth_token,
                                                    self.account_id,
                                                    bucket_name)
    if None == bucket_id:
        raise BackblazeB2Error("Unable to find bucket name \"" + bucket_name
                               + "\".")

    vals = BackblazeB2Api.get_upload_url(self.api_url, self.auth_token,
                                         bucket_id)

    upload_url = util.http.Url(util.http.Protocol.HTTPS, [], [])
    upload_url.from_string(vals["upload_url"])

    upload_auth_token = vals["upload_auth_token"]

    results = BackblazeB2Api.upload_file(upload_url, upload_auth_token,
                                         dst_file_name, src_file_path)
    msg = "File upload complete."
    msg += " SrcFilePath=\"" + str(src_file_path) + "\""
    msg += ", DstFileName=\"" + results["file_name"] + "\""
    msg += ", FileId=\"" + results["file_id"] + "\""
    msg += ", BucketId=\"" + results["bucket_id"] + "\""
    msg += ", FileHashSha1=\"" + results["hash_sha1"] + "\"."
    print(msg)

def start_large_file(api_url, auth_token, account_id, bucket_name,
                     dst_file_name):
    bucket_id = util.client.get_bucket_id_from_name(api_url, auth_token,
                                                    account_id, bucket_name)

    return BackblazeB2Api.start_large_file(api_url, auth_token, bucket_id,
                                           dst_file_name)

def upload_file_big(src_file_path, api_url, auth_token, file_id, part_len,
                    part_hashes):
    file_len = util.util.get_file_len_bytes(src_file_path)

    src_file = util.util.open_binary_read_file(src_file_path)
    src_file.seek(part_len * len(part_hashes))

    results = BackblazeB2Api.get_upload_part_url(api_url, auth_token, file_id)
    upload_url = util.http.Url(None, None, None)
    upload_url.from_string(results["upload_part_url"])
    upload_auth_token = results["upload_part_auth_token"]

    part = util.util.read_file_chunk(src_file, part_len)
    while len(part) > 0:
        try:
            result = BackblazeB2Api.upload_part(upload_url,
                                                upload_auth_token,
                                                len(part_hashes) + 1, part)
            part_hashes.append(result["sha1_hash"])

            percent = str((part_len * len(part_hashes)) / file_len) + "%"
            fraction = str(part_len * len(part_hashes)) + "/" + str(file_len)
            print("Part uploaded. " + fraction + " (" + percent + ").")

            part = util.util.read_file_chunk(src_file, part_len)
        except BackblazeB2ExpiredAuthError as e:
            print("Refreshing upload URL.")
            results = BackblazeB2Api.get_upload_part_url(api_url, auth_token,
                                                         file_id)
            upload_url = results["upload_part_url"]
            upload_auth_token = results["upload_part_auth_token"]
        except BackblazeB2ConnectError as e:
            print("Refreshing upload URL.")
            results = BackblazeB2Api.get_upload_part_url(api_url, auth_token,
                                                         file_id)
            upload_url = results["upload_part_url"]
            upload_auth_token = results["upload_part_auth_token"]

    BackblazeB2Api.finish_large_file(api_url, auth_token, file_id, part_hashes)

def get_file_info(api_url, auth_token, account_id, bucket_name, file_name):
    bucket_id = util.client.get_bucket_id_from_name(api_url, auth_token,
                                                    account_id, bucket_name)
    bucket_files = BackblazeB2Api.list_file_names(api_url, auth_token,
                                                  bucket_id)
    try:
        return bucket_files[file_name]
    except KeyError as e:
        msg = "Unable to get file info."
        msg += " AccountID=\"" + str(account_id) + "\""
        msg += ", bucketName=\"" + bucket_name + "\""
        msg += ", fileName=\"" + file_name + "\"."
        raise BackblazeB2Error(msg) from e
