# This code generates lego brick piles for AI training.
# Check https://github.com/AsherBarak/lego-ai-fun for more details.
#
# All rights reserved
 



 # design + color = element
from sys import path
import bpy
import random
import mathutils
import os
from pathlib import Path
from datetime import datetime
import queue
import numpy as np
import json
 
# todo: setup input parameters:
# Parameters that need to change between machines:
SURFACE_IMAGES_DIR = "C:\\Workspace\\Private\\lego-ai-fun-main\\SyntheticDataGeneration\\Blender\\SurfaceImages"
LDRAW_PATH = 'C:\\Workspace\\Private\\Ldraw\\parts\\ldraw\\'
LDRAW_LIB_PARTS_PATH = LDRAW_PATH+'parts\\'
GENERATED_DATA_ROOT_PATH = 'C:\\Workspace\\Private\\Ldraw\\Generations'
 
# Control parameters
GENERATED_SCENES_COUNT = 1
BATCH_FOLDER_NAME = datetime.now().strftime("%b_%d_%H_%M")
BATCH_FILE_PREFIX = BATCH_FOLDER_NAME+"_"
OBJECTS_IN_SCENE_COUNT_MAX = 10
OBJECTS_IN_SCENE_COUNT_MIN = 2
IMAGE_X_RESOLUTION = 640
IMAGE_Y_RESOLUTION = 640
IMAGE_RENDER_MAX_CYCLES = 50
 

 #todo - change the dictonary!!!
 ELEMENT_DESIGN_ID_DICT{
    'part_num': [element_id,color_id]
    '67906c01': [6300211,14]
    '2564': [4566309,0]
    '53657': [4275423,1004]
    '92926': [6194308,71]
    '26561': [6229123,4]
    '51035': [4241969,1004]
    '50899pat0001': [4257250,-1]
 }




 
LONDON_21034 = [
['90398',1],
['85861',3],
['15712',36],
['4070',6],
['6541',4],
['3070b',3],
['15070',2],
['32016',2],
['61252',4],
['18674',3],
['11211',4],
['2412b',6],
['15573',4],
['11458',4],
['3023',9],
['61409',2],
['15397',1],
['30374',3],
['26603',4],
# ['x136',2],
['4477',2],
['6231',2],
['3024',4],
['3070b',4],
['15070',8],
['49668',8],
['30136',20],
['2877',8],
['15573',4],
['3023',4],
['15208',4],
['3022',8],
# ['3003pb091',1],
['3623',2],
['4490',4],
['3021',4],
['3020',3],
['4274',1],
['2780',4],
['3069b',3],
['3023',12],
['3022',1],
['99206',1],
['3021',3],
['2431',3],
['3710',5],
['6636',3],
['3795',2],
['87609',6],
# ['4162pb167',1],
['3460',4],
['3035',1],
['2445',4],
['3023',23],
['3065',2],
['3069b',40],
['98138',4],
['23443',4],
['3070b',4],
['15573',2],
['3069b',4],
['32580',4],
['48729b',4],
['25269',4],
['3070b',7],
['3673',4],
['3069b',9],
['15573',6],
['3023',7],
['18677',4],
['99207',4],
['99781',4],
['87994',1],
['87580',2],
['3022',8],
['2420',1],
['30165',4],
['64727',1],
['2431',4],
['3020',4],
['3795',3],
# ['4589b',1],
['86208',4],
['15571',1],
['3044c',1],
['3049c',1],
['15573',8],
['99780',4],
['3022',2],
['3688',3],
['60478',4],
['2431',4],
['30350c',2],
['4073',5],
['15395',1],
['98138',3],
#['75c24',4],
]


