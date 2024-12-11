#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/08/27
# @Author  : wanggaofei03
# @File    : std_alg_common.py
"""
import os
import json
import yaml
from argparse import ArgumentParser
import shutil
import bcelogger

from gaea_operator.metric.types.metric import LOSS_METRIC_NAME, \
    MAP_METRIC_NAME, \
    AP50_METRIC_NAME, \
    AR_METRIC_NAME, \
    BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME, \
    ACCURACY_METRIC_NAME, \
    CLASSIFICATION_ACCURACY_METRIC_NAME, \
    SEG_MAP_METRIC_NAME, \
    SEG_AP50_METRIC_NAME, \
    SEG_AR_METRIC_NAME

NX_SPLIT_CHAR = ' '

NX_ANNOTATION_TYPE_DET = 'detect'
NX_ANNOTATION_TYPE_CLS = 'classify'
NX_ANNOTATION_TYPE_SEMANTIC_SEG = 'semantic_segment'    # 语义分割
NX_ANNOTATION_TYPE_INSTANCE_SEG = 'instance_segment'    # 实例分割

NX_METRIC_MAP = {
    'metric_names': {
        NX_ANNOTATION_TYPE_DET: [LOSS_METRIC_NAME, MAP_METRIC_NAME, AP50_METRIC_NAME, AR_METRIC_NAME],
        NX_ANNOTATION_TYPE_CLS: [LOSS_METRIC_NAME, ACCURACY_METRIC_NAME],
        NX_ANNOTATION_TYPE_INSTANCE_SEG: [SEG_MAP_METRIC_NAME, SEG_AP50_METRIC_NAME, SEG_AR_METRIC_NAME, \
                                          LOSS_METRIC_NAME, MAP_METRIC_NAME, AP50_METRIC_NAME, AR_METRIC_NAME]
    }, 
    'metric_name': {
        NX_ANNOTATION_TYPE_DET: BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME,
        NX_ANNOTATION_TYPE_CLS: CLASSIFICATION_ACCURACY_METRIC_NAME,
        NX_ANNOTATION_TYPE_INSTANCE_SEG: BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME
    }
}

NX_CATEGORY_MAP = {
    NX_ANNOTATION_TYPE_DET: "Image/ObjectDetection",
    NX_ANNOTATION_TYPE_CLS: "Image/ImageClassification/MultiTask",
    NX_ANNOTATION_TYPE_INSTANCE_SEG: "Image/InstanceSegmentation"
}

def _delete_file_name_prefix(path_str, s3_filesystem_head, local_filesystem_head):
    """
    删除文件名前缀，返回去掉前缀的路径字符串。如果路径字符串不是以指定的前缀开头，则返回None。
    
    Args:
        path_str (str): 包含文件名的路径字符串，可能以bos:/、s3:/或/开头。
    
    Returns:
        Union[str, None]: 去掉前缀后的路径字符串，如果路径字符串不是以指定的前缀开头，则返回None。
    """
    # process s3
    if path_str.startswith('s3:') and s3_filesystem_head is not None and s3_filesystem_head.startswith('s3:'):
        abs_path = path_str.replace(s3_filesystem_head, local_filesystem_head, 1)
        return abs_path
    
    prefix = ['bos:/', '/']
    for _, p in enumerate(prefix):
        if path_str.startswith(p):
            abs_path = path_str[len(p): ]
            if not abs_path.startswith('/'):
                abs_path = '/' + abs_path
            return abs_path
    return None

def _cvt_2_abs_path(path_str, abs_work_path, default_prefix=None, abs_work_folders=None, abs_work_default_folders=None,
                    s3_filesystem_head=None, local_filesystem_head=None):
    """
    将相对路径转换为绝对路径，如果不是bos/s3的路径则会抛出ValueError。
    
    Args:
        path_str (str): 需要转换的路径字符串，可以是相对路径或者绝对路径。
            - 若路径字符串以bos://开头，则认为是bos路径，不进行处理；
            - 若路径字符串以s3://开头，则认为是s3路径，不进行处理；
            - 否则，认为是相对路径，会根据abs_work_path参数进行转换。
        abs_work_path (str): 工作目录的绝对路径，用于处理相对路径。
        default_prefix (str): 默认的前缀，用于处理相对路径。
        abs_work_folders (List[str]): 工作目录的所有子目录文件名，用于处理相对路径。
        abs_work_default_folders (List[str]): 工作目录的默认子目录文件名，用于处理相对路径。
    
    Returns:
        str: 返回一个绝对路径字符串。
    
    Raises:
        ValueError: 当路径字符串不是bos/s3路径且无法通过abs_work_path转换成绝对路径时，会抛出ValueError异常。
    """
    # 1. judge bos/s3
    abs_path = _delete_file_name_prefix(path_str, s3_filesystem_head=s3_filesystem_head, 
                                        local_filesystem_head=local_filesystem_head)
    if abs_path is not None:
        return abs_path
    
    # 2. relative path -> abs path
    top_folder = path_str.split('/')[0]
    default_prefix = default_prefix if default_prefix else 'images'

    # 2.1 search relative path top folder from abs_work_path
    ## 最高优先级为外部指定输入
    if abs_work_folders is not None:
        folders = abs_work_folders
    else:
        ## 如果存在 abs_work_path 赋值 listdir 结果，否则赋值 []
        if os.path.exists(abs_work_path):
            folders = os.listdir(abs_work_path)
        else:
            folders = []
    
    ## 最高优先级为外部指定输入
    if abs_work_default_folders is not None:
        abs_work_default_folders = abs_work_default_folders
    else:
        ## 如果存在 default_prefix 赋值 listdir 结果，否则赋值 []
        abs_work_default_path = os.path.join(abs_work_path, default_prefix)
        if os.path.exists(abs_work_default_path):
            abs_work_default_folders = os.listdir(abs_work_default_path)
        else:
            abs_work_default_folders = []

    if top_folder in folders:
        return os.path.join(abs_work_path, path_str)
    elif default_prefix in folders and top_folder in abs_work_default_folders:
        return os.path.join(abs_work_path, default_prefix, path_str)
    else:
        raise ValueError("relativate path file is invalid, please check. path: {} work_path: {}".format(path_str,
                                                                                                        abs_work_path))

def _retrive_path(path, exts, prefix, tail):
        """
        从指定路径中递归搜索，返回指定扩展名的文件列表

        Args:
        path (str): 指定的文件目录路径
        exts (list[str]): 文件扩展名列表

        Returns:
        list[str]: 返回包含文件路径的列表

        """
        aim_files = []
        n = 0
        for home, dirs, files in os.walk(path):
            for _, f in enumerate(files):
                if f.split('.')[-1] in exts and not f.startswith("."):
                    if f.startswith(prefix) or (len(tail) > 0 and f.split('.')[-2].endswith(tail)):
                        w_name = os.path.join(home, f)
                        n += 1
                        bcelogger.info("FIND" + str(n) + ":" + w_name)
                        aim_files.append(w_name)

        return aim_files

def _modify_detection_annotations(
        src_name, dst_path, abs_work_path, abs_work_folders, abs_work_default_folders, all_image_folders, 
        s3_filesystem_head, local_filesystem_head):
    """
    修改检测标注文件，将相对路径转换为绝对路径。
    
    Args:
        src_name (str): 原始标注文件名，包含路径信息。
        dst_path (str): 目标保存路径。
        abs_work_path (str): 工作目录的绝对路径。
        abs_work_folders (list[str]): 工作目录的所有子目录文件名。
        abs_work_default_folders (list[str]): 工作目录的默认子目录文件名。
        all_image_folders (set[str]): 工作目录下的所有图片文件夹
    
    Returns:
        str: 返回已经修改后的标注文件名，包含完整路径信息。
        
    Raises:
        None.
    """
    json_data = json.load(open(src_name, "r"))
    images = json_data["images"]
    bcelogger.info(f"Parse annotation file {src_name}, image num is {len(images)}")
            
    for img in images:
        img["file_name"] = _cvt_2_abs_path(
                img["file_name"], abs_work_path, 'images', abs_work_folders, abs_work_default_folders, 
                s3_filesystem_head=s3_filesystem_head, local_filesystem_head=local_filesystem_head)
        all_image_folders.add(os.path.dirname(img["file_name"]))
    
    dst_name = os.path.join(dst_path, src_name.split('/')[-1])
    with open(dst_name, "w") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    
    bcelogger.info('save detection annotation file: {}'.format(dst_name))
    return dst_name

# file name do NOT have space character
def _modify_classify_annotations(
        src_name, dst_path, abs_work_path, abs_work_folders, abs_work_default_folders, all_image_folders, 
        s3_filesystem_head, local_filesystem_head):
    """
    修改分类标注文件，将相对路径转换为绝对路径。
    
    Args:
        src_name (str): 源文件名，包括路径。
        dst_path (str): 目标保存路径。
        abs_work_path (str): 工作空间的绝对路径。
        abs_work_folders (list[str]): 工作空间的所有子目录文件名。
        abs_work_default_folders (list[str]): 工作空间的默认子目录文件名。
        all_image_folders (set[str]): 工作空间下的所有图片文件夹
    
    Returns:
        str, optional: 返回目标文件名，如果转换失败则返回None。
    
    Raises:
        None.
    """
    with open(src_name) as f:
        lines = f.readlines()
        
        dst_name = os.path.join(dst_path, src_name.split('/')[-1])
        with open(dst_name, 'w') as dst_f:
            for l in lines:
                # urgly code
                l = l.strip()
                if l.startswith('"') and l.endswith('"'):
                    bcelogger.info('strip head-tail "')
                    l = l.strip('"')
                frags = l.strip().split(NX_SPLIT_CHAR)
                frags[0] = _cvt_2_abs_path(
                        frags[0], abs_work_path, 'images', abs_work_folders, abs_work_default_folders, 
                        s3_filesystem_head=s3_filesystem_head, local_filesystem_head=local_filesystem_head)
                dst_f.write(NX_SPLIT_CHAR.join(frags) + '\n')
                all_image_folders.add(os.path.dirname(frags[0]))
    
            bcelogger.info('save classify annotation file: {}'.format(dst_name))
            return dst_name
    return None

# file name do NOT have space character
def _modify_segment_annotations(src_name, dst_path, abs_work_path, s3_filesystem_head, local_filesystem_head):
    """
    修改分割注释，将相对路径转换为绝对路径。
    
    Args:
        src_name (str): 源文件名，包括路径。
        dst_path (str): 目标路径。
        abs_work_path (str): 工作路径。
    
    Returns:
        str, optional: 返回新的文件名，如果修改失败则返回None。
    
    Raises:
        None.
    """
    with open(src_name) as f:
        lines = f.readlines()
        
        dst_name = os.path.join(dst_path, src_name.split('/')[-1])
        with open(dst_name, 'w') as dst_f:
            for l in lines:
                frags = l.split(NX_SPLIT_CHAR)
                frags[0] = _cvt_2_abs_path(frags[0], abs_work_path, s3_filesystem_head=s3_filesystem_head, 
                                           local_filesystem_head=local_filesystem_head) # image
                frags[1] = _cvt_2_abs_path(frags[1], abs_work_path, s3_filesystem_head=s3_filesystem_head, 
                                           local_filesystem_head=local_filesystem_head) # mask
                dst_f.write(NX_SPLIT_CHAR.join(frags) + '\n')
    
            bcelogger.info('save segment annotation file: {}'.format(dst_name))
            return dst_name
    return None
            
def _copy_annotation_file_2_backup_path(name, backup_path, prefix):
    """
    将指定名称的注释文件复制到备份路径中。
    
    Args:
        name (str): 需要被复制的注释文件名称，包括完整路径。
        backup_path (str): 备份路径，该路径下会存在一个与原始注释文件同名的副本。
    
    Returns:
        None.
    
    Raises:
        None.
    """
    if not os.path.exists(backup_path):
        os.makedirs(backup_path, exist_ok=True)
    dst_name = name.split('/')[-1]
    if prefix not in dst_name:
        dst_name = prefix + '-' + dst_name
    backup_name = os.path.join(backup_path, dst_name)
    shutil.copyfile(src=name, dst=backup_name)
    bcelogger.info('save annotation file to backup path: {}'.format(backup_name))

def _get_txt_annotation_type(name):
    """
    获取文本注释类型，如果最后一行是数字或负数加数字，则返回cls类型，否则返回seg类型。
    
    Args:
        name (str): 文件名，包含路径。
    
    Returns:
        str, optional: 返回以下三种类型之一：NX_ANNOTATION_TYPE_CLS、NX_ANNOTATION_TYPE_SEG、None。默认为None。
            - NX_ANNOTATION_TYPE_CLS (str)：cls类型，表示文本注释类型为分类。
            - None (None)：如果无法确定文本注释类型，则返回None。
    """
    with open(name) as f:
        l = f.readlines()[0].strip()
        l = l.strip()
        if l.startswith('"') and l.endswith('"'):
            bcelogger.info('strip head-tail "')
            l = l.strip('"')
        last_val = l.split(NX_SPLIT_CHAR)[-1]
        if last_val.isdigit() or (last_val.startswith('-') and last_val[1: ].isdigit()):
            return NX_ANNOTATION_TYPE_CLS
        else:
            return NX_ANNOTATION_TYPE_SEMANTIC_SEG # modify latter
    return None

def _get_file_annotation_type(name):
    """
    获取文件的标注类型，支持JSON和TXT两种格式。
    
    Args:
        name (str): 文件名，包含路径信息。
            JSON格式的文件应以"json"结尾，TXT格式的文件应以"txt"结尾。
    
    Returns:
        int: 返回一个整数，分别表示标注类型如下：
            0 - NX_ANNOTATION_TYPE_DET（目标检测）；
            1 - NX_ANNOTATION_TYPE_SEG（语义分割）；
            2 - NX_ANNOTATION_TYPE_ASR（语音识别）；
            3 - NX_ANNOTATION_TYPE_OCR（光学字符识别）。
    
        Raises:
            ValueError: 当文件名不是JSON或TXT格式时，会引发此错误。
    """
    if name.split('/')[-1].endswith('json'):
        return NX_ANNOTATION_TYPE_DET
    elif name.split('/')[-1].endswith('txt'):
        return _get_txt_annotation_type(name)
    else:
        raise ValueError("do NOT support annotation {}".format(name))
    
def _guess_algorith_annotation_type(annotation_path):
    """
    根据注释路径猜测算法注释类型，如果是文件则返回文件注释类型，否则返回None。
    如果注释路径为文件且存在于'train'或'val'目录下，则返回第一个找到的文件注释类型。
    
    Args:
        annotation_path (str): 注释路径，可以是文件或者目录。
    
    Returns:
        str, None: 如果注释路径是文件，返回文件注释类型；如果注释路径是目录，返回None。
    
    Raises:
        ValueError: 当注释路径不支持时，会引发ValueError异常。
    """
    if os.path.isfile(annotation_path):
        # file
        return _get_file_annotation_type(annotation_path)
    else:
        # folder
        for p in ['train', 'val', 'annotation']:
            names = _retrive_path(annotation_path, ['json', 'txt'], p, p)
            if len(names) > 0:
                return _get_file_annotation_type(names[0])
    raise ValueError("do NOT support annotation {}".format(annotation_path)) 

def get_annotation_type(label_description_path):
    """
    根据 label_description 获取标签类型

    Args:
        label_description_path (str): 标签描述文件路径
    
    Returns:
        str: 标签类型
    """

    try:
        with open(label_description_path) as f:
            label_description = yaml.safe_load(f)
    except Exception as e:
        bcelogger.warning(f"解析 label_description 失败: {e}")
        return ''
    
    # 获取 label_description 的所有 task_type
    all_task_type = [item['task_type'] for item in label_description['tasks']]
    if 'detection' in all_task_type:
        return NX_ANNOTATION_TYPE_DET
    elif 'semantic_segmentation' in all_task_type:
        return NX_ANNOTATION_TYPE_SEMANTIC_SEG
    elif 'instance_segmentation' in all_task_type:
        return NX_ANNOTATION_TYPE_INSTANCE_SEG
    elif 'image_classification' in all_task_type:
        return NX_ANNOTATION_TYPE_CLS
    else:
        return ''
            
def _modify_annotation(src_name, dst_path, abs_work_path, all_image_folders, s3_filesystem_head, local_filesystem_head):
    """
    根据源文件名修改对应的标注信息，返回修改后的标注文件路径或None。
    
    Args:
        src_name (str): 源文件名，包括扩展名。
        dst_path (str): 目标标注文件保存路径，不包括扩展名。
        abs_work_path (str): 绝对工作路径，用于生成新的标注文件名。
        all_image_folders (set[str]): 所有参与训练的图像文件夹集合
    
    Returns:
        str or None: 如果修改成功，返回修改后的标注文件路径；否则返回None。
    """

    # 通过提前 os.listdir() 预先缓存所有文件夹，避免后续的 os.listdir() 耗时
    bcelogger.info(f"预先 os.listdir() 以加速数据集准备部分时间")
    default_prefix = 'images'
    abs_work_folders = os.listdir(abs_work_path) if os.path.exists(abs_work_path) else []
    abs_work_default_path = os.path.join(abs_work_path, default_prefix)
    abs_work_default_folders = (
            os.listdir(abs_work_default_path) if os.path.exists(abs_work_default_path) else [])
    
    annotation_type = _guess_algorith_annotation_type(src_name)
    if annotation_type == NX_ANNOTATION_TYPE_DET or annotation_type == NX_ANNOTATION_TYPE_INSTANCE_SEG:
        return _modify_detection_annotations(
                src_name, dst_path, abs_work_path, abs_work_folders, abs_work_default_folders, all_image_folders, 
                s3_filesystem_head=s3_filesystem_head, local_filesystem_head=local_filesystem_head)
    elif annotation_type == NX_ANNOTATION_TYPE_CLS:
        return _modify_classify_annotations(
                src_name, dst_path, abs_work_path, abs_work_folders, abs_work_default_folders, all_image_folders, 
                s3_filesystem_head=s3_filesystem_head, local_filesystem_head=local_filesystem_head)
    elif annotation_type == NX_ANNOTATION_TYPE_SEMANTIC_SEG:
        return _modify_segment_annotations(src_name, dst_path, abs_work_path, 
                s3_filesystem_head=s3_filesystem_head, local_filesystem_head=local_filesystem_head)
    else:
        return None

def pre_listdir_folders(all_image_folders):
    """通过 os.listdir() 预先缓存所有文件夹，避免后续的 os.listdir() 耗时
    
    Args:
        all_image_folders (set[str]): 所有参与训练的图像文件夹集合
    """
    done_folders = set()
    for image_folder_path in all_image_folders:
        current_path = '/'
        for item in image_folder_path.split('/'):
            current_path = os.path.join(current_path, item)
            if current_path not in done_folders:
                
                try:
                    os.listdir(current_path)
                except Exception as e:
                    bcelogger.info(f"Exception occurred while listing directory: {e}")
                
                done_folders.add(current_path)
                bcelogger.info(f"warm up folder: {current_path}")
            # else pass


def generate_label_description(input_base, anno_path, save_root):
    """
    根据 input_base 和数据标签自动生成 label_description.yaml 文件

    Args:
        input_base (str): base 模型，支持中文名称和标准化的类名
        anno_path (str): 标注文件路径
        save_root (str): 保存路径
    
    Returns:
        file_path (str): 生成的文件路径
    """

    if input_base in ['实例分割-标准版', 'StandardizeModelPpyoloeseg']:
        label_description = generate_instance_segmentation_coco(anno_path)
    else:
        bcelogger.error('unsupported model type:{}'.format(input_base))
        return ''
    
    if not label_description:
        bcelogger.error('generate label description failed. see above error message.')
        return ''
    
    file_path = os.path.join(save_root, 'label_description.yaml')
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(label_description, f)
    
    return file_path


def generate_instance_segmentation_coco(anno_path):
    """
    生成实例分割 COCO 标签描述字典

    Args:
        anno_path (str): 标注文件路径
    
    Returns:
        dict: 标签描述字典
    """

    # anno_path 检查是否存在
    if not os.path.exists(anno_path):
        bcelogger.error('annotation path {} does not exist.'.format(anno_path))
        return None
    
    # 加载标签文件
    with open(anno_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成 label_description
    label_description = {
        'tasks': [{
            'task_type': 'instance_segmentation',
            'task_name': '实例分割',
            'anno_key': 1,
            'categories': {}
        }]
    }

    # 生成标签和含义的对照表
    for item in data['categories']:
        label_description['tasks'][0]['categories'][str(item['id'])] = item['name']

    return label_description

def is_rle_segmentation(json_path):
    
    """
    judge rle segmentation
    """
    if not os.path.exists(json_path):
        return False
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    is_rle = False
    try:
        # 遍历 annotations 并转换 segmentation
        for annotation in data['annotations']:
            if 'segmentation' in annotation:
                segmentation = annotation['segmentation']
                if isinstance(segmentation, dict) and 'counts' in segmentation:
                    is_rle = True
                    break
    except Exception as e:
        bcelogger.error(f"Error judge rle segmentation: {e}")
    return is_rle

def rle_to_polygon(json_path, min_area=5):
    """
    将RLE格式的掩码转换为多边形表示。
    :param json_path: 修改JSON文件路径
    :param min_area: 最小面积，小于此值的多边形将被过滤
    """
    if is_rle_segmentation(json_path) is False:
        return 
    with open(json_path, 'r') as f:
        data = json.load(f)

    import cv2
    from pycocotools import mask
    try:
        # 遍历 annotations 并转换 segmentation
        for annotation in data['annotations']:
            segmentation = annotation['segmentation']
            if isinstance(segmentation, dict) and 'counts' in segmentation:
                # 如果是RLE格式，转换为多边形
                rle_mask = segmentation
                
                # Check if 'size' and 'counts' fields are present
                if 'size' in rle_mask:
                    height, width = rle_mask['size']
                else:
                    raise ValueError("RLE mask should contain 'size' field")
                
                if 'counts' in rle_mask and type(rle_mask['counts']) == list:
                    rle_mask = mask.frPyObjects(rle_mask, height, width)
                else:
                    raise ValueError("RLE mask should contain 'counts' field as list")
                
                # Decode RLE to binary mask
                binary_mask = mask.decode(rle_mask).squeeze()
                # Find contours in the binary mask
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                polygons = []
                for contour in contours:
                    # Filter small areas and flatten contour points to polygon
                    if cv2.contourArea(contour) >= min_area:
                        polygon = contour.flatten().tolist()
                        if len(polygon) > 4:  # 至少需要2个点构成多边形
                            polygons.append(polygon)              
                annotation['segmentation'] = polygons
            else:
                # 如果不是RLE格式，跳过
                bcelogger.info(f"Not rle segmentation")
    except Exception as e:
        bcelogger.error(f"Error converting segmentation: {e}")
    
    # 保存结果到新文件
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    bcelogger.info(f"convert rle2polygon {json_path}")