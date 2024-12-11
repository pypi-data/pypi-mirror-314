import unittest
import sys
sys.path.append('../anura/direct')
from anura.direct.client import AnuraDirect
from anura.direct.exceptions import AnuraClientException

class TestSDK(unittest.TestCase):

    def test_empty_instance(self):
        direct = AnuraDirect('')
        with self.assertRaises(AnuraClientException):
            direct.get_result('127.0.0.1')

    def test_invalid_instance(self):
        direct = AnuraDirect('abcdefg')
        with self.assertRaises(AnuraClientException):
            direct.get_result('127.0.0.1')

    def test_remove_additional_data(self):
        direct = AnuraDirect('')
        direct.add_additional_data('1', 'my-value')
        direct.remove_additional_data('1')

        assert len(direct.__additional_data) == 0

if __name__ == '__main__':
    unittest.main()