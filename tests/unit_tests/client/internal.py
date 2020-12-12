import unittest
from unittest.mock import patch
import traceback

import tests.mocks.util.http
from client.internal import Internal

@patch('util.http.send_request', tests.mocks.util.http.send_request)
class ClientInternalTests(unittest.TestCase):
    @patch('client.internal.Internal.get_key_from_file',
           tests.mocks.client.internal.Internal.get_key_from_file)
    def test_authorize(self):
        try:
            Internal().authorize(None)
        except:
            traceback.print_exc()
            self.assertTrue(False)

    @unittest.SkipTest
    def test_init_auth(self):
        pass

    @unittest.SkipTest
    def test_check_for_upload_parts(self):
        pass

    @unittest.SkipTest
    def test_get_bucket_id_from_name(self):
        pass

    @unittest.SkipTest
    def test_get_key_from_file(self):
        pass

    @unittest.SkipTest
    def test_get_file_info(self):
        pass

    @unittest.SkipTest
    def test_skip_already_downloaded(self):
        pass

    @unittest.SkipTest
    def test_upload_file_big(self):
        pass

    @unittest.SkipTest
    def test_upload_file_small(self):
        pass

    @unittest.SkipTest
    def test_verify_uploaded_parts(self):
        pass
