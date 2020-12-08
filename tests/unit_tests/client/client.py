import unittest
from unittest.mock import patch
import traceback

from client.client import Client
import tests.mocks.util.http
import tests.mocks.client.internal

@patch('util.http.send_request', tests.mocks.util.http.send_request)
@patch('client.internal.Internal.get_key_from_file',
       tests.mocks.client.internal.Internal.get_key_from_file)
class ClientTests(unittest.TestCase):
    def test_authorize(self):
        try:
            Client().authorize()
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_all_large_files(self):
        try:
            Client().cancel_all_large_files()
        except:
            traceback.print_exc()
            self.assertTrue(False)

    def test_cancel_large_file(self):
        try:
            Client().cancel_large_file("someFileId")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    @unittest.SkipTest
    def test_download_file(self):
        pass

    def test_list_buckets(self):
        try:
            Client().list_buckets()
            Client().list_buckets("someBucketName")
        except:
            traceback.print_exc()
            self.assertTrue(False)

    @unittest.SkipTest
    def test_upload_file(self):
        pass
