
import hashlib
import io
import logging
import os
import random

from lxml import etree
import PIL.Image
import tensorflow.compat.v1 as tf


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def recursive_parse_xml_to_dict(xml):
    """Recursively parses XML contents to python dict.

    We assume that `object` tags are the only ones that can appear
    multiple times at the same level of a tree.

    Args:
      xml: xml tree obtained by parsing XML file contents using lxml.etree

    Returns:
      Python dictionary holding XML contents.
    """
    if not xml:
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = recursive_parse_xml_to_dict(child)
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def dict_to_tf_example(input_folder_path, xml, label_map_dict, ignore_difficult_instances=False):
    data = recursive_parse_xml_to_dict(xml)['annotation']
    img_path = os.path.join(
        input_folder_path, data['filename'])
    with tf.gfile.GFile(img_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)
    if image.format != 'JPEG':
        raise ValueError('Image format not JPEG '+image.format)
    key = hashlib.sha256(encoded_jpg).hexdigest()

    width = int(data['size']['width'])
    height = int(data['size']['height'])

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []
    truncated = []
    poses = []
    difficult_obj = []
    if 'object' in data:
        for obj in data['object']:
            difficult = bool(int(obj['difficult']))
            if ignore_difficult_instances and difficult:
                continue

            global current_lable_id
            obj_name = obj['name']
            if obj_name not in label_map_dict:
                label_map_dict[obj_name] = current_lable_id
                current_lable_id += 1

            difficult_obj.append(int(difficult))

            xmin.append(float(obj['bndbox']['xmin']) / width)
            ymin.append(float(obj['bndbox']['ymin']) / height)
            xmax.append(float(obj['bndbox']['xmax']) / width)
            ymax.append(float(obj['bndbox']['ymax']) / height)
            classes_text.append(obj['name'].encode('utf8'))
            classes.append(label_map_dict[obj_name])
            truncated.append(int(obj['truncated']))
            poses.append(obj['pose'].encode('utf8'))

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': int64_feature(height),
        'image/width': int64_feature(width),
        'image/filename': bytes_feature(
            data['filename'].encode('utf8')),
        'image/source_id': bytes_feature(
            data['filename'].encode('utf8')),
        'image/key/sha256': bytes_feature(key.encode('utf8')),
        'image/encoded': bytes_feature(encoded_jpg),
        'image/format': bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': float_list_feature(xmin),
        'image/object/bbox/xmax': float_list_feature(xmax),
        'image/object/bbox/ymin': float_list_feature(ymin),
        'image/object/bbox/ymax': float_list_feature(ymax),
        'image/object/class/text': bytes_list_feature(classes_text),
        'image/object/class/label': int64_list_feature(classes),
        'image/object/difficult': int64_list_feature(difficult_obj),
        'image/object/truncated': int64_list_feature(truncated),
        'image/object/view': bytes_list_feature(poses),
    }))
    return example


def convert(input_folder_path, output_folder, output_file_prefix,train_proportion, test_proportion,):

    train_writer = tf.python_io.TFRecordWriter(os.path.join(
        output_folder, output_file_prefix+'_train.record'))
    test_writer = tf.python_io.TFRecordWriter(os.path.join(
        output_folder, output_file_prefix+'_test.record'))
    lable_map_file_name = os.path.join(
        output_folder, output_file_prefix+'_label_map.pbtxt')

    label_map_dict = {}

    for el in os.scandir(input_folder_path):
        if (el.is_file) and el.name.endswith('.xml'):
            with tf.gfile.GFile(el.path, 'r') as fid:
                xml_str = fid.read()
            xml = etree.fromstring(xml_str)
            tf_example = dict_to_tf_example(
                input_folder_path, xml, label_map_dict)

            if (random.uniform(0, train_proportion+test_proportion)<train_proportion):
                train_writer.write(tf_example.SerializeToString())
            else:
                test_writer.write(tf_example.SerializeToString())
    train_writer.close()
    test_writer.close()

    f=open(lable_map_file_name,'w')
    for label in label_map_dict.items():
        f.write('item {\n')
        f.write('   name: "'+label[0]+'",\n')
        f.write('   id: '+str(label[1])+',\n')
        f.write('   display_name: "'+label[0]+'",\n')
        f.write('}\n')
    f.close()


###############################
# run
INPUT_FOLDER_PATH = 'C:\\temp\\Data_Dec_19_22_43'
OUTPUT_FOLDER = 'C:\\temp\\TFRecords'
OUTPUT_FILE_PREFIX = 'Dec_19_22_43_2'
TRAIN_PROPOTION = 90
TEST_PROPORTION = 10

# global counter
current_lable_id = 1

convert(INPUT_FOLDER_PATH, OUTPUT_FOLDER, OUTPUT_FILE_PREFIX, TRAIN_PROPOTION, TEST_PROPORTION)
