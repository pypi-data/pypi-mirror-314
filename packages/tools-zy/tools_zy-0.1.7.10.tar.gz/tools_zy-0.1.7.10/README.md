# tools_zy[![Version][version-badge]][version-link] ![MIT License][license-badge]


此工具包旨在给AI工作者提供一把趁手的工具，尽量简化非核心的工作。\
其中包含深度学习模型过程中可能会用到的一些工具，比如数据整理、格式转换、划分数据集等。

因此也要注意，其中某些函数可能并没有提供过多自由度，如果需要，请自行修改。

### 安装

```bash
$ pip install tools-zy
```

### 使用

含有的功能示例如下：
```python
import tools_zy as tz

# 复制、移动文件夹中以.bmp结尾的文件。（还支持指定文件名，支持递归操作）
tz.copy_file("/home/org_folder", "/home/new_folder", format=".bmp")
tz.move_file("/home/org_folder", "/home/new_folder", format=".bmp")

# 获取（复制、移动）文件夹中以.bmp结尾的一些随机文件。
tz.copy_some_random_files("/home/org_folder", "/home/new_folder", 1000, format='.bmp')
tz.move_some_random_files("/home/org_folder", "/home/new_folder", 1000, format='.bmp')

# 划分分类数据集
img_folder = r"/home/classify/rawData"  # 包含n个名称为数字序列的文件夹
out_folder = r"/home/classify/splitData"  # 
tz.split_classifid_images(img_folder, out_folder, (0.8, 0.2, 0), format=".bmp")
# 划分lablmes数据集 (划分图片和json文件到train, val, test文件夹)
labelme_folder = r"D:\Zhiyuan\pics_get\keypoints\20241118"
data_folder = tz.split_labelmes(labelme_folder, ratio=(0.85, 0.1, 0.05), format=".bmp")


# 将labelme的json格式转化为coco格式，要求图片和json文件名相同且在同一文件夹下
labelme_json_folder = r'D:\Zhiyuan\pics_get\keypoints\keypoints\20241030' 
coco_json_path = r'D:\Zhiyuan\pics_get\keypoints\keypoints\20241030.json'
categories_json_file = r"D:\Zhiyuan\code\tz\categories_person.json"
tz.labelmes2coco(labelme_json_folder, coco_json_path, categories_json_file, bbox=[1, 1, 511, 1023])
coco_json_path = r'D:\Zhiyuan\pics_get\keypoints\keypoints\20241121.json'
labelme_json_folder = r'D:\Zhiyuan\pics_get\keypoints\keypoints\20241121'
tz.coco2labelmes(coco_json_path, labelme_json_folder)



```
#### labelme标注文件连续操作：划分labelme数据集->转化为coco格式
```python
labelme_folder = r"D:\Zhiyuan\pics_get\keypoints\20241118"
splited_labelmes_folder = tz.split_labelmes(labelme_folder, ratio=(0.85, 0.1, 0.05), format='.bmp')
categories_json_file = r"D:\Zhiyuan\code\tz\categories_person.json"
tz.splited_labelmes2cocos(splited_labelmes_folder, categories_json_file=categories_json_file)
```


### License

[MIT](https://github.com/wzy-777/tools_zy/blob/main/LICENSE)


[version-badge]:   https://img.shields.io/badge/version-0.1-brightgreen.svg
[version-link]:    https://pypi.org/project/tools-zy/
[license-badge]:   https://img.shields.io/github/license/pythonml/douyin_image.svg