import copy
import json
import os
import pathlib

from api.api import Api
import Bbb2Error
import log
import util

class AppKey:
    def __init__(self, key_id, app_key):
        self.key_id = key_id
        self.app_key = app_key

class UploadFileLimits:
    TERABYTE = 1024 * 1024 * 1024 * 1024
    MAX_FILE_BYTES = 10 * TERABYTE
    MAX_UPLOAD_PARTS = 10000

class Internal:
    def __init__(self):
        self.credentials = None

    def authorize(self, key_id = None, application_key = None):
        local_key_id = copy.deepcopy(key_id)
        local_application_key = copy.deepcopy(application_key)
        if (None == key_id) or (None == application_key):
            key = self.get_key_from_file()
            local_key_id = key.key_id
            local_application_key = key.app_key

        self.credentials = Api.authorize_account(local_key_id,
                                                 local_application_key)
        log.log_info("Authorized.")

    def init_auth(self):
        if None == self.credentials:
            self.authorize()

    def check_for_upload_parts(creds, bucket_name, file_name):
        bucket_id = get_bucket_id_from_name(creds, bucket_name)

        unfinished_uploads = util.api.list_all_unfinished_large_files(creds,
                                                                      bucket_id)
        file_id = None
        for file in unfinished_uploads.unfinished_files:
            if file.file_name == file_name:
                file_id = file.file_id
                break

        if None == file_id:
            return UnfinishedUpload(None, None, dict())

        upload_parts = util.api.list_all_parts(creds, file_id).upload_parts
        return UnfinishedUpload(file_id, file_name, upload_parts)

    def get_bucket_id_from_name(creds, bucket_name):
        buckets = api.api.Api.list_buckets(creds, bucket_name)
        if bucket_name in buckets:
            return buckets[bucket_name]

        return None

    def get_key_from_file(self, key_file_path = None):
        if None == key_file_path:
            key_file_path = pathlib.Path.home() / ".bbb2.json"

        key_file = None
        try:
            key_file = open(file=str(key_file_path), mode='r', encoding='utf-8')
            key_file_contents = json.load(key_file)
            return AppKey(key_file_contents["keyId"],
                          key_file_contents["applicationKey"])
        except OSError as e:
            msg = "Failed to open key file." \
                  + " KeyFilePath=\"" + str(key_file_path) + "\"."
            raise Bbb2Error.InternalError(msg) from e
        except json.JSONDecodeError as e:
            msg = "Failed to parse key file." \
                  + " KeyFilePath=\"" + str(key_file_path) + "\"."
            raise Bbb2Error.InternalError(msg) from e
        except KeyError as e:
            msg = "Failed to find fields in key file." \
                  + " KeyFilePath=\"" + str(key_file_path) + "\"."
            raise Bbb2Error.InternalError(msg) from e
        finally:
            if None != key_file:
                key_file.close()

    def get_file_info(creds, bucket_name, file_name):
        bucket_id = get_bucket_id_from_name(creds, bucket_name)
        bucket_files = api.api.Api.list_file_names(creds, bucket_id)
        if file_name in bucket_files:
            return bucket_files[file_name]
        else:
            return None

    class SkipAlreadyUploadedResults:
        cur_part_num = 1
        bytes_already_uploaded = 0

        def __init__(self, cur_part_num, bytes_already_uploaded):
            self.cur_part_num = cur_part_num
            self.bytes_already_uploaded = bytes_already_uploaded

    def skip_already_uploaded(file_stream, uploaded_parts):
        bytes_already_uploaded = 0
        cur_part_num = 1
        while cur_part_num in uploaded_parts.uploaded_parts:
            cur_part = uploaded_parts.uploaded_parts[cur_part_num]

            bytes_already_uploaded += cur_part.content_len
            cur_part_num += 1

        file_stream.seek(bytes_already_uploaded)
        return SkipAlreadyUploadedResults(cur_part_num, bytes_already_uploaded)

    def upload_file_big(creds, src_file_path, dst_bucket_name, dst_file_name,
                        uploaded_parts):
        uploaded_parts = check_for_upload_parts(creds, dst_bucket_name,
                                                dst_file_name)
        file_id = uploaded_parts.file_id
        if None == file_id:
            dst_bucket_id = get_bucket_id_from_name(creds, dst_bucket_name)
            file_id = api.api.Api.start_large_file(creds, dst_bucket_id,
                                                      dst_file_name)
            uploaded_parts.file_id = file_id
            uploaded_parts.file_name = dst_file_name
            uploaded_parts.uploaded_parts = dict()

        log.log_info("Upload file ID is " + str(file_id))

        src_file = util.util.open_binary_read_file(src_file_path)

        results = skip_already_uploaded(src_file, uploaded_parts)
        part_num = results.cur_part_num
        total_bytes_uploaded = results.bytes_already_uploaded
        log.log_info("Starting from part number " + str(part_num) + ".")

        file_len = util.util.get_file_len_bytes(src_file_path)
        remaining_file_len = file_len - total_bytes_uploaded
        remaining_parts = creds.MAX_UPLOAD_PARTS - part_num + 1

        part_len = creds.recommended_upload_part_bytes
        if (remaining_file_len > (remaining_parts
                                  * creds.recommended_upload_part_bytes)):
            part_len = (remaining_file_len // remaining_parts) + 1

        log.log_info("Part length is " + str(part_len) + ".")

        upload_creds = api.api.Api.get_upload_part_url(creds, file_id)
        upload_url = util.http.Url(None, None, None)
        upload_url.from_string(upload_creds["upload_part_url"])
        upload_auth_token = upload_creds["upload_part_auth_token"]

        # BackblazeB2 documentation says 5 consecutive failures implies something is
        # wrong on their end.
        MAX_CONSECUTIVE_FAILURES = 5

        part = util.util.read_file_chunk(src_file, part_len)
        consecutive_failures = 0
        while len(part) > 0:
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                raise Bbb2Error.RemoteError("Max consecutive failures reached.")

            part_sha1 = util.util.calc_sha1(part)

            result = None
            try:
                result = api.api.Api.upload_part(upload_url,
                                                    upload_auth_token, part_num,
                                                    part)
                consecutive_failures = 0
            except (Bbb2Error.ConnectError, Bbb2Error.ExpiredAuthError,
                    Bbb2Error.RemoteError):
                consecutive_failures += 1

            # Refresh the upload URL outside of "except" block because it has chance
            # to throw another exception. Throwing exception inside of an "except"
            # block crashes the whole program.
            if consecutive_failures > 0:
                log.log_warning("Refreshing upload URL.")
                new_url = api.api.Api.get_upload_part_url(creds, file_id)
                upload_url.from_string(new_url["upload_part_url"])
                upload_auth_token = new_url["upload_part_auth_token"]
                continue

            if part_sha1 != result["sha1_hash"]:
                log.log_warning("SHA1 mismatch. Retrying.")
                continue

            total_bytes_uploaded += len(part)
            part_record = api.api.Api.UploadPart(part_num, len(part),
                                                    part_sha1)

            uploaded_parts.uploaded_parts[part_num] = part_record

            log.log_info("Part uploaded. "
                         + util.gen_fraction_percent_str(total_bytes_uploaded,
                                                         file_len)
                         + ".")
            part_num += 1
            part = util.util.read_file_chunk(src_file, part_len)

        bad_part = verify_uploaded_parts(src_file_path, uploaded_parts)
        if 0 == bad_part:
            part_hashes = []
            for i in range(1, part_num):
                part_hashes.append(uploaded_parts.uploaded_parts[i].sha1)

            api.api.Api.finish_large_file(creds, file_id, part_hashes)
        else:
            log.log_warning("Bad part detected!"
                            + " Recommending to restart the upload from scratch."
                            + " BadPartNum=" + str(bad_part) + ".")

    def upload_file_small(creds, bucket_name, dst_file_name, src_file_path):
        bucket_id = util.client.get_bucket_id_from_name(creds, bucket_name)
        if None == bucket_id:
            raise Bbb2Error.Bbb2Error("Unable to find bucket name"
                                      + " \"" + bucket_name + "\".")

        vals = api.api.Api.get_upload_url(creds.api_url, creds.auth_token,
                                             bucket_id)

        upload_url = util.http.Url(util.http.Protocol.HTTPS, [], [])
        upload_url.from_string(vals["upload_url"])

        upload_auth_token = vals["upload_auth_token"]

        results = api.api.Api.upload_file(upload_url, upload_auth_token,
                                             dst_file_name, src_file_path)
        msg = "File upload complete."
        msg += " SrcFilePath=\"" + str(src_file_path) + "\""
        msg += ", DstFileName=\"" + results["file_name"] + "\""
        msg += ", FileId=\"" + results["file_id"] + "\""
        msg += ", BucketId=\"" + results["bucket_id"] + "\""
        msg += ", FileHashSha1=\"" + results["hash_sha1"] + "\"."
        print(msg)

    # Returns zero if all uploaded part checksums match and if the whole file is
    # covered by the parts. Else, returns the earliest part number which failed
    # verification. If there is a file length mismatch, assume the very first part
    # is invalid. A file length mismatch is nigh impossible however due to the fact
    # that the checksums would probably fail to match first.
    def verify_uploaded_parts(file_path, uploaded_parts):
        exception_cur_part_num = 0

        file_stream = util.util.open_binary_read_file(file_path)
        try:
            bytes_uploaded = 0
            for cur_part_num in range(1, len(uploaded_parts.uploaded_parts) + 1):
                exception_cur_part_num = cur_part_num

                cur_part = uploaded_parts.uploaded_parts[cur_part_num]

                file_part = util.util.read_file_chunk(file_stream,
                                                      cur_part.content_len)
                file_part_sha1 = util.util.calc_sha1(file_part)

                if ((file_part_sha1 != cur_part.sha1)
                    or (len(file_part) != cur_part.content_len)):
                    return cur_part_num

                log.log_info("Part " + str(cur_part_num) + " verified.")
                bytes_uploaded += cur_part.content_len

            file_len = util.util.get_file_len_bytes(file_path)
            if bytes_uploaded != file_len:
                log.log_warning("File length mismatch in uploaded parts."
                                + " LocalFileLen=" + str(file_len) + "."
                                + " UploadedPartsLen=" + str(bytes_uploaded) + ".")
                return 1

            return 0
        except KeyError:
            msg = ("Part missing from uploaded part range."
                   + " MissingPartNum=" + str(exception_cur_part_num) + ".")
            log.log_warning(msg)
            return exception_cur_part_num
        finally:
            file_stream.close()
