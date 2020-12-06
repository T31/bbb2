import copy
import log
import os
import random

from api.api import Api
import Bbb2Error
import client.util
import util.http
import util.util

class Client():
    def __init__(self):
        self.credentials = None

    def authorize(self, key_id = None, application_key = None):
        local_key_id = copy.deepcopy(key_id)
        local_application_key = copy.deepcopy(application_key)
        if (None == key_id) or (None == application_key):
            key = client.util.get_key_from_file()
            local_key_id = key.key_id
            local_application_key = key.app_key

        self.credentials = Api.authorize_account(local_key_id,
                                                 local_application_key)

        log.log_info("Authorized.")

    def cancel_all_large_files(self):
        for bucket_name in self.list_buckets():
            bucket_id = client.util.get_bucket_id_from_name(self.credentials,
                                                            bucket_name)

            unfinished_files = \
            api.api.Api.list_unfinished_large_files(self.credentials,
                                                       bucket_id)

            for file in unfinished_files.unfinished_files:
                self.cancel_large_file(file.file_id)

    def cancel_large_file(self, file_id):
        api.api.Api.cancel_large_file(self.credentials, file_id)
        print("Cancelled large file ID " + str(file_id))

    def download_file(self, src_bucket_name, src_file_path, dst_file_path):
        log.log_info("Downloading file \"" + src_file_path + "\""
                     + " from bucket \"" + src_bucket_name + "\""
                     + " to path \"" + dst_file_path + "\".")

        src_file_info = client.util.get_file_info(self.credentials,
                                                  src_bucket_name,
                                                  src_file_path)
        src_file_id = src_file_info["fileId"]
        src_file_len = src_file_info["contentLength"]
        bytes_downloaded = 0
        chunk_len = 10 * 1024 * 1024

        out_file = None
        try:
            if (os.path.exists(dst_file_path)):
                log.log_info("File already exists. Appending.")
                out_file = open(file=dst_file_path, mode='ab')
                bytes_downloaded = util.util.get_file_len_bytes(dst_file_path)
            else:
                out_file = open(file=dst_file_path, mode='wb')

            while bytes_downloaded < src_file_len:
                start_idx_inc = bytes_downloaded
                end_idx_inc = bytes_downloaded + chunk_len
                if end_idx_inc > src_file_len:
                    end_idx_inc = src_file_len - 1

                result = api.api.Api.download_file_by_id(self.credentials,
                                                            src_file_id,
                                                            start_idx_inc,
                                                            end_idx_inc)
                out_file.write(result.payload)
                bytes_downloaded += len(result.payload)

                percent = util.util.gen_fraction_percent_str(bytes_downloaded,
                                                             src_file_len)
                log.log_info("Downloading. " + percent + ".")
        finally:
            if None != out_file:
                out_file.close()

    def list_buckets(self, bucket_name=None):
        return api.api.Api.list_buckets(self.credentials, bucket_name)

    def upload_file(self, bucket_name, dst_file_name, src_file_path):
        file_len = util.util.get_file_len_bytes(src_file_path)

        log.log_info("Uploading file \"" + str(src_file_path) + "\"."
                     + " FileLen=" + str(file_len) + ".")

        if file_len > SessionCredentials.MAX_FILE_BYTES:
            raise Bbb2Error.Bbb2Error("File \"" + str(src_file_path) + "\""
                                   + " exceeds max file bytes "
                                   + str(SessionCredentials.MAX_FILE_BYTES) + ".")

        if file_len <= self.credentials.recommended_upload_part_bytes:
            client.util.upload_file_small(self.credentials, bucket_name,
                                          dst_file_name, src_file_path)
        else:
            uploaded_parts = client.util.UnfinishedUpload()

            while True:
                try:
                    client.util.upload_file_big(self.credentials, src_file_path,
                                                bucket_name, dst_file_name,
                                                uploaded_parts)
                    return
                except Bbb2Error.ExpiredAuthError:
                    log.log_warning("Reauthorizing.")
                    self.authorize()
                except Bbb2Error.RemoteError as e:
                    exc_msg = e.__class__.__name__ + ": " + str(e)
                    seconds = random.randrange(60, 300)
                    msg = ("Backblaze server error. " + exc_msg + "."
                           + " Sleeping for " + str(seconds) + " seconds.")

                    log.log_warning(msg)
                    sleep(seconds)
                    continue
