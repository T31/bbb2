import base64
import copy
import hashlib
import http
import json

from api.raw import RawApi
from api.results import ListPartsResult
from api.results import ListUnfinishedLargeFilesResult
import api.util
import Bbb2Error
import log
import util.http
import util.util

class Api(RawApi):
    @staticmethod
    def list_all_parts(creds, file_id):
        all_upload_parts = [RawApi.list_parts(creds, file_id)]

        while ((None != all_upload_parts[-1].next_part)
                and (all_upload_parts[-1].next_part <= creds.MAX_UPLOAD_PARTS)):
            cur_part = RawApi.list_parts(creds, file_id,
                                         all_upload_parts[-1].next_part)
            all_upload_parts.append(cur_part)

        complete_upload = ListPartsResult()
        for part in all_upload_parts:
            for part_num in part.upload_parts:
                complete_upload.upload_parts[part_num] \
                = part.upload_parts[part_num]

        return complete_upload

    @staticmethod
    def list_all_unfinished_large_files(creds, bucket_id):
        all_parts = [RawApi.list_unfinished_large_files(creds, bucket_id)]

        while None != all_parts[-1].next_file:
            next_file_id = all_parts[-1].next_file
            next_part = RawApi.list_unfinished_large_files(creds, bucket_id,
                                                           next_file_id)
            all_parts.append(next_part)

        complete_result = ListUnfinishedLargeFilesResult()
        for part in all_parts:
            for unfinished_file in part.unfinished_files:
                complete_result.unfinished_files.append(unfinished_file)

        return complete_result
