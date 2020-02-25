import unittest

import sys
sys.path.append('../src/plenoptic_simulation')

import optics

class TestOptics(unittest.TestCase):
    def test_open_lens_file(self):
        file = 'C:\\Temp\\Plenoptic-Simulation\\src\\plenoptic_simulation\\optics\\D-Gauss F1.4 45deg_Mandler USP2975673 p351.json'
        self.assertTrue(optics.open_lens_file(file))
        self.assertIsInstance(optics.open_lens_file(file), list)
        self.assertEqual(optics.open_lens_file(file)[0]['radius'], 0.08824)
    def test_create_lenses(self):
        self.assertTrue(optics.create_lenses())
