import bpy

class Test_PT_Panel(bpy.types.Panel):
    bl_idname = "CAMGEN_PT_Main"
    bl_label = "Camera Generator"
    bl_category = "Camera Generator Addon"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('operators.addcamera', text="Add Camera")