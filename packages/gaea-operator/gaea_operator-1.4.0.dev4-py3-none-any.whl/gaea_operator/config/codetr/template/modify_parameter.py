# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify input train parameter yaml
Authors: liyinggang
Date:    2023-02-29
"""
import math
import os
import yaml
import argparse

import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE

VAR_KEY_MAX_EPOCHS = "max_epochs"
VAR_KEY_BATCH_SIZE = "batch_size"
VAR_KEY_EVAL_HEIGHT = 'eval_height'
VAR_KEY_EVAL_WIDTH = 'eval_width'
VAR_KEY_DATA_ROOT = "data_root"
VAR_KEY_NUM_CLASSES = "num_classes"
VAR_KEY_TRAIN_ANNO = "train_anno"
VAR_KEY_VAL_ANNO = "val_anno"
KEY_CLASS_NAMES = "class_names"
VAR_KEY_MEAN = "mean"
VAR_KEY_STD = "std"
KEY_CONFIG_TYPE = "config_type"

KEY_LOAD_FROM = 'load_from'
VAL_LOAD_FROM_NAME = 'co_dino_swin_l.pth'
KEY_PRETRAINED = 'pretrained'
KEY_OUTPUT_DIR = 'output_dir'
VAL_PRETRAINED_NAME = 'swin_large_patch4_window12_384_22k.pth'
KEY_PARAM_SCHEDULER = 'param_scheduler'
KEY_TYPE = 'type'
KEY_MILESTONES = 'milestones'
KEY_MULTISTEPLR = "MultiStepLR"
KEY_TRAIN_DATALOADER = 'train_dataloader'
KEY_DATASET = 'dataset'
KEY_PIPELINE = 'pipeline'
KEY_TRANSFROMS = 'transforms'
KEY_SCALES = 'scales'
KEY_CODETR = 'codetr'
KEY_CLASS_NAMES_META = ['metainfo.classes', 'test_dataloader.dataset.metainfo.classes',
                        'train_dataloader.dataset.metainfo.classes',
                        'val_dataloader.dataset.metainfo.classes']
# eval
KEY_TEST_DATA_ROOT = ['data_root', 'test_dataloader.dataset.data_root', 'train_dataloader.dataset.data_root']
KEY_TEST_ANNO_FILES = ['train_dataloader.dataset.ann_file',
                       'test_dataloader.dataset.ann_file',
                       'test_evaluator.ann_file']
# deploy
KEY_SCORE_THRESH = 'score_thresh'
KEY_IOU_THRESH = 'iou_thresh'
DEPLOY_KEY_SCORE_THRESHOLD = 'codebase_config.post_processing.score_threshold'
DEPLOY_KEY_IOU_THRESHOLD = 'codebase_config.post_processing.iou_threshold'
DEPLOY_KEY_DEPLOY_INPUT_SHAPE = 'onnx_config.input_shape'

IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)


def get_yaml(yaml_name):
    """
    读取指定YAML文件，并返回解析后的数据。如果读取失败，则返回None。
    
    Args:
        yaml_name (str): YAML文件的路径名。
    
    Returns:
        dict, optional: 返回一个字典类型，包含YAML文件中的内容；如果读取失败，则返回None。
    """
    if os.path.exists(yaml_name):
        with open(yaml_name) as f:
            yaml_data = yaml.load(f, Loader=yaml.Loader)
            return yaml_data
    return {}


def save_yaml(yaml_data, yaml_name):
    """
    将字典数据保存为YAML格式的文件。
    
    Args:
        yaml_data (dict): 需要保存的字典数据。
        yaml_name (str): YAML文件名，包含路径。
    
    Returns:
        None; 无返回值，直接写入文件。
    """
    with open(yaml_name, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)


def set_value(yaml_data, key, val):
    """
    设置YAML数据中指定键的值，如果该键不存在则添加。如果键已经存在，将更新其值；否则，将添加一个新的键-值对。
    如果键不存在，将输出错误日志。
    
    Args:
        yaml_data (dict): YAML格式的数据，类型为字典，用于存储和修改键值对。
        key (str): 需要设置或添加的键名，类型为字符串。
        val (any): 需要设置或添加的键值，任意类型。
    
    Returns:
        None - 无返回值，直接修改传入的yamldata参数。
    
    Raises:
        None - 该函数没有引发任何异常。
    """
    if key in yaml_data:
        bcelogger.info('old val. {} -> {}'.format(key, yaml_data[key]))
        yaml_data[key] = val
        bcelogger.info('new val. {} -> {}'.format(key, yaml_data[key]))
    else:
        bcelogger.error('do NOT find key: {}'.format(key))


def get_value(yaml_data, key):
    """
    根据指定的键值获取对应的值，如果找不到则返回None。
    
    Args:
        yaml_data (dict): YAML格式的数据字典。
        key (str): 需要查询的键值。
    
    Returns:
        Union[str, int, dict, list, None]: 如果找到该键值，则返回对应的值；否则返回None。
    """
    if key in yaml_data:
        return yaml_data[key]
    else:
        bcelogger.info('do NOT find key: {}'.format(key))
        return None


def process_var(line, var_name, val):
    """
    处理变量
    """
    l = line.strip().split()
    if len(l) != 3:
        return line, False
    else:
        if str(l[0]) == var_name + ':' and str(l[1]) == '&' + var_name:
            return line.replace(l[-1], str(val)), True
        else:
            return line, False


def modify_var_value(yaml_name, var_name_vals):
    """
    处理变量
    """
    lines = []
    new_lines = []
    with open(yaml_name) as f:
        lines = f.readlines()
    for _, v in enumerate(lines):
        find = False
        for var_name, val in var_name_vals:
            if var_name in v:
                new_l, find = process_var(v, var_name, val)
                if find:
                    new_lines.append(new_l)
                    break

        if not find:
            new_lines.append(v)
    tmp_name = '/root/yaml_tmp.yaml'
    with open(tmp_name, 'w') as f:
        for _, n in enumerate(new_lines):
            f.write(n)
    with open(tmp_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
    return yaml_data


def convert_value_type(val):
    """
        convert string to real data type
    """
    if isinstance(val, str):
        if val.isdigit():
            return int(val)
        elif val.replace('.', '', 1).isdigit():
            return float(val)
        else:
            return val
    else:
        return val


def set_multi_key_value(yaml_data, multi_key, val):
    """
        set all do not care parameter
    """
    keys = multi_key.split('.')
    config_dict = yaml_data
    for i, key in enumerate(keys):
        if key in config_dict:
            if i + 1 == len(keys):
                config_dict[key] = convert_value_type(val)
            else:
                config_dict = config_dict[key]
        else:
            bcelogger.error('do NOT find key: {} of {}'.format(key, multi_key))
            break

# def set_transform_multi_scales(yaml_data, base_width: int, base_height: int):
def set_transform_multi_scales(yaml_data, base_width: int, base_height: int, keep_ratio=False):
    # """
    #     为transform生成多尺度分别率，其中下限 减少比例为0.5，上限增加比例为1.25(考虑训练显存）
    # """
    # min_width = math.ceil((base_width - base_width * 0.5) / 32) * 32
    # max_width = math.floor((base_width + base_width * 0.25) / 32) * 32
    # min_height = math.ceil((base_height - base_height * 0.5) / 32) * 32
    # max_height = math.floor((base_height + base_height * 0.25) / 32) * 32

    # scales = []
    # # step必须为32整数倍
    # for width in range(min_width, max_width + 1, 32):
    #     for height in range(min_height, max_height + 1, 32):
    #         scales.append((width, height))
    """
    生成多尺度scales方式有所变动
    新需求：scales与图像大小联动自动生成，
    scales_upper取max(eval_height,eval_width,480)（其中480为默认值，与eval_height,eval_width对比筛选出最长边，然后生成列表：
    """
    scales = [(math.ceil(i / 32) * 32, math.ceil(max(base_width, base_height, 480) / 32) * 32) 
               for i in range(min(base_width, base_height, 480), max(base_width, base_height, 480) + 1, 32)]

    if KEY_TRAIN_DATALOADER in yaml_data and KEY_DATASET in yaml_data[KEY_TRAIN_DATALOADER] \
            and KEY_PIPELINE in yaml_data[KEY_TRAIN_DATALOADER][KEY_DATASET]:
        for ppl in yaml_data[KEY_TRAIN_DATALOADER][KEY_DATASET][KEY_PIPELINE]:
            if ppl["type"] == "RandomChoice" and 'transforms' in ppl:
                for choices in ppl['transforms']:
                    for choice in choices:
                        if choice['type'] == "RandomChoiceResize":
                            choice['scales'] = scales
                            choice['keep_ratio'] = keep_ratio


