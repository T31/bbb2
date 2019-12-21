import copy
import os

import BackblazeB2Api
from BackblazeB2Error import BackblazeB2Error
from BackblazeB2Error import BackblazeB2ExpiredAuthError
import util.client
import util.http
import util.util

class BackblazeB2Client:
    account_id = None
    auth_token = None
    api_url = None
    download_url = None
    min_upload_part_bytes = None
    recommended_upload_part_bytes = None

    TERABYTE = 1099511627776
    MAX_FILE_BYTES = 10 * TERABYTE

    MAX_UPLOAD_PARTS = 10000

    def authorize(self, key_id=None, application_key=None):
        temp_key_id = copy.deepcopy(key_id)
        temp_application_key = copy.deepcopy(application_key)
        if (None == key_id) or (None == application_key):
            cred_pair = util.client.get_cred_from_default_file()
            temp_key_id = cred_pair[0]
            temp_application_key = cred_pair[1]

        response = BackblazeB2Api.authorize(temp_key_id, temp_application_key)
        self.account_id = response["account_id"]
        self.auth_token = response["auth_token"]
        self.api_url = util.http.Url(util.http.Protocol.HTTP, [], [])
        self.api_url.from_string(response["api_url"])
        self.download_url = util.http.Url(util.http.Protocol.HTTP, [], [])
        self.download_url.from_string(response["download_url"])
        self.min_upload_part_bytes = response["min_part_size_bytes"]
        self.recommended_upload_part_bytes = response["rec_part_size_bytes"]

    def cancel_all_large_files(self):
        for (bucket_name, bucket_id) in self.list_buckets():
            for file_id in BackblazeB2Api.list_unfinished_large_files(self.api_url,
                                                                      self.auth_token,
                                                                      bucket_id):
                self.cancel_large_file(file_id)

    def cancel_large_file(self, file_id):
        BackblazeB2Api.cancel_large_file(self.api_url, self.auth_token, file_id)
        print("Cancelled large file ID " + str(file_id))

    def copy_file(self, src_file_id, dst_bucket_name, dst_file_name):
        dst_bucket_id = BackblazeB2Api.list_buckets(self.api_url,
                                                    self.auth_token,
                                                    self.account_id,
                                                    dst_bucket_name)[0][1]

        BackblazeB2Api.copy_file(self.api_url, self.auth_token, src_file_id,
                                 dst_bucket_id, dst_file_name)

    def download_file(self, src_bucket_name, src_file_name, dst_file_path):
        src_file_info = util.client.get_file_info(self.api_url, self.auth_token,
                                                  self.account_id,
                                                  src_bucket_name,
                                                  src_file_name)
        src_file_id = src_file_info["fileId"]
        src_file_len = src_file_info["contentLength"]
        bytes_downloaded = 0
        chunk_len = 10 * 1024 * 1024

        out_file = None
        try:
            if (os.path.exists(dst_file_path)):
                out_file = open(file=dst_file_path, mode='ab')
                bytes_downloaded = util.util.get_file_len_bytes(dst_file_path)
            else:
                out_file = open(file=dst_file_path, mode='wb')

            while bytes_downloaded < src_file_len:
                start_idx_inc = bytes_downloaded
                end_idx_inc = bytes_downloaded + chunk_len
                if end_idx_inc > src_file_len:
                    end_idx_inc = src_file_len - 1

                data = BackblazeB2Api.download_file_by_id(self.download_url,
                                                          self.auth_token,
                                                          src_file_id,
                                                          start_idx_inc,
                                                          end_idx_inc)
                out_file.write(data)
                bytes_downloaded += len(data)
                print("Bytes downloaded: " + str(bytes_downloaded))
        finally:
            out_file.close()

    def list_buckets(self, bucket_name=None):
        return BackblazeB2Api.list_buckets(self.api_url, self.auth_token,
                                           self.account_id, bucket_name)

    def upload_file(self, bucket_name, dst_file_name, src_file_path):
        file_len = util.util.get_file_len_bytes(src_file_path)
        print("Uploading file \"" + str(src_file_path) + "\"."
              + " FileLen=" + str(file_len) + ".")

        if file_len > self.MAX_FILE_BYTES:
            raise BackblazeB2Error("File \"" + str(src_file_path) + "\""
                                   + " exceeds max file bytes "
                                   + str(self.MAX_FILE_BYTES) + ".")

        if file_len <= self.recommended_upload_part_bytes:
            util.client.upload_file_small(bucket_name, dst_file_name,
                                          src_file_path)
            return

        part_len = self.recommended_upload_part_bytes
        if (file_len > (self.recommended_upload_part_bytes
                        * self.MAX_UPLOAD_PARTS)):
            part_len = file_len // (self.MAX_UPLOAD_PARTS - 1)

        print("Part length is " + str(part_len) + ".")

        file_id = util.client.start_large_file(self.api_url, self.auth_token,
                                               self.account_id, bucket_name,
                                               dst_file_name)

        print("Upload file ID is " + str(file_id) + ".")

        part_hashes = []
        while True:
            try:
                return util.client.upload_file_big(src_file_path, self.api_url,
                                                   self.auth_token, file_id,
                                                   part_len, part_hashes)
            except BackblazeB2ExpiredAuthError as e:
                print("Reauthorizing.")
                self.authorize()
