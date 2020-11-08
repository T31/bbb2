import unittest
from unittest.mock import patch

import api.raw
import util.http
import tests.mocks.util.http

class AuthorizeTests(unittest.TestCase):
    @patch('util.http.send_request', tests.mocks.util.http.send_request)
    def test_auth(self):
        api.raw.authorize("fuck", "me")
        self.assertTrue(True)

if "__main__" == __name__:
    unittest.main()
