# Initialisation

from . import utils
from . import optics
from . import interface
from . import config
from . import blender
import bpy
bl_info = {
    "name": "Plenoptic_Simulation",
    "author": "Tim Michels, Tom Allen",
    "description": "Simulates a plenoptic camera",
    "blender": (2, 80, 2),
    "version": (1, 0, 0),
    "location": "View 3D",
    "warning": "",
    "category": "Camera"
}

# Imports


classes = (interface.Test_PT_Panel, optics.AddCameraOperation)

register, unregister = bpy.utils.register_classes_factory(classes)
