# This code generates lego brick piles for AI training.
# Check https://github.com/AsherBarak/lego-ai-fun for more details.
#
# All rights reserved

import bpy
import random
import mathutils
import os
from datetime import datetime
import queue
import numpy as np

# todo: setup input parameters:
# Parameters that need to change between machines:
SURFACE_IMAGES_DIR = "C:\\Users\\ASUS\\Documents\\lego-ai-fun\\SyntheticDataGeneration\\Blender\\SurfaceImages"
LDRAW_PATH = 'C:\\Users\\ASUS\\Documents\\Ldarw\\ldraw\\'
LDRAW_LIB_PARTS_PATH = LDRAW_PATH+'parts\\'
GENERATED_DATA_ROOT_PATH = '/temp'

# Control parameters
GENERATED_SCENES_COUNT = 100
SCENE_FILE_PREFIX = datetime.now().strftime("%b_%d_%H_%M_")
OBJECTS_IN_SCENE_COUNT_MAX = 150
OBJECTS_IN_SCENE_COUNT_MIN = 100
IMAGE_X_RESOLUTION = 640
IMAGE_Y_RESOLUTION = 640
IMAGE_RENDER_MAX_CYCLES = 50
TRAINING_BRICKS_FILE_NAMES = [
    # '4073',
    # '3023',
    # '3024',
    # '2780',
    # '98138',
    # '3069b',
    # '3004',
    # '54200',
    # '3710',
    # '3005',
    '3020', # flat 2x4
    # '3022',
    # '6558',
    # '15573',
    # '2412b',
    # '3070b',
    # '3021',
    # '3623',
    # '3666',
    '3003', # standard 2x2
    # '3010',
    # '11477',
    '3001', # standard 2x4
    # '85984',
    # '4274',
    # '2431',
    # '2420',
    # '3062b',
    # '15068',
    # '85861',
    # '43093',
     ]
# todo: use individual color frequesncies for different bricks
TRAINING_BRICK_COLORS_RGB = [
    #"""Source: https://rebrickable.com/colors/"""
    [0x05131D, 153931,  'Black'],
    [0xFFFFFF, 97551, ' White'],
    [0xA0A5A9, 83298, 'Ligth Bluish Gray'],
    [0xC91A09, 68715, ' Red'],
    [0x6C6E68, 65121, ' Dark Bluish Gray'],
    [0xF2CD37, 53660, ' Yellow'],
    [0x0055BF, 38925, ' Blue'],
    [0xE4CD9E, 23328, ' Tan'],
    [0x9BA19D, 24848, 'Light Gray'],
    [0x582A12, 24993, ' Redish Brown'],
    [0x237841, 17801, ' Green'],
    [0xFE8A18, 10549, ' Orange'],
]

BRICK_NAME_PREFIX= 'Brick_'
VIEWER_NAME_PREFIX = 'Viewer_'

SURFACE_SCALE = 5
MAX_RANDOM_BRICK_HEIGHT = 8

bricks_colors_weights_sum = 0
for color in TRAINING_BRICK_COLORS_RGB:
    bricks_colors_weights_sum += color[1]

current_scene_index=1
current_scene_bricks=set()
scene_folder_name=''

#################################
# Utils

def hex_to_rgb_old(hex_value):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b, 1

def srgb_to_linearrgb(c):
    if c < 0:
        return 0
    elif c < 0.04045:
        return c/12.92
    else:
        return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h, alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r, g, b)] + [alpha])

