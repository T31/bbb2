import json
import pathlib

import BackblazeB2Api

def get_cred_from_default_file(self):
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
        return (cred_file_contents["accountId"],
                cred_file_contents["applicationId"])
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