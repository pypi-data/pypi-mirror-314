# -*- coding: utf-8 -*-

import time
import copy
import os
import json
from tqdm import tqdm
from xml.dom.minidom import Document
import cv2

def get_categories(categories_json_file: str = None) -> dict:
    if categories_json_file is None:
        categories = {
            "supercategory": "person",
            "id": 1,
            "name": "person",
            "keypoints": [
                "nose",
                "l_shoulder",
                "r_shoulder",
                "l_elbow",
                "r_elbow",
                "l_wrist",
                "r_wrist",
                "l_hip",
                "r_hip",
                "l_knee",
                "r_knee",
                "l_ankle",
                "r_ankle"
            ],
            "skeleton": [
                [1, 2],
                [1, 3],
                [2, 3],
                [2, 4], [4, 6],
                [3, 5], [5, 7],
                [2, 8],
                [3, 9],
                [8, 9],
                [8, 10], [10, 12],
                [9, 11], [11, 13]
            ]
        }
    else:
        with open(categories_json_file, 'r', encoding='utf-8') as file:
            categories = json.load(file)    
    return categories

def labelme2coco(labelme_json_path, coco_json_path, categories_json_file='./categories_person.json', exists_add=False, bbox=None):
    with open(labelme_json_path, 'r', encoding='utf-8') as f:
        labelme_data = json.load(f)

    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    if os.path.exists(coco_json_path):
        if exists_add:
            with open(coco_json_path, 'r') as f:
                coco_data = json.load(f)
        else:
            coco_json_path = coco_json_path.split('.')[0] + '_' + str(time.time()) + '.json'
        
    file_name = os.path.basename(labelme_data['imagePath'])
    image_id = file_name.split('.')[0]

    categorie_i = get_categories(categories_json_file)
    if categorie_i not in coco_data['categories']:
        coco_data['categories'].append(categorie_i)

    image_i = {'height': labelme_data['imageHeight'], 
               'width': labelme_data['imageWidth'],
               'file_name': file_name,
               'id': image_id}
    coco_data['images'].append(image_i)

    keypoints = [0] * 3 * len(categorie_i['keypoints'])
    shapes = labelme_data['shapes']
    for shape_i in shapes:
        if shape_i['shape_type'] == 'rectangle':
            (x1, y1), (x2, y2) = shape_i['points']
            x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
            y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1)
            if bbox is None:
                bbox = [x1, y1, x2 - x1, y2 - y1]
        elif shape_i['shape_type'] == 'point':
            idx = int(shape_i['label'])
            keypoints[(idx - 1) * 3 + 0] = shape_i['points'][0][0]
            keypoints[(idx - 1) * 3 + 1] = shape_i['points'][0][1]
            keypoints[(idx - 1) * 3 + 2] = 2
            if shape_i['group_id'] is not None:
                keypoints[(idx - 1) * 3 + 2] = int(shape_i['group_id'])
    if bbox is None:
        bbox = [1, 1, labelme_data['imageWidth'] - 1, labelme_data['imageHeight'] - 1]
    annotation_i = {'segmentation': [[]],
                    'num_keypoints': len(categorie_i['keypoints']),
                    'area': int((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])),
                    'iscrowd': 0,
                    'keypoints': copy.deepcopy(keypoints),
                    'image_id': image_id,
                    'bbox': bbox,
                    'category_id': 1,
                    'id': image_id
                    }
    coco_data['annotations'].append(annotation_i)
    with open(coco_json_path, 'w') as f:
        json.dump(coco_data, f, indent=4, ensure_ascii=False)
    return coco_json_path

def labelmes2coco(labelme_json_folder, coco_json_path, categories_json_file='./categories_person.json', bbox=None):
    # 初始一部分数据
    if os.path.exists(coco_json_path):
        coco_json_path = coco_json_path.split('.')[0] + '_' + str(time.time()) + '.json'
    print('Start to convert labelme json to coco json...')
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    categorie_i = get_categories(categories_json_file)
    if categorie_i not in coco_data['categories']:
        coco_data['categories'].append(categorie_i)
    
    # 遍历添加
    json_paths = [os.path.join(labelme_json_folder, f) for f in os.listdir(labelme_json_folder) if f.endswith('.json')]
    for labelme_json_path in tqdm(json_paths, desc=labelme_json_folder, unit=' json'):
        # labelme2coco(labelme_json_path, coco_json_path, exists_add=True, bbox=bbox)
        with open(labelme_json_path, 'r', encoding='utf-8') as f:
            labelme_data = json.load(f)
            file_name = os.path.basename(labelme_data['imagePath'])
            image_id = file_name.split('.')[0]

            image_i = {'height': labelme_data['imageHeight'], 
                    'width': labelme_data['imageWidth'],
                    'file_name': file_name,
                    'id': image_id}
            coco_data['images'].append(image_i)

            keypoints = [0] * 3 * len(categorie_i['keypoints'])
            shapes = labelme_data['shapes']
            for shape_i in shapes:
                if shape_i['shape_type'] == 'rectangle':
                    (x1, y1), (x2, y2) = shape_i['points']
                    x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
                    y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1)
                    if bbox is None:
                        bbox = [x1, y1, x2 - x1, y2 - y1]
                elif shape_i['shape_type'] == 'point':
                    idx = int(shape_i['label'])
                    keypoints[(idx - 1) * 3 + 0] = shape_i['points'][0][0]
                    keypoints[(idx - 1) * 3 + 1] = shape_i['points'][0][1]
                    keypoints[(idx - 1) * 3 + 2] = 2
                    if shape_i['group_id'] is not None:
                        keypoints[(idx - 1) * 3 + 2] = int(shape_i['group_id'])
            if bbox is None:
                bbox = [1, 1, labelme_data['imageWidth'] - 1, labelme_data['imageHeight'] - 1]
            annotation_i = {'segmentation': [[]],
                            'num_keypoints': len(categorie_i['keypoints']),
                            'area': int((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])),
                            'iscrowd': 0,
                            'keypoints': copy.deepcopy(keypoints),
                            'image_id': image_id,
                            'bbox': bbox,
                            'category_id': 1,
                            'id': image_id
                            }
            coco_data['annotations'].append(annotation_i)
    with open(coco_json_path, 'w') as f:
        json.dump(coco_data, f, indent=4, ensure_ascii=False)
        print('save coco json to {}'.format(coco_json_path))
    return coco_json_path

def splited_labelmes2cocos(splited_labelmes_folder, categories_json_file='./categories_person.json', bbox=None, cocos_folder=None):
    if cocos_folder is None:
        cocos_folder = splited_labelmes_folder
    labelmes2coco(splited_labelmes_folder + '/train', cocos_folder + '/train.json', categories_json_file, bbox)
    labelmes2coco(splited_labelmes_folder + '/val', cocos_folder + '/val.json', categories_json_file, bbox)
    labelmes2coco(splited_labelmes_folder + '/test', cocos_folder + '/test.json', categories_json_file, bbox)



def coco2labelmes(coco_json_path, labelme_json_folder):
    """
    将coco格式的json转化为labelme的json格式
    :param coco_json_path: coco格式的json文件路径
    :param labelme_json_folder: labelme的json文件夹路径
    :return:
    """
    if not os.path.exists(labelme_json_folder):
        os.makedirs(labelme_json_folder)
    with open(coco_json_path, 'r') as f:
        coco_dict = json.load(f)

    for image_i in coco_dict['images']:
        labelme_dict_i = {'version': '5.5.0',
                          'flags': {},
                          'shapes': [],
                          'imagePath': image_i['file_name'],
                          'imageData': None,
                          'imageHeight': image_i['height'],
                          'imageWidth': image_i['width']
                          }
        for annotation_i in coco_dict['annotations']:
            if annotation_i['image_id'] == image_i['id']:
                shape_i = {'label': 'person',
                          'points': [[annotation_i['bbox'][0], annotation_i['bbox'][1]],
                                     [annotation_i['bbox'][0] + annotation_i['bbox'][2], annotation_i['bbox'][1] + annotation_i['bbox'][3]]],
                          'group_id': None,
                          'description': '',
                          'shape_type': 'rectangle',
                          'flags': {},
                          'mask': None
                          }
                labelme_dict_i['shapes'].append(shape_i)
                for idx in range(annotation_i['num_keypoints']):
                    shape_i = {'label': str(idx + 1),
                               'points': [[annotation_i['keypoints'][idx * 3 + 0], annotation_i['keypoints'][idx * 3 + 1]]],
                               'group_id': None,
                               'description': '',
                               'shape_type': 'point',
                               'flags': {},
                               'mask': None
                               }
                    labelme_dict_i['shapes'].append(shape_i)
        labelme_path_i = os.path.join(labelme_json_folder, image_i['file_name'].split('.')[0] + '.json')
        if os.path.exists(labelme_path_i):
            labelme_path_i = os.path.join(labelme_json_folder, f"{image_i['file_name'].split('.')[0]}_{int(time.time() * 1000)}.json")
        with open(labelme_path_i, 'w') as f:
            json.dump(labelme_dict_i, f, indent=4, ensure_ascii=False)
    print(f"save {len(coco_dict['images'])} images to {labelme_json_folder}")


def txt2xml(txtpath, picfolder, class_dict, xmlfolder, img_format=".bmp", element_folder="xxx_folder"):  # 读取txt路径，xml保存路径，数据集图片所在路径
    if not os.path.exists(xmlfolder):
        os.makedirs(xmlfolder)
    name = os.path.basename(txtpath)
    # 读取图片和txt列表
    img = cv2.imread(os.path.join(picfolder, name[0:-4] + img_format))
    Pheight, Pwidth, Pdepth = img.shape

    with open(txtpath, 'r') as f:
        txtList = f.readlines()
        xmlBuilder = Document()
        # 创建annotation标签
        annotation = xmlBuilder.createElement("annotation")
        xmlBuilder.appendChild(annotation)
        # folder标签
        folder = xmlBuilder.createElement("folder")
        folderContent = xmlBuilder.createTextNode(element_folder)
        folder.appendChild(folderContent)
        annotation.appendChild(folder)
        # filename标签
        filename = xmlBuilder.createElement("filename")
        filenameContent = xmlBuilder.createTextNode(name[0:-4] + img_format)
        filename.appendChild(filenameContent)
        annotation.appendChild(filename)
        # size标签
        size = xmlBuilder.createElement("size")
        # size子标签width
        width = xmlBuilder.createElement("width")
        widthContent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthContent)
        size.appendChild(width)
        # size子标签height
        height = xmlBuilder.createElement("height")
        heightContent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightContent)
        size.appendChild(height)
        # size子标签depth
        depth = xmlBuilder.createElement("depth")
        depthContent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthContent)
        size.appendChild(depth)
        annotation.appendChild(size)

        for i in txtList:
            oneline = i.strip().split(" ")

            object = xmlBuilder.createElement("object")
            picname = xmlBuilder.createElement("name")
            nameContent = xmlBuilder.createTextNode(class_dict[int(oneline[0])])
            picname.appendChild(nameContent)
            object.appendChild(picname)
            pose = xmlBuilder.createElement("pose")
            poseContent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(poseContent)
            object.appendChild(pose)
            truncated = xmlBuilder.createElement("truncated")
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)
            difficult = xmlBuilder.createElement("difficult")
            difficultContent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultContent)
            object.appendChild(difficult)
            bndbox = xmlBuilder.createElement("bndbox")
            xmin = xmlBuilder.createElement("xmin")
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)
            ymin = xmlBuilder.createElement("ymin")
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)
            xmax = xmlBuilder.createElement("xmax")
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)
            ymax = xmlBuilder.createElement("ymax")
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)
            object.appendChild(bndbox)

            annotation.appendChild(object)

        f = open(os.path.join(xmlfolder, name[0:-4] + ".xml"), 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()

def txts2xmls(txtfolder, picfolder, class_dict, xmlfolder, img_format=".bmp", element_folder="xxx_folder"):
    # (txtpath, picfolder, class_dict, xmlfolder, img_format=".bmp", element_folder="xxx_folder")
    for txt in tqdm(os.listdir(txtfolder), desc=txtfolder, unit=' txt'):
        txt2xml(os.path.join(txtfolder, txt), picfolder, class_dict, xmlfolder, img_format, element_folder)
    print(f"save {len(os.listdir(txtfolder))} xmls to {xmlfolder}")
