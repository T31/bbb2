import json
import os
import pathlib

import BackblazeB2Api
from BackblazeB2Error import BackblazeB2Error

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
    for bucket in buckets:
        if bucket_name == bucket[0]:
            return bucket[1]

    return None
