""" testen voor de package waterstand """
import urllib.request

import unittest
from unittest.mock import patch, MagicMock

import waterstand

class TestUrlopen(unittest.TestCase):

  @patch('urllib.request.urlopen')
  def test_haalwaterstand(self, mock_urlopen):
    f = open('tests/testdata.json', 'r')
    testdata = f.read()

    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = testdata.encode('utf-8')
    mock_response.__enter__.return_value = mock_response

    mock_urlopen.return_value = mock_response

    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    self.assertEqual(response, {'tijd': '24-11 16:50', 'nu': 101.0, 'morgen': 101.0})
