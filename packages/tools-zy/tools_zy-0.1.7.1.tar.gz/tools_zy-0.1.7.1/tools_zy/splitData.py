import os
import random
import time
import shutil
from . import utils

def check_sequential_folders(folder_path):
    folder_list = sorted(os.listdir(folder_path))
    count = 0
    for _, folder_name in enumerate(folder_list):
        expected_name = str(count)
        if folder_name == expected_name:
            count += 1
    return count

def split_classifid_images(top_folder, out_folder, split_list, format=".bmp", num_class=None):
    """
    top_folder: 图片文件夹的根目录，里面有多个数字命名的子文件夹
    """
    if num_class is None:
        num_class = check_sequential_folders(top_folder)
    # 创建输出文件夹 
    train_path = os.path.join(out_folder, "train")
    val_path = os.path.join(out_folder, "val")
    test_path = os.path.join(out_folder, "test")
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)
    # 
    train, val, test = split_list
    for i in range(num_class):
        count = 0
        class_num = str(i)
        img_folder = os.path.join(top_folder, class_num)
        all_img = os.listdir(img_folder)
        all_name = [os.path.splitext(name)[0] for name in all_img]
        random.shuffle(all_name)  # 打乱顺序
        train_name = all_name[:int(train * len(all_name))]
        val_name = all_name[int(train * len(all_name)):int((train + val) * len(all_name))]
        test_name = all_name[int((train + val) * len(all_name)):]
        utils.copy_files(img_folder, "/".join([train_path, class_num]), train_name, format)
        utils.copy_files(img_folder, "/".join([val_path, class_num]), val_name, format)
        utils.copy_files(img_folder, "/".join([test_path, class_num]), test_name, format)



def split_labelmes(labelme_folder: str, ratio: tuple = (0.85, 0.1, 0.05), formats=['jpg', 'bmp']):
    random.seed(time.time())

    # 获取源文件夹中的所有JPG文件
    pics = [f for f in os.listdir(labelme_folder) if f.split('.')[-1] in formats]
    # 随机打乱并划分JPG文件列表
    random.shuffle(pics)
    total_files = len(pics)
    train_ratio, val_ratio, test_ratio = ratio
    train_cnt, val_cnt = int(total_files * train_ratio), int(total_files * val_ratio)
    train_jpgs = pics[:train_cnt]
    val_jpgs = pics[train_cnt:train_cnt + val_cnt]
    test_jpgs = pics[train_cnt + val_cnt:]

    def move_files(pics, target_dir):
        os.makedirs(target_dir, exist_ok=True)
        img_folder = os.path.join(target_dir, 'images')
        os.makedirs(img_folder, exist_ok=True)
        json_folder = os.path.join(target_dir, 'labelme_json')
        os.makedirs(json_folder, exist_ok=True)

        for pic in pics:
            json_file = pic.replace(pic.split('.')[-1], 'json')
            shutil.copy(os.path.join(labelme_folder, pic), img_folder)
            if os.path.exists(os.path.join(labelme_folder, json_file)):
                shutil.copy(os.path.join(labelme_folder, json_file), json_folder)

    # 移动文件到相应的目标文件夹
    split_folder = labelme_folder + '_split'
    move_files(train_jpgs, split_folder + '/train')
    move_files(val_jpgs, split_folder + '/val')
    move_files(test_jpgs, split_folder + '/test')

    print(f"split pic and json to:\n"
          f"==>{split_folder}")
    return split_folder
