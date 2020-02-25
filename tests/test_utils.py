import unittest

import sys
sys.path.append('../src/plenoptic_simulation')

import utils

class TestUtils(unittest.TestCase):
    def test_str_to_float(self):
        self.assertEqual(utils.str_to_float('1'), 1.0)
        self.assertEqual(utils.str_to_float(' 1 '), 1.0)
        self.assertEqual(utils.str_to_float('-1'), -1.0)
        self.assertEqual(utils.str_to_float(''), 0.0)
        self.assertRaises(ValueError, utils.str_to_float, 'abc')
