import unittest
from unittest.mock import patch
import traceback

from api.api import Api
from api.results import AuthorizeResult
import tests.mocks.util.http
import tests.mocks.util.util
import util.http

@patch('util.http.send_request', tests.mocks.util.http.send_request)
@patch('util.util.calc_sha1_file', tests.mocks.util.util.calc_sha1_file)
@patch('util.util.get_entire_file', tests.mocks.util.util.get_entire_file)
@patch('util.util.get_file_len_bytes', tests.mocks.util.util.get_file_len_bytes)
class ApiApiInheritedTests(unittest.TestCase):
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

        self.upload_url = util.http.Url.from_string("https://up.backblaze.com")

    def test_authorize(self):
        try:
            Api.authorize("someKeyId", "someAppKey")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_large_file(self):
        try:
            Api.cancel_large_file(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_download_file_by_id(self):
        try:
            Api.download_file_by_id(self.creds, "someFileId", 0, 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)
    
    def test_finish_large_file(self):
        try:
            Api.finish_large_file(self.creds, "someFileId",
                                      ["hash", "hash"])
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_part_url(self):
        try:
            Api.get_upload_part_url(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_url(self):
        try:
            Api.get_upload_url(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_buckets(self):
        try:
            Api.list_buckets(self.creds, "someBucketName")
            Api.list_buckets(self.creds)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_file_names(self):
        try:
            Api.list_file_names(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_parts(self):
        try:
            Api.list_parts(self.creds, "someFileId")
            Api.list_parts(self.creds, "someFileId", 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_unfinished_large_files(self):
        try:
            Api.list_unfinished_large_files(self.creds, "someBucketId")
            Api.list_unfinished_large_files(self.creds, "someBucketId",
                                                "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_start_large_file(self):
        try:
            Api.start_large_file(self.creds, "someBucketId", "someFileName")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_upload_file(self):
        try:
            Api.upload_file(self.upload_url, "someUploadAuthToken",
                                "someDstFileName", "someSrcFile")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_upload_part(self):
        try:
            Api.upload_part(self.upload_url, "someAuthToken", 20,
                                bytes([5, 5,]))
        except:
            traceback.print_exc()
            self.assertTrue(False)

class ApiApiTests(unittest.TestCase):
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

        self.creds.MAX_UPLOAD_PARTS = 10000

    @patch('util.http.send_request',
           tests.mocks.util.http.send_request_list_all_upload_parts)
    def test_list_all_parts(self):
        try:
            Api.list_all_parts(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    @patch('util.http.send_request',
           tests.mocks.util.http.send_request_list_all_unfinished_large_files)
    def test_list_all_unfinished_large_files(self):
        try:
            Api.list_all_unfinished_large_files(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)
