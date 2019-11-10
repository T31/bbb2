import copy

import BackblazeB2Api
from BackblazeB2Error import BackblazeB2Error
import util.client
import util.http

class BackblazeB2Client:
    account_id = None
    auth_token = None
    api_url = None
    download_url = None
    min_upload_part_bytes = None
    recommended_upload_part_bytes = None

    upload_auth_token = None
    upload_url = None

    def authorize(self, key_id=None, application_key=None):
        temp_key_id = copy.deepcopy(key_id)
        temp_application_key = copy.deepcopy(application_key)
        if (None == key_id) or (None == application_key):
            cred_pair = util.client.get_cred_from_default_file()
            temp_key_id = cred_pair[0]
            temp_application_key = cred_pair[1]

        response = BackblazeB2Api.authorize(temp_key_id, temp_application_key)
        try:
            temp_account_id = response["accountId"]
            temp_auth_token = response["authorizationToken"]
            temp_api_url = util.http.Url(util.http.Protocol.HTTP, [], [])
            temp_api_url.from_string(response["apiUrl"])
            temp_download_url = util.http.Url(util.http.Protocol.HTTP, [], [])
            temp_download_url.from_string(response["downloadUrl"])
            temp_min_upload_part_bytes = response["absoluteMinimumPartSize"]
            temp_recommended_upload_part_bytes = response["recommendedPartSize"]
        except KeyError as e:
            msg = "Response was missing value. " + str(response)
            raise BackblazeB2Error(msg) from e

        self.account_id = temp_account_id
        self.auth_token = temp_auth_token
        self.api_url = temp_api_url
        self.download_url = temp_download_url
        self.min_upload_part_bytes = temp_min_upload_part_bytes
        self.recommended_upload_part_bytes = temp_recommended_upload_part_bytes

    def cancel_large_file(self, file_id):
        BackblazeB2Api.cancel_large_file(api_url, auth_token, file_id)

    def list_buckets(self, bucket_name=None):
        return BackblazeB2Api.list_buckets(self.api_url, self.auth_token,
                                           self.account_id, bucket_name)

    def upload_file(self, bucket_name, dst_file_name, src_file_path):
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
