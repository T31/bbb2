import unittest
from unittest.mock import patch
import traceback

from api.raw import RawApi
from api.results import AuthorizeAccountResult
import tests.mocks.util.http
import tests.mocks.util.util
from tests.test_errors import BadMockRequestError
import util.http

@patch('util.http.send_request', tests.mocks.util.http.send_request)
@patch('util.util.calc_sha1_file', tests.mocks.util.util.calc_sha1_file)
@patch('util.util.get_entire_file', tests.mocks.util.util.get_entire_file)
@patch('util.util.get_file_len_bytes', tests.mocks.util.util.get_file_len_bytes)
class ApiRawTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.creds = AuthorizeAccountResult(None)
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

    def test_authorize_account(self):
        try:
            RawApi.authorize_account("someKeyId", "someAppKey")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_large_file(self):
        try:
            RawApi.cancel_large_file(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_download_file_by_id(self):
        try:
            RawApi.download_file_by_id(self.creds, "someFileId", 0, 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)
    
    def test_finish_large_file(self):
        try:
            RawApi.finish_large_file(self.creds, "someFileId",
                                      ["hash", "hash"])
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_part_url(self):
        try:
            RawApi.get_upload_part_url(self.creds, "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_get_upload_url(self):
        try:
            RawApi.get_upload_url(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_buckets(self):
        try:
            RawApi.list_buckets(self.creds, "someBucketName")
            RawApi.list_buckets(self.creds)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_file_names(self):
        try:
            RawApi.list_file_names(self.creds, "someBucketId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_parts(self):
        try:
            RawApi.list_parts(self.creds, "someFileId")
            RawApi.list_parts(self.creds, "someFileId", 3)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_list_unfinished_large_files(self):
        try:
            RawApi.list_unfinished_large_files(self.creds, "someBucketId")
            RawApi.list_unfinished_large_files(self.creds, "someBucketId",
                                                "someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_start_large_file(self):
        try:
            RawApi.start_large_file(self.creds, "someBucketId", "someFileName")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_upload_file(self):
        try:
            RawApi.upload_file(self.upload_url, "someUploadAuthToken",
                                "someDstFileName", "someSrcFile")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_upload_part(self):
        try:
            RawApi.upload_part(self.upload_url, "someAuthToken", 20,
                                bytes([5, 5,]))
        except:
            traceback.print_exc()
            self.assertTrue(False)
