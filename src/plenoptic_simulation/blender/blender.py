import bpy


def initialise_cycles(scene: bpy.types.Scene, settings: bpy.types.PropertyGroup):
    '''Applies Cycles settings'''
    for setting in settings:
        scene.cycles[setting] = settings[setting]


def import_collection(path: str):
    '''Imports stuff from resources.blend'''
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection

    for filename in ['Camera Collection', 'Glass Material', 'MLA Hex Material']:
        bpy.ops.wm.append(filename=filename,
                          directory=f'{path}/{filename.split()[-1]}')

    for materials in ['Glass Material', 'MLA Hex Material', 'MLA Rect Material']:
        bpy.data.materials[materials].use_fake_user = True

    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
        'Camera Collection']
