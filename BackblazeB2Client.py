import BackblazeB2Api
import BackblazeB2ClientUtil
from BackblazeB2Error import BackblazeB2Error
import util.http

class BackblazeB2Client:
    account_id = None
    auth_token = None
    api_url = None
    download_url = None
    min_upload_part_bytes = None
    recommended_upload_part_bytes = None

    def authorize(self, account_id=None, application_id=None):
        temp_account_id = account_id
        temp_application_id = application_id
        if (None == account_id) or (None == application_id):
            cred_pair = BackblazeB2ClientUtil.get_cred_from_default_file()
            temp_account_id = cred_pair[0]
            temp_application_id = cred_pair[1]

        response = BackblazeB2Api.authorize(temp_account_id,
                                            temp_application_id)
        try:
            temp_auth_token = response["authorizationToken"]
            temp_api_url = util.http.Url(Protocol.HTTP, [], [])
            temp_api_url.from_string(response["apiUrl"])
            temp_download_url = util.http.Url(Protocol.HTTP, [], [])
            temp_download_url.from_string(response["downloadUrl"])
            temp_min_upload_part_bytes = response["absoluteMinimumPartSize"]
            temp_recommended_upload_part_bytes = response["recommendedPartSize"]
        except KeyError as e:
            msg = "Response was missing value. " + str(response)
            raise BackblazeB2Error(msg) from e

        self.account_id = account_id
        self.auth_token = temp_auth_token
        self.api_url = temp_api_url
        self.download_url = temp_download_url
        self.min_upload_part_bytes = temp_min_upload_part_bytes
        self.recommended_upload_part_bytes = temp_recommended_upload_part_bytes

    def cancel_large_file(self, file_id):
        BackblazeB2Api.cancel_large_file(api_url, auth_token, file_id)
