import json
import bpy
import math

from .. import blender, config


def open_lens_file(path: str) -> [dict]:
    '''Opens a JSON file and returns its contents'''
    with open(path) as file:
        return json.load(file)


def add_circle(config: dict):
    '''Adds a circle'''
    bpy.ops.mesh.primitive_circle_add(**config['defaults'])
    circle = bpy.context.active_object
    for setting, value in config.items():
        if setting is 'defaults':
            continue
        setattr(circle, setting, value)
    return circle


def calculate_sagitta(half_lens_height, surface_radius):
    if half_lens_height > surface_radius:
        return surface_radius
    return surface_radius - math.sqrt(surface_radius * surface_radius - half_lens_height * half_lens_height)


def calculate_number_of_vertices(half_lens_height, surface_radius, vertex_count_height):
    return int(vertex_count_height / (math.asin(half_lens_height / surface_radius) / math.pi) + 0.5) * 2


def create_flat_surface(half_lens_height: float, ior: float, position: float, name: str):
    '''Creates a flat surface as part of the lens stack'''
    circle = add_circle({
        'defaults': {
            'vertices': 64,
            'radius': half_lens_height,
            'fill_type': 'TRIFAN',
            'calc_uvs': False,
            'location': (position, 0, 0),
            'rotation': (0, -math.pi / 2, 0)
        },
        'name': name,
        'parent': bpy.data.objects['Objective']
    })

    # TODO: Refactor
    glass_material = bpy.data.materials['Glass Material'].copy()
    glass_material.name = f'Glass Material {name}'
    glass_material.node_tree.nodes['IOR'].outputs['Value'].default_value = ior

    glass_material.node_tree.links.remove(
        glass_material.node_tree.nodes['Vector Transform.002'].outputs[0].links[0])
    circle.data.materials.append(glass_material)

    bpy.ops.object.mode_set(mode="OBJECT")
    outer_vertex = circle.data.vertices[0]
    for vertex in circle.data.vertices:
        if vertex.co.z > outer_vertex.co.z:
            outer_vertex = vertex

    return [outer_vertex.co.x, outer_vertex.co.y, outer_vertex.co.z]


def create_lens_surface(vertex_count_height, vertex_count_radial, surface_radius, half_lens_height, ior, position, name):
    flip = False
    if surface_radius < 0.0:
        flip = True
        surface_radius = -1.0 * surface_radius

    # create circle
    circle = add_circle({
        'defaults': {
            'vertices': calculate_number_of_vertices(half_lens_height, surface_radius, vertex_count_height),
            'radius': surface_radius,
            'location': (0, 0, 0)
        }
    })

    # ================================================MAGIC
    bpy.ops.object.transform_apply()
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode="OBJECT")
    circle.data.vertices[0].co.x = 0.0
    # select all vertices that should be deleted
    for vertex in circle.data.vertices:
        if (vertex.co.y < surface_radius - calculate_sagitta(half_lens_height, surface_radius)) or (vertex.co.x > 0.0):
            vertex.select = True
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.delete(type='VERT')
    # select all remaining vertices to create a rotational surface
    bpy.ops.mesh.select_all(action='SELECT')
    # use the spin operator to create the rotational surface
    bpy.ops.mesh.spin(steps=vertex_count_radial,
                      angle=2.0*math.pi, axis=(0, 1, 0))
    # remove double vertices resulting from the spinning
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0)
    # flip normals for a convex surface
    if not flip:
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode="OBJECT")
    # move to correct position
    circle.rotation_euler[0] = math.pi/2.0
    if flip:
        circle.rotation_euler[1] = math.pi/2.0
    else:
        circle.rotation_euler[1] = -math.pi/2.0
    bpy.ops.object.transform_apply()
    circle.location[0] = position
    # rename object and move it to 'Objective' empty
    circle.name = name
    circle.parent = bpy.data.objects['Objective']
    # add glass material
    glass_material = bpy.data.materials['Glass Material'].copy()
    glass_material.name = "Glass Material "+name
    glass_material.node_tree.nodes['IOR'].outputs['Value'].default_value = ior
    circle.data.materials.append(glass_material)
    # return the outer vertex for housing creation
    bpy.ops.object.mode_set(mode="OBJECT")
    outer_vertex = circle.data.vertices[0]
    for vertex in circle.data.vertices:
        if vertex.co.z > outer_vertex.co.z:
            outer_vertex = vertex

    # ================================================END MAGIC
    return [outer_vertex.co.x, outer_vertex.co.y, outer_vertex.co.z]


def create_lenses(vertex_count_height: int, vertex_count_radial: int, lenses: [dict]):
    '''Creates the lens stack'''
    outer_vertices, outer_lens_index = [], list(range(len(lenses)))

    for index, lens in enumerate(lenses):
        if lens['material'] == "air" and lenses[index - 1]['material'] == "air":
            outer_lens_index.remove(index)
            continue
        if lens['radius'] == 0.0:
            outer_vertices.append(create_flat_surface(
                lens['semi_aperture'], lens['ior_ratio'], lens['position'], lens['name']))
            continue
        create_lens_surface(vertex_count_height, vertex_count_radial,
                            lens['radius'], lens['semi_aperture'], lens['ior_ratio'], lens['position'], lens['name'])
    return outer_vertices, outer_lens_index


class AddCameraOperation(bpy.types.Operator):
    bl_idname = "operators.addcamera"
    bl_label = "Test"
    bl_description = "Runs test"

    def execute(self, context):
        addon_directory = bpy.utils.user_resource('SCRIPTS', "addons")
        lens = open_lens_file(
            f'{addon_directory}/plenoptic_simulation/optics/D-Gauss F1.4 45deg_Mandler USP2975673 p351.json')

        blender.initialise_cycles(bpy.data.scenes[0], config.cycles_config)
        blender.import_collection(
            f'{addon_directory}/plenoptic_simulation/blender/resources.blend')

        create_lenses(36, 32, lens)

        return {'FINISHED'}