# todo: use individual color frequesncies for different bricks
TRAINING_BRICK_COLORS_RGB = [
    #"""Source: https://rebrickable.com/colors/"""
    [0xC0C0C0, 153931,  'Black'],
    [0x606060, 97551, ' White'],
    [0xE0E0E0, 83298, 'Ligth Bluish Gray'],
    [0x330019, 68715, ' Red'],
    [0x6C6E68, 65121, ' Dark Bluish Gray'],
    [0xF2CD37, 53660, ' Yellow'],
    [0x0055BF, 38925, ' Blue'],
    [0xE4CD9E, 23328, ' Tan'],
    [0x9BA19D, 24848, 'Light Gray'],
    [0x582A12, 24993, ' Redish Brown'],
    [0x237841, 17801, ' Green'],
    [0xFE8A18, 10549, ' Orange'],
]
 
COLOR_ID_RGB_DICT ={
id:['rgb','name']
-1:['0033B2','[Unknown]']
0:['05131D','Black']
1:['0055BF','Blue']
2:['237841','Green']
3:['008F9B','Dark Turquoise']
4:['C91A09','Red']
5:['C870A0','Dark Pink']
6:['583927','Brown']
7:['9BA19D','Light Gray']
8:['6D6E5C','Dark Gray']
9:['B4D2E3','Light Blue']
10:['4B9F4A','Bright Green']
11:['55A5AF','Light Turquoise']
12:['F2705E','Salmon']
13:['FC97AC','Pink']
14:['F2CD37','Yellow']
15:['FFFFFF','White']
17:['C2DAB8','Light Green']
18:['FBE696','Light Yellow']
19:['E4CD9E','Tan']
20:['C9CAE2','Light Violet']
21:['D4D5C9','Glow In Dark Opaque']
22:['81007B','Purple']
23:['2032B0','Dark Blue-Violet']
25:['FE8A18','Orange']
26:['923978','Magenta']
27:['BBE90B','Lime']
28:['958A73','Dark Tan']
29:['E4ADC8','Bright Pink']
30:['AC78BA','Medium Lavender']
31:['E1D5ED','Lavender']
32:['635F52','Trans-Black IR Lens']
33:['0020A0','Trans-Dark Blue']
34:['84B68D','Trans-Green']
35:['D9E4A7','Trans-Bright Green']
36:['C91A09','Trans-Red']
40:['635F52','Trans-Black']
41:['AEEFEC','Trans-Light Blue']
42:['F8F184','Trans-Neon Green']
43:['C1DFF0','Trans-Very Lt Blue']
45:['DF6695','Trans-Dark Pink']
46:['F5CD2F','Trans-Yellow']
47:['FCFCFC','Trans-Clear']
52:['A5A5CB','Trans-Purple']
54:['DAB000','Trans-Neon Yellow']
57:['FF800D','Trans-Neon Orange']
60:['645A4C','Chrome Antique Brass']
61:['6C96BF','Chrome Blue']
62:['3CB371','Chrome Green']
63:['AA4D8E','Chrome Pink']
64:['1B2A34','Chrome Black']
68:['F3CF9B','Very Light Orange']
69:['CD6298','Light Purple']
70:['582A12','Reddish Brown']
71:['A0A5A9','Light Bluish Gray']
72:['6C6E68','Dark Bluish Gray']
73:['5A93DB','Medium Blue']
74:['73DCA1','Medium Green']
75:['05131D','Speckle Black-Copper']
76:['6C6E68','Speckle DBGray-Silver']
77:['FECCCF','Light Pink']
78:['F6D7B3','Light Nougat']
79:['FFFFFF','Milky White']
80:['A5A9B4','Metallic Silver']
81:['899B5F','Metallic Green']
82:['DBAC34','Metallic Gold']
84:['AA7D55','Medium Nougat']
85:['3F3691','Dark Purple']
86:['7C503A','Medium Brown']
89:['4C61DB','Royal Blue']
92:['D09168','Nougat']
100:['FEBABD','Light Salmon']
110:['4354A3','Violet']
112:['6874CA','Blue-Violet']
114:['DF6695','Glitter Trans-Dark Pink']
115:['C7D23C','Medium Lime']
117:['FFFFFF','Glitter Trans-Clear']
118:['B3D7D1','Aqua']
120:['D9E4A7','Light Lime']
125:['F9BA61','Light Orange']
129:['A5A5CB','Glitter Trans-Purple']
132:['05131D','Speckle Black-Silver']
133:['05131D','Speckle Black-Gold']
134:['AE7A59','Copper']
135:['9CA3A8','Pearl Light Gray']
137:['7988A1','Metal Blue']
142:['DCBC81','Pearl Light Gold']
143:['CFE2F7','Trans-Medium Blue']
148:['575857','Pearl Dark Gray']
150:['ABADAC','Pearl Very Light Gray']
151:['E6E3E0','Very Light Bluish Gray']
158:['DFEEA5','Yellowish Green']
178:['B48455','Flat Dark Gold']
179:['898788','Flat Silver']
182:['F08F1C','Trans-Orange']
183:['F2F3F2','Pearl White']
191:['F8BB3D','Bright Light Orange']
212:['9FC3E9','Bright Light Blue']
216:['B31004','Rust']
226:['FFF03A','Bright Light Yellow']
230:['E4ADC8','Trans-Pink']
232:['7DBFDD','Sky Blue']
236:['96709F','Trans-Light Purple']
272:['0A3463','Dark Blue']
288:['184632','Dark Green']
294:['BDC6AD','Glow In Dark Trans']
297:['AA7F2E','Pearl Gold']
308:['352100','Dark Brown']
313:['3592C3','Maersk Blue']
320:['720E0F','Dark Red']
321:['078BC9','Dark Azure']
322:['36AEBF','Medium Azure']
323:['ADC3C0','Light Aqua']
326:['9B9A5A','Olive Green']
334:['BBA53D','Chrome Gold']
335:['D67572','Sand Red']
351:['F785B1','Medium Dark Pink']
366:['FA9C1C','Earth Orange']
373:['8.45E+86','Sand Purple']
378:['A0BCAC','Sand Green']
379:['6074A1','Sand Blue']
383:['E0E0E0','Chrome Silver']
450:['B67B50','Fabuland Brown']
462:['FFA70B','Medium Orange']
484:['A95500','Dark Orange']
503:['E6E3DA','Very Light Gray']
1000:['D9D9D9','Glow in Dark White']
1001:['93910000','Medium Violet']
1002:['C0F500','Glitter Trans-Neon Green']
1003:['68BCC5','Glitter Trans-Light Blue']
1004:['FCB76D','Trans-Flame Yellowish Orange']
1005:['FBE890','Trans-Fire Yellow']
1006:['B4D4F7','Trans-Light Royal Blue']
1007:['8E5597','Reddish Lilac']
1008:['039CBD','Vintage Blue']
1009:['1E601E','Vintage Green']
1010:['CA1F08','Vintage Red']
1011:['F3C305','Vintage Yellow']
1012:['EF9121','Fabuland Orange']
1013:['F4F4F4','Modulex White']
1014:['AfB5C7','Modulex Light Bluish Gray']
1015:['9C9C9C','Modulex Light Gray']
1016:['595D60','Modulex Charcoal Gray']
1017:['6B5A5A','Modulex Tile Gray']
1018:['4D4C52','Modulex Black']
1019:['330000','Modulex Tile Brown']
1020:['5C5030','Modulex Terracotta']
1021:['907450','Modulex Brown']
1022:['DEC69C','Modulex Buff']
1023:['B52C20','Modulex Red']
1024:['F45C40','Modulex Pink Red']
1025:['F47B30','Modulex Orange']
1026:['F7AD63','Modulex Light Orange']
1027:['FFE371','Modulex Light Yellow']
1028:['FED557','Modulex Ochre Yellow']
1029:['BDC618','Modulex Lemon']
1030:['7DB538','Modulex Pastel Green']
1031:['7C9051','Modulex Olive Green']
1032:['27867E','Modulex Aqua Green']
1033:['467083','Modulex Teal Blue']
1034:['0057A6','Modulex Tile Blue']
1035:['61AFFF','Modulex Medium Blue']
1036:['68AECE','Modulex Pastel Blue']
1037:['BD7D85','Modulex Violet']
1038:['F785B1','Modulex Pink']
1039:['FFFFFF','Modulex Clear']
1040:['595D60','Modulex Foil Dark Gray']
1041:['9C9C9C','Modulex Foil Light Gray']
1042:['6400','Modulex Foil Dark Green']
1043:['7DB538','Modulex Foil Light Green']
1044:['0057A6','Modulex Foil Dark Blue']
1045:['68AECE','Modulex Foil Light Blue']
1046:['4B0082','Modulex Foil Violet']
1047:['8B0000','Modulex Foil Red']
1048:['FED557','Modulex Foil Yellow']
1049:['F7AD63','Modulex Foil Orange']
1050:['FF698F','Coral']
1051:['5AC4DA','Pastel Blue']
1052:['F08F1C','Glitter Trans-Orange']
1053:['68BCC5','Trans-Blue Opal']
1054:['CE1D9B','Trans-Medium Reddish Violet Opal']
1055:['FCFCFC','Trans-Clear Opal']
1056:['583927','Trans-Brown Opal']
1057:['C9E788','Trans-Light Bright Green']
1058:['94E5AB','Trans-Light Green']
1059:['8320B7','Trans-Purple Opal']
1060:['84B68D','Trans-Green Opal']
1061:['0020A0','Trans-Dark Blue Opal']
1062:['EBD800','Vibrant Yellow']
1063:['B46A00','Metallic Copper']
1064:['FF8014','Fabuland Red']
1065:['AC8247','Reddish Gold']
1066:['DD982E','Curry']
1067:['AD6140','Dark Nougat']
1068:['EE5434','Reddish Orange']
1069:['D60026','Pearl Red']
1070:['0059A3','Pearl Blue']
1071:['008E3C','Pearl Green']
1072:['57392C','Pearl Brown']
1073:['0A1327','Pearl Black']
1074:['009ECE','Duplo Blue']
1075:['3E95B6','Duplo Medium Blue']
1076:['FFF230','Duplo Lime']
1077:['78FC78','Fabuland Lime']
1078:['468A5F','Duplo Medium Green']
1079:['60BA76','Duplo Light Green']
1080:['F3C988','Light Tan']
1081:['872B17','Rust Orange']
1082:['FE78B0','Clikits Pink']
1083:['945148','Two-tone Copper']
1084:['AB673A','Two-tone Gold']
1085:['737271','Two-tone Silver']
1086:['6A7944','Pearl Lime']
1087:['FF879C','Duplo Pink']
9999:['05131D','[No Color/Any Color]']
}


 
BRICK_NAME_PREFIX = 'Brick_'
VIEWER_NAME_PREFIX = 'Viewer_'
 
