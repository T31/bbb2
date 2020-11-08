import unittest
from unittest.mock import patch
import traceback

import api.raw
import util.http
import tests.mocks.util.http
from tests.test_errors import BadMockRequestError

class AuthorizeTests(unittest.TestCase):
    @patch('util.http.send_request', tests.mocks.util.http.send_request)
    def test_auth(self):
        try:
            result = api.raw.authorize("someKeyId", "someAppKey")
            self.assertTrue(True)
        except:
            traceback.print_exc()
            self.assertTrue(False)

if "__main__" == __name__:
    unittest.main()
