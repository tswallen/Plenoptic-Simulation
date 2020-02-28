import bpy
import optics
import unittest

import sys
sys.path.append('../src/plenoptic_simulation')


class TestOptics(unittest.TestCase):
    def test_open_lens_file(self):
        file = 'C:\\Temp\\Plenoptic-Simulation\\src\\plenoptic_simulation\\optics\\D-Gauss F1.4 45deg_Mandler USP2975673 p351.json'
        self.assertEqual(optics.open_lens_file(file)[0]['radius'], 0.08824)

    def test_add_circle(self):
        circle = {
            'defaults': {
                'vertices': 64,
                'radius': 32,
                'fill_type': 'TRIFAN',
                'calc_uvs': False,
                'location': (0, 0, 0)
            },
            'name': 'Test'
        }
        self.assertIsInstance(optics.add_circle(circle), bpy.types.Object)
        self.assertEqual(getattr(optics.add_circle(circle), 'name'), 'Test')
