import base64
import copy
import hashlib
import http
import json

from api.raw import RawApi
import api.util
import Bbb2Error
import util.http
import util.util

class Api(RawApi):
    @staticmethod
    def list_all_parts(creds, file_id):
        result_list = [BackblazeB2Api.list_parts(creds, file_id)]

        while ((None != result_list[-1].next_part)
                and (result_list[-1].next_part <= creds.MAX_UPLOAD_PARTS)):
            result = BackblazeB2Api.list_parts(creds, file_id,
                                               result_list[-1].next_part)
            result_list.append(result)

        all_upload_parts = dict()
        for result in result_list:
            for part_num in result.upload_parts:
                all_upload_parts[part_num] = result.upload_parts[part_num]

        return BackblazeB2Api.ListPartsResult(all_upload_parts, None)

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
