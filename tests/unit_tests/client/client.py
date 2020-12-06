import unittest
from unittest.mock import patch
import traceback

from client.client import Client
import tests.mocks.util.http
import tests.mocks.client.util

@patch('util.http.send_request', tests.mocks.util.http.send_request)
class ClientTests(unittest.TestCase):
    @patch('client.util.get_key_from_file',
           tests.mocks.client.util.get_key_from_file)
    def test_authorize(self):
        try:
            Client().authorize()
        except:
            traceback.print_exc()
            self.assertTrue(False)