SURFACE_SCALE = 5
MAX_RANDOM_BRICK_HEIGHT = 8
 
bricks_colors_weights_sum = 0
for color in TRAINING_BRICK_COLORS_RGB:
    bricks_colors_weights_sum += color[1]
 
current_scene_index = 1
current_scene_bricks = set()
scene_folder_name = ''
 
#################################
# Utils
 
def get_rgb(color_id):
    color_array =  COLOR_ID_RGB_DICT[color_id]
    return color_array[0]


def element_id_to_design_id_color(element_id):
    #Todo - build function
    design_id_color = ELEMENT_DESIGN_ID_DICT[element_id]
    return design_id_color
 
 
def get_design_ids_array_of_set(set):
    design_ids_array = []
    for brick in set
        design_ids_array.append(element_id_to_design_id_color(brick[0]))
    return design_ids_array



def get_rgbs_array_of_set(set):
    rgb_ids_array = []
    for brick in set
        design_id_color = element_id_to_design_id_color(brick[0])
        rgb_ids_array.append(get_rgb(design_id_color[1]))
    return rgb_ids_array
    
   

    
    


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
 
 
def write_batch_parameters():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    params = {
        "TIMESTAMP": timestamp,
        "GENERATED_SCENES_COUNT": GENERATED_SCENES_COUNT,
        "BATCH_FOLDER_NAME": BATCH_FOLDER_NAME,
        "OBJECTS_IN_SCENE_COUNT_MAX": OBJECTS_IN_SCENE_COUNT_MAX,
        "OBJECTS_IN_SCENE_COUNT_MIN": OBJECTS_IN_SCENE_COUNT_MIN,
        "IMAGE_X_RESOLUTION": IMAGE_X_RESOLUTION,
        "IMAGE_Y_RESOLUTION": IMAGE_Y_RESOLUTION,
        "IMAGE_RENDER_MAX_CYCLES": IMAGE_RENDER_MAX_CYCLES,
        "TRAINING_BRICKS_FILE_NAMES": TRAINING_BRICKS_FILE_NAMES,
        "TRAINING_BRICK_COLORS_RGB": TRAINING_BRICK_COLORS_RGB,
    }
    batch_folder = os.path.join(GENERATED_DATA_ROOT_PATH,
                                BATCH_FOLDER_NAME)
    Path(batch_folder).mkdir(parents=True, exist_ok=True)
    f = open(os.path.join(batch_folder, BATCH_FILE_PREFIX+'parapmeters.json'), 'a')
    f.write(json.dumps(params, indent=4))
    f.close()
 
 
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
    for color in get_rgbs_array_of_set(LONDON_21034):
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
 
 
def create_file_output_node(scene_folder, render_layers_node):
    tree = bpy.context.scene.node_tree
    file_output_node = tree.nodes.new('CompositorNodeOutputFile')
    file_output_node.base_path = scene_folder
    file_output_node.location = 100, 0
    file_output_node.format.file_format = 'JPEG'
    tree = bpy.context.scene.node_tree
    links = tree.links
    link = links.new(render_layers_node.outputs[0], file_output_node.inputs[0])
    file_output_node.location = (800, 0)
    return file_output_node
 
 