def set_transform_whether_contain_rotatekangtuo(yaml_data, contain_rotatekangtuo=True):
    """    
    判断是否包含RotateKangtuo，默认包含，如果不包含，则进行去除
    train_dataloader.dataset.pipeline.transforms.RotateKangtuo  
    """
    if contain_rotatekangtuo:
        bcelogger.info('set contain_rotatekangtuo to True')
        return  # 默认为True，不需要去除RotateKangtuo
    if KEY_TRAIN_DATALOADER in yaml_data and KEY_DATASET in yaml_data[KEY_TRAIN_DATALOADER] \
            and KEY_PIPELINE in yaml_data[KEY_TRAIN_DATALOADER][KEY_DATASET]:
        for ppl in yaml_data[KEY_TRAIN_DATALOADER][KEY_DATASET][KEY_PIPELINE]:
            if ppl["type"] == "RandomChoice" and 'transforms' in ppl:
                for index, choices in enumerate(ppl["transforms"]):
                    # 使用列表推导式生成新choices，过滤掉类型为RotateKangtuo的元素，避免直接remove/del会导致列表长度变化部分RotateKangtuo没有删除的问题
                    # choices = [
                    #     choice for choice in choices if choice["type"] != "RotateKangtuo"
                    # ]  # bug: 不能直接为choices赋值，choices与原来的choices不是同一个对象--无法改变yaml_data
                    ppl["transforms"][index] = [
                        choice for choice in choices if choice["type"] != "RotateKangtuo"
                    ]  # OK
                    bcelogger.info('remove RotateKangtuo')