def point_camera_to_origin(camera, distance=10.0):
    looking_direction = camera.location - mathutils.Vector((0.0, 0.0, 0.0))
    rot_quat = looking_direction.to_track_quat('Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    camera.location = rot_quat @ mathutils.Vector((0.0, 0.0, distance))

def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax

# Parallel execution ustils:
execution_queue = queue.Queue()

# This function can safely be called in another thread.
# The function will be executed when the timer runs the next time.
def run_in_main_thread(function):
    execution_queue.put(function)

def execute_queued_functions():
    while not execution_queue.empty():
        function = execution_queue.get()
        function()
    return 5.0

bpy.app.timers.register(execute_queued_functions)

##################################
# Main code

# Done once
def set_blender():
    bpy.ops.object.delete()
    set_rendering()
    bpy.data.scenes["Scene"].view_layers["ViewLayer"].use_pass_cryptomatte_object = True
    bpy.context.scene.use_nodes = True
    
def set_rendering():
    scene = bpy.data.scenes["Scene"]
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = IMAGE_RENDER_MAX_CYCLES
    scene.render.resolution_x = IMAGE_X_RESOLUTION
    scene.render.resolution_y = IMAGE_Y_RESOLUTION

def clear_render_tree_and_create_layers_node():
    tree = bpy.context.scene.node_tree
    for every_node in tree.nodes:
        tree.nodes.remove(every_node)
    render_layers_node = tree.nodes.new('CompositorNodeRLayers')
    render_layers_node.location = 0, 0
    comp_node = tree.nodes.new('CompositorNodeComposite')
    comp_node.location = 400, 0
    links = tree.links
    link = links.new(render_layers_node.outputs[0], comp_node.inputs[0])
    # todo: consider adding a noise layer - https://blender.stackexchange.com/questions/84546/adding-random-noise-to-rendered-images
    return render_layers_node
    
def create_materials_dictionary():
    # Set one brick to initialize ldraw library
    bpy.ops.import_scene.importldraw(ldrawPath=LDRAW_PATH,
        filepath=LDRAW_LIB_PARTS_PATH+"3001.dat", addEnvironment=False, positionCamera=False)
    bpy.ops.object.delete()
    materials_dictionary = {}
    for color in TRAINING_BRICK_COLORS_RGB:
        material = bpy.data.materials.new(name='LegoColor_'+color[2])
        material.use_nodes = True
        nodes = material.node_tree.nodes
        for node in nodes:
            material.node_tree.nodes.remove(node)
        concave_walls_group = nodes.new(type='ShaderNodeGroup')
        concave_walls_group.node_tree = bpy.data.node_groups['Concave Walls']
        concave_walls_group.inputs[0].default_value = 0.2
        lego_standard_group = nodes.new(type='ShaderNodeGroup')
        lego_standard_group.location = (400, 0)
        lego_standard_group.node_tree = bpy.data.node_groups['Lego Standard']
        rgb_color = hex_to_rgb(color[0])
        lego_standard_group.inputs[0].default_value = rgb_color
        material.node_tree.links.new(
            concave_walls_group.outputs[0],
            lego_standard_group.inputs[1]
        )
        output_material = nodes.new(type='ShaderNodeOutputMaterial')
        output_material.location = (800, 0)
        material.node_tree.links.new(
            lego_standard_group.outputs[0],
            output_material.inputs[0]
        )
        material.diffuse_color = rgb_color
        materials_dictionary[color[0]] = material
    return materials_dictionary


def create_file_output_node(directorypath, render_layers_node):
    tree = bpy.context.scene.node_tree
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')
    file_output_node.base_path = directorypath
    file_output_node.location = 100, 0
    tree = bpy.context.scene.node_tree
    links = tree.links
    link = links.new(render_layers_node.outputs[0], file_output_node.inputs[0])  
    file_output_node.location=(800,0)  
    return file_output_node

def set_lighting():
    print('Lighting not implemented')
    # todo: consider area lighting to diffuse shadows
    # todo: consider multiple light sources (seem less frequest in pics we have)

def set_camera():
    camera=bpy.data.objects['Camera']
    camera_x=random.randint(0,SURFACE_SCALE*2)-SURFACE_SCALE/2
    camera_y=random.randint(0,SURFACE_SCALE*2)-SURFACE_SCALE/2
    camera_d=random.randint(8,15)
    camera.location=mathutils.Vector((camera_x, camera_y, 10))
    point_camera_to_origin(camera, camera_d)
    
def get_random_surface_image_path():
    return SURFACE_IMAGES_DIR+'\\'+random.choice(os.listdir(SURFACE_IMAGES_DIR)) 

def create_surface():
    surface=bpy.data.objects.get('Plane')
    if (not(surface)):
        bpy.ops.mesh.primitive_plane_add()
    surface = bpy.data.objects['Plane']
    bpy.context.view_layer.objects.active = surface
    surface.scale = [SURFACE_SCALE*2, SURFACE_SCALE*2, 1]
    bpy.ops.rigidbody.object_add(type='PASSIVE')

    material = bpy.data.materials.new(name='SurfaceMaterial')
    material.use_nodes = True
    nodes = material.node_tree.nodes
    # Surface material
    for node in nodes:
        material.node_tree.nodes.remove(node)
    image_node = nodes.new(type='ShaderNodeTexImage')
    texture_image_path=get_random_surface_image_path()
    image_node.image = bpy.data.images.load(texture_image_path)
    principled_BSDF_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_BSDF_node.location = (400, 0)
    material.node_tree.links.new(
        image_node.outputs[0],
        principled_BSDF_node.inputs[0]
    )
    output_material = nodes.new(type='ShaderNodeOutputMaterial')
    output_material.location = (800, 0)
    material.node_tree.links.new(
        principled_BSDF_node.outputs[0],
        output_material.inputs[0]
    )
    if surface.data.materials:
        surface.data.materials[0] = material
    else:
        surface.data.materials.append(material)
    # todo: add fabric on the surface?

def delete_existing_bricks():
    meshes=set()
    for brick in current_scene_bricks:
        meshes.add(brick.data)
        bpy.data.objects.remove(brick)
    current_scene_bricks.clear()
    for mesh in meshes:
        bpy.data.meshes.remove(mesh)

def pick_random_brick_color_hex():
    pick = random.randint(0, bricks_colors_weights_sum)
    sum_count = 0
    for color in TRAINING_BRICK_COLORS_RGB:
        sum_count += color[1]
        if pick < sum_count:
            return color[0]

def animation_callback(scene):
    if scene.frame_current == 70:
        bpy.ops.screen.animation_cancel(restore_frame=False)
        bpy.app.handlers.frame_change_pre.remove(animation_callback)
        run_in_main_thread(bpy.ops.render.render)

def render_complete_callback(a, b):
    run_in_main_thread(after_render_complete) 

def after_render_complete():
    global current_scene_index
    current_scene_index = current_scene_index + 1
    # Disabled because cv2 dependency is not available in blender. We use another process to convert maps to box data
    #write_render_data()
    if (current_scene_index<(GENERATED_SCENES_COUNT+1)):
        generate_and_render_scene(current_scene_index)

def write_render_data():
    # Collect render data
    f = open(GENERATED_DATA_ROOT_PATH+'\\'+scene_folder_name+"\\demofile2.txt", "a")
    for brick in current_scene_bricks:
        viewer_name=VIEWER_NAME_PREFIX +brick.name
        viewer_node=bpy.context.scene.node_tree.nodes[viewer_name]
        #viewer_node =bpy.data.images[viewer_name]
        viewer_node.select=True
        # get viewer pixels
        pixels = bpy.data.images['Viewer Node'].pixels
        f.writelines(brick.name+' '+str(len(pixels))+'\n') # size is always width * height * 4 (rgba)
        # copy buffer to numpy array for faster manipulation
        arr = np.array(pixels[:]).reshape((IMAGE_X_RESOLUTION,IMAGE_Y_RESOLUTION,4))
        f.writelines(str(bbox2(arr))+'\n')
    f.close()

def generate_and_render_scene(i_scene):
    create_surface()
    set_lighting()
    set_camera()
    delete_existing_bricks()
    render_layers_node = clear_render_tree_and_create_layers_node()
    file_output_node = create_file_output_node(GENERATED_DATA_ROOT_PATH, render_layers_node)
    global scene_folder_name
    scene_folder_name = SCENE_FILE_PREFIX+str(i_scene)
    file_output_node.base_path += '/'+scene_folder_name
    #file_output_node.file_slots.remove(file_output_node.inputs[0])
    bricks_count = random.randint(
        OBJECTS_IN_SCENE_COUNT_MIN, OBJECTS_IN_SCENE_COUNT_MAX)
    for i_brick in range(0, bricks_count):
        # Create
        brick_code = random.sample(TRAINING_BRICKS_FILE_NAMES, k=1)[0]
        brick_id = brick_code+'_'+str(i_brick)
        bpy.ops.import_scene.importldraw(ldrawPath=LDRAW_PATH,
            filepath=LDRAW_LIB_PARTS_PATH+brick_code+".dat", addEnvironment=False, positionCamera=False)
        brick = bpy.context.selected_objects[0]
        current_scene_bricks.add(brick)
        brick.name = BRICK_NAME_PREFIX+brick_id
        # Material and Color
        brick.material_slots[0].link = 'OBJECT'
        color = pick_random_brick_color_hex()
        brick.material_slots[0].material = MATERIALS_DICTIONARY[color]
        # Location
        surface_half = SURFACE_SCALE/2
        brick.location = [
            random.uniform(-surface_half, surface_half),
            random.uniform(-surface_half, surface_half),
            random.uniform(0, MAX_RANDOM_BRICK_HEIGHT)]
        brick.rotation_euler = [random.uniform(
            0, 6.28), random.uniform(0, 6.28), random.uniform(0, 6.28)]
        # Animation
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        # Mask file
        # this will need to change if we would like to have multiple angles on the same scene (we do not expect the scene setupe to be a big cost so maybe not)
        brick_mask_file_name = SCENE_FILE_PREFIX+str(i_scene)+'_'+brick_id+'_'
        tree = bpy.context.scene.node_tree
        #id_mask_node = tree.nodes.new('CompositorNodeIDMask')
        cryptomatte_node = tree.nodes.new('CompositorNodeCryptomatteV2')
        cryptomatte_node.matte_id = brick.name
        cryptomatte_node.location=[400, -50*(i_brick+4)]
        cryptomatte_node.hide=True
        file_output_node.file_slots.new(brick_mask_file_name)
        tree.links.new(
            cryptomatte_node.outputs['Matte'],
            file_output_node.inputs[brick_mask_file_name]
        )
        # We can't read the masks because we don't have cv2 so we don't need to generate the viewer nodes
        #create_viewer_node(i_brick, brick, tree, cryptomatte_node)
    # todo: add non lego bricks objects to increase picture fidelity
    bpy.context.scene.frame_set(0)
    bpy.app.handlers.frame_change_pre.append(animation_callback)
    bpy.ops.screen.animation_play()

def create_viewer_node(i_brick, brick, tree, cryptomatte_node):
    viewer_node = tree.nodes.new('CompositorNodeViewer')
    viewer_node.name=VIEWER_NAME_PREFIX+brick.name
    viewer_node.location=[800, -50*(i_brick+10)]
    tree.links.new(
            cryptomatte_node.outputs['Matte'],
            viewer_node.inputs[0]
        )
    # rendering is timed after animation completion in animation callback

############################
# startup code:
set_blender()
MATERIALS_DICTIONARY = create_materials_dictionary()
bpy.app.handlers.render_post.append(render_complete_callback)

generate_and_render_scene(current_scene_index)
