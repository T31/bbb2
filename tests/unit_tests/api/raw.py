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
            self.assertTrue(True)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_large_file(self):
        try:
            api.raw.cancel_large_file(self.creds, "someFileId")
            self.assertTrue(True)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_download_file_by_id(self):
        try:
            api.raw.download_file_by_id(self.creds, "someFileId", 0, 3)
            self.assertTrue(True)
        except:
            traceback.print_exc()
            self.assertTrue(False)
    
    def test_finish_large_file(self):
        try:
            api.raw.finish_large_file(self.creds, "someFileId",
                                      ["hash", "hash"])
            self.assertTrue(True)
        except:
            traceback.print_exc()
            self.assertTrue(False)