def set_schedule_step(yaml_data, max_epochs: int):
    """
        set scheduler step
    """
    half_epochs = max(1, max_epochs // 2)
    if KEY_PARAM_SCHEDULER in yaml_data:
        for scheduler in yaml_data[KEY_PARAM_SCHEDULER]:
            if KEY_MULTISTEPLR == scheduler[KEY_TYPE]:
                scheduler[KEY_MILESTONES] = [half_epochs]
                bcelogger.info('set scheduler milestones to: {}'.format(scheduler[KEY_MILESTONES]))


def set_class_names(yaml_data, class_names: list):
    """
    设置yaml数据中的类别名称。
    
    Args:
        yaml_data (dict): 包含类别名称信息的yaml数据。
        class_names (list): 类别名称列表。
    
    Returns:
        None
    
    """
    for multi_key in KEY_CLASS_NAMES_META:
        set_multi_key_value(yaml_data, multi_key, class_names)


def get_pretrained_model_name(pretrained_model_path):
    """
        get pretrained model absolute path
    """
    pths = []
    for filepath in os.listdir(pretrained_model_path):
        if filepath.endswith('.pth'):
            bcelogger.info('find pth file: {}'.format(filepath))
            pths.append(os.path.join(pretrained_model_path, filepath))
    return pths


def _get_pth_file(pths: list, name: str):
    """
        get pth file from uri path
    """
    for _, pth in enumerate(pths):
        if name == pth.split('/')[-1]:
            bcelogger.info('pth: {}'.format(pth))
            return pth
    return None

def generate_train_config(
        advanced_parameters: dict,
        pretrain_model_uri: str,
        train_config_name: str
):
    """
        modify parameter by template config
    """
    # 0. list var parameters
    width = advanced_parameters[VAR_KEY_EVAL_WIDTH]
    height = advanced_parameters[VAR_KEY_EVAL_HEIGHT]
    max_epochs = advanced_parameters[VAR_KEY_MAX_EPOCHS]
    batch_size = advanced_parameters[VAR_KEY_BATCH_SIZE]
    data_root = advanced_parameters[VAR_KEY_DATA_ROOT]
    num_lcasses = advanced_parameters[VAR_KEY_NUM_CLASSES]

    local_model_uris = get_pretrained_model_name(pretrain_model_uri)
    bcelogger.info('pretrained model path: {}'.format(local_model_uris))

    var_name_vals = [[VAR_KEY_EVAL_WIDTH, width], [VAR_KEY_EVAL_HEIGHT, height],
                     [VAR_KEY_MAX_EPOCHS, max_epochs], [VAR_KEY_BATCH_SIZE, batch_size],
                     [VAR_KEY_DATA_ROOT, data_root], [VAR_KEY_NUM_CLASSES, num_lcasses],
                     [VAR_KEY_TRAIN_ANNO, os.path.join(data_root, 'train.json')],
                     [VAR_KEY_VAL_ANNO, os.path.join(data_root, 'val.json')],
                     [KEY_PRETRAINED, _get_pth_file(local_model_uris, VAL_PRETRAINED_NAME)],
                     [KEY_OUTPUT_DIR, os.path.dirname(train_config_name)]]

    input_yaml_name = 'train_parameter.yaml'

    bcelogger.info('use the optimized config. train parameter name: {}'.format(input_yaml_name))

    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_yaml_name)
    yaml_data = modify_var_value(input_yaml_name, var_name_vals)

    # 1. set scheduler step
    set_schedule_step(yaml_data, int(max_epochs))

    # 2. set transform multi scales
    set_transform_multi_scales(
        yaml_data,
        int(width),
        int(height),
        keep_ratio=(
            advanced_parameters[
                "train_dataloader.dataset.pipeline.transforms.RandomChoiceResize.keep_ratio"
            ]
            if advanced_parameters.get(
                "train_dataloader.dataset.pipeline.transforms.RandomChoiceResize.keep_ratio",
                None,
            )
            is not None
            else False
        ),
    )  # 默认为False

    # 3. set train_dataloader.dataset.pipeline.transforms.RotateKangtuo True or False
    set_transform_whether_contain_rotatekangtuo(
        yaml_data,
        contain_rotatekangtuo=(
            advanced_parameters[
                "train_dataloader.dataset.pipeline.transforms.RotateKangtuo"
            ]
            if advanced_parameters.get(
                "train_dataloader.dataset.pipeline.transforms.RotateKangtuo", None
            )
            is not None
            else True
        ),
    )  # 默认为True

    # 4. set class names meta info
    set_class_names(yaml_data, advanced_parameters[KEY_CLASS_NAMES])
    bcelogger.info('set class names: {}'.format(advanced_parameters[KEY_CLASS_NAMES]))

    # 5. set pretrained load from
    set_multi_key_value(yaml_data, KEY_LOAD_FROM, _get_pth_file(local_model_uris, VAL_LOAD_FROM_NAME))

    additional_parameter_keys = []
    # 对特定参数已进行特殊处理(not in)
    # additional_parameter_keys = ["train_dataloader.dataset.pipeline.transforms.RandomChoiceResize.keep_ratio", 
    #                              "train_dataloader.dataset.pipeline.transforms.RotateKangtuo"]
    # -1. set get-though parameters by key-value of dict
    for key, val in advanced_parameters.items():
        if key in additional_parameter_keys:
            set_multi_key_value(yaml_data, key, val)

    bcelogger.info('begin to save yaml. {}'.format(train_config_name))
    save_yaml(yaml_data, train_config_name)
    bcelogger.info('write train config finish.')


