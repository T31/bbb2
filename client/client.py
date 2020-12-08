import log
import os
import random

from api.api import Api
import Bbb2Error
import client.internal
import util.util

class Client(client.internal.Internal):
    def authorize(self, app_key = None):
        return super().authorize(app_key)

    def cancel_all_large_files(self):
        self.init_auth()
        for bucket_id in self.list_buckets().buckets:

            unfinished_files = \
            Api.list_unfinished_large_files(self.credentials, bucket_id)

            for unfinished_file in unfinished_files.unfinished_files:
                self.cancel_large_file(unfinished_file.file_id)

    def cancel_large_file(self, file_id):
        self.init_auth()
        Api.cancel_large_file(self.credentials, file_id)
        log.log_info("Cancelled large file ID \"" + str(file_id) + "\"")

    def download_file(self, src_bucket_name, src_file_path, dst_file_path):
        self.init_auth()
        log.log_info("Downloading file \"" + src_file_path + "\""
                     + " from bucket \"" + src_bucket_name + "\""
                     + " to path \"" + dst_file_path + "\".")

        src_file_info = self.get_file_info(src_bucket_name, src_file_path)
        if None == src_file_info:
            msg = "Unable to find file \"" + str(src_file_path) + "\"" \
                  + " in bucket \"" + str(src_bucket_name) + "\"." \
                  + " Unable to download file."
            log.log_warning(msg)
            return False

        src_file_id = src_file_info.file_id
        src_file_len = src_file_info.content_length
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

                result = Api.download_file_by_id(self.credentials, src_file_id,
                                                 start_idx_inc, end_idx_inc)

                out_file.write(result.payload)
                bytes_downloaded += len(result.payload)

                percent = util.util.gen_fraction_percent_str(bytes_downloaded,
                                                             src_file_len)
                log.log_info("Downloading. " + percent + ".")
        finally:
            if None != out_file:
                out_file.close()

        return True

    def list_buckets(self, bucket_name = None):
        self.init_auth()
        return Api.list_buckets(self.credentials, bucket_name)

    def upload_file(self, bucket_name, dst_file_name, src_file_path):
        self.init_auth()
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
