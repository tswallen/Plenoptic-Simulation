import bpy
import config
import blender
import unittest

import sys
sys.path.append('../src/plenoptic_simulation')


class TestBlender(unittest.TestCase):
    def test_initialise_cycles(self):
        scene = bpy.data.scenes[0]
        blender.initialise_cycles(scene, config.cycles_config)
        for setting in config.cycles_config:
            self.assertEquals(
                scene.cycles[setting], config.cycles_config[setting])

    def test_import_collection(self):
        file = 'C:\\Temp\\Plenoptic-Simulation\\src\\plenoptic_simulation\\resources.blend'
        blender.import_collection(file)