def set_lighting():
    print('Lighting not implemented')
    # todo: consider area lighting to diffuse shadows
    # todo: consider multiple light sources (seem less frequest in pics we have)
 
 
def set_camera():
    camera = bpy.data.objects['Camera']
    camera_x = random.randint(0, SURFACE_SCALE*2)-SURFACE_SCALE/2
    camera_y = random.randint(0, SURFACE_SCALE*2)-SURFACE_SCALE/2
    camera_d = random.randint(8, 15)
    camera.location = mathutils.Vector((camera_x, camera_y, 10))
    point_camera_to_origin(camera, camera_d)
 
 
def get_random_surface_image_path():
    return SURFACE_IMAGES_DIR+'\\'+random.choice(os.listdir(SURFACE_IMAGES_DIR))
 
 
def create_surface():
    surface = bpy.data.objects.get('Plane')
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
    texture_image_path = get_random_surface_image_path()
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
    meshes = set()
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
    # write_render_data()
    if (current_scene_index < (GENERATED_SCENES_COUNT+1)):
        generate_and_render_scene(current_scene_index)
 
 
def write_render_data():
    # Collect render data
    f = open(GENERATED_DATA_ROOT_PATH+'\\' +
             scene_folder_name+"\\demofile2.txt", "a")
    for brick in current_scene_bricks:
        viewer_name = VIEWER_NAME_PREFIX + brick.name
        viewer_node = bpy.context.scene.node_tree.nodes[viewer_name]
        #viewer_node =bpy.data.images[viewer_name]
        viewer_node.select = True
        # get viewer pixels
        pixels = bpy.data.images['Viewer Node'].pixels
        # size is always width * height * 4 (rgba)
        f.writelines(brick.name+' '+str(len(pixels))+'\n')
        # copy buffer to numpy array for faster manipulation
        arr = np.array(pixels[:]).reshape(
            (IMAGE_X_RESOLUTION, IMAGE_Y_RESOLUTION, 4))
        f.writelines(str(bbox2(arr))+'\n')
    f.close()
 
 