def generate_deploy_config(advanced_parameters: dict, deploy_config_name: str):
    """
        modify parameter by template config
    """
    input_yaml_name = 'deploy_parameter.yaml'
    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_yaml_name)
    bcelogger.info('deploy parameter name: {}'.format(input_yaml_name))
    with open(input_yaml_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
        set_multi_key_value(
            yaml_data,
            DEPLOY_KEY_SCORE_THRESHOLD,
            (
                advanced_parameters[KEY_SCORE_THRESH]
                if KEY_SCORE_THRESH in advanced_parameters
                else 0.001
            ),
        )
        set_multi_key_value(
            yaml_data,
            DEPLOY_KEY_IOU_THRESHOLD,
            (
                advanced_parameters[KEY_IOU_THRESH]
                if KEY_IOU_THRESH in advanced_parameters
                else 0.5
            ),
        )
        set_multi_key_value(
            yaml_data,
            DEPLOY_KEY_DEPLOY_INPUT_SHAPE,
            [
                int(advanced_parameters[VAR_KEY_EVAL_WIDTH]),
                int(advanced_parameters[VAR_KEY_EVAL_HEIGHT]),
            ],
        )

    bcelogger.info('begin to save yaml. {}'.format(deploy_config_name))
    save_yaml(yaml_data, deploy_config_name)
    bcelogger.info('write deploy config finish.')


def modify_eval_config(config_data: dict, params: list):
    """
    params: [[data_root, '/ssd2/lyg/Dataset/wgisd_dataset'], [...]]
    """
    for _, v in enumerate(params):
        key = v[0]
        val = v[1]
        if key in config_data:
            if key == VAR_KEY_DATA_ROOT:
                for anno_root in KEY_TEST_DATA_ROOT:
                    set_multi_key_value(config_data, anno_root, val)
            if key == VAR_KEY_VAL_ANNO:
                for test_anno_file in KEY_TEST_ANNO_FILES:
                    set_multi_key_value(config_data, test_anno_file, val)


def parse_opt():
    """ parser opt
        Args:

        Returns:
            opt -- command line parameter
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--advanced_parameters', type=str, default="", help='train parameter dict')
    parser.add_argument('--pretrain_model_uri', type=str, default="", help='pretrain model path')
    parser.add_argument('--train_config_name', type=str, default="", help='output train config file name')
    option = parser.parse_args()
    return option


def str2dict(str):
    """
        demo use only
    """
    s = str.split(',')
    param_dict = {}
    for _, v in enumerate(s):
        kv = v.split(':')
        param_dict[kv[0]] = kv[1]
    return param_dict


if __name__ == "__main__":
    opt = parse_opt()
    bcelogger.info("args: {}".format(opt))
    advanced_parameters = {
        'batch_size': '1',
        'data_root': '/ssd2/lyg/Dataset/wgisd_dataset',
        'eval_height': '224',
        'eval_width': '224',
        'max_epochs': '1',
        'num_classes': '5',
        'class_names': ["Chardonnay", "Cabernet Franc", "Cabernet Sauvignon", "Sauvignon Blanc", "Syrah"],
        'score_thresh': '0.001',
        'iou_thresh': '0.5',
        'extra_augment': 'kangtuo_rotate',
    }
    generate_train_config(advanced_parameters, '/ssd2/lyg/models/co-dino/pretrain', 'gen_train_config.yaml')
    generate_deploy_config(advanced_parameters, 'gen_deploy_config.yaml')
    # generate_train_config(str2dict(opt.advanced_parameters), opt.pretrain_model_uri, opt.train_config_name)
