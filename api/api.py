import base64
import copy
import hashlib
import http
import json

from api.raw import RawApi
from api.results import ListPartsResult
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
        list_of_lists = [BackblazeB2Api.list_unfinished_large_files(creds,
                                                                    bucket_id)]

        while None != list_of_lists[-1].next_file:
            next_file_id = list_of_lists[-1].next_file
            new_list = BackblazeB2Api.list_unfinished_large_files(creds,
                                                                  bucket_id,
                                                                  next_file_id)
            list_of_lists.append(new_list)

        complete_list = []
        for inner_list in list_of_lists:
            for unfinished_large_file in inner_list.unfinished_files:
                complete_list.append(unfinished_large_file)

        return BackblazeB2Api.ListUnfinishedLargeFilesResult(complete_list,
                                                             None)