def generate_and_render_scene(i_scene):
    create_surface()
    set_lighting()
    set_camera()
    delete_existing_bricks()
    render_layers_node = clear_render_tree_and_create_layers_node()
    batch_folder = os.path.join(GENERATED_DATA_ROOT_PATH, BATCH_FOLDER_NAME)
    file_output_node = create_file_output_node(
        batch_folder, render_layers_node)
    global scene_folder_name
    scene_folder_name = BATCH_FILE_PREFIX+str(i_scene)
    file_output_node.base_path += '/'+scene_folder_name
    file_output_node.file_slots[0].path = "Img_"+BATCH_FILE_PREFIX
 
 
    for brickArray in LONDON_21034:
        print(brickArray[1])
        for i_brick in range(0,brickArray[1]):
            brick_code = brickArray[0]
            brick_id = brick_code + '_' + str(i_brick)
            bpy.ops.import_scene.importldraw(ldrawPath=LDRAW_PATH,
                                            filepath=LDRAW_LIB_PARTS_PATH+brick_code+".dat", addEnvironment=False, positionCamera=False)
            brick = bpy.context.selected_objects[0]
            print("________________" + str(brickArray[1]) + "________________")
            current_scene_bricks.add(brick)
            brick.name = BRICK_NAME_PREFIX+brick_id
            brick.material_slots[0].link = 'OBJECT'
            color = get_rgb(element_id_to_design_id_color(brickArray[0])[1])
            brick.material_slots[0].material = MATERIALS_DICTIONARY[color]
 
 
        # # file_output_node.file_slots.remove(file_output_node.inputs[0])
        # bricks_count = random.randint(
        #     OBJECTS_IN_SCENE_COUNT_MIN, OBJECTS_IN_SCENE_COUNT_MAX)
        # for i_brick in range(0, bricks_count):
        #     # Create
        #     brick_code = random.sample(TRAINING_BRICKS_FILE_NAMES, k=1)[0]
        #     brick_id = brick_code+'_'+str(i_brick)
        #     bpy.ops.import_scene.importldraw(ldrawPath=LDRAW_PATH,
        #                                      filepath=LDRAW_LIB_PARTS_PATH+brick_code+".dat", addEnvironment=False, positionCamera=False)
        #     brick = bpy.context.selected_objects[0]
        #     current_scene_bricks.add(brick)
        #     brick.name = BRICK_NAME_PREFIX+brick_id
        #     # Material and Color
        #     brick.material_slots[0].link = 'OBJECT'
        #     color = pick_random_brick_color_hex()
        #     brick.material_slots[0].material = MATERIALS_DICTIONARY[color]
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
            brick_mask_file_name = "Mask_"+BATCH_FILE_PREFIX+str(i_scene)+'_'+brick_id+'_'+str(color)+'_'
            tree = bpy.context.scene.node_tree
            #id_mask_node = tree.nodes.new('CompositorNodeIDMask')
            cryptomatte_node = tree.nodes.new('CompositorNodeCryptomatteV2')
            cryptomatte_node.matte_id = brick.name
            cryptomatte_node.location = [400, -50*(i_brick+4)]
            cryptomatte_node.hide = True
            file_output_node.file_slots.new(brick_mask_file_name)
            file_slot=file_output_node.file_slots[brick_mask_file_name]
            file_slot.format.file_format = 'PNG'
            file_slot.format.color_mode = 'BW'
            file_slot.use_node_format = False
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
    viewer_node.name = VIEWER_NAME_PREFIX+brick.name
    viewer_node.location = [800, -50*(i_brick+10)]
    tree.links.new(
        cryptomatte_node.outputs['Matte'],
        viewer_node.inputs[0]
    )
    # rendering is timed after animation completion in animation callback
 
 
############################
# startup code:
set_blender()
write_batch_parameters()
MATERIALS_DICTIONARY = create_materials_dictionary()
bpy.app.handlers.render_post.append(render_complete_callback)
 
generate_and_render_scene(current_scene_index)
 
 
 

