import unittest
from unittest.mock import patch
import traceback

import api.raw
from api.results import AuthorizeResult
import tests.mocks.util.http
from tests.test_errors import BadMockRequestError
import util.http

@patch('util.http.send_request', tests.mocks.util.http.send_request)
class ApiRawTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.creds = AuthorizeResult(None)
        self.creds.auth_token = "someAuthToken"
        self.creds.api_url = util.http.Url(util.http.Protocol.HTTPS,
                                           util.http.Domain(["api000",
                                                             "backblazeb2",
                                                             "com"]),
                                           util.http.Path([]))
        self.creds.download_url = util.http.Url(util.http.Protocol.HTTPS,
                                                util.http.Domain(["f000",
                                                                  "backblazeb2",
                                                                  "com"]),
                                                util.http.Path([]))

    def test_authorize(self):
        try:
            api.raw.authorize("someKeyId", "someAppKey")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_large_file(self):
        try:
            api.raw.cancel_large_file(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_download_file_by_id(self):
        try:
            api.raw.download_file_by_id(self.creds, "someFileId", 0, 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)
    
    def test_finish_large_file(self):
        try:
            api.raw.finish_large_file(self.creds, "someFileId",
                                      ["hash", "hash"])
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_part_url(self):
        try:
            api.raw.get_upload_part_url(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_url(self):
        try:
            api.raw.get_upload_url(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_buckets(self):
        try:
            api.raw.list_buckets(self.creds, "someBucketName")
            api.raw.list_buckets(self.creds)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_file_names(self):
        try:
            api.raw.list_file_names(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_parts(self):
        try:
            api.raw.list_parts(self.creds, "someFileId")
            api.raw.list_parts(self.creds, "someFileId", 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_unfinished_large_files(self):
        try:
            api.raw.list_unfinished_large_files(self.creds, "someBucketId")
            api.raw.list_unfinished_large_files(self.creds, "someBucketId",
                                                "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_start_large_file(self):
        try:
            api.raw.start_large_file(self.creds, "someBucketId", "someFileName")
        except:
            traceback.print_exc()
            self.assertTrue(False)
