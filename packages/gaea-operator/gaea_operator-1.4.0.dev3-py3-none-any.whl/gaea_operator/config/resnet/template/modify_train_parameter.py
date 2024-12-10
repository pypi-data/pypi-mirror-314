# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify input train parameter yaml
Authors: wanggaofei(wanggaofei03@baidu.com)
Date:    2023-02-29
"""

import json
import os
import yaml
import argparse
import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE

KEY_EPOCH = 'Global.epochs'
KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_WIDTH = 'eval_width'
KEY_GLOBAL = 'Global'
KEY_IMAGE_SHAPE = 'image_shape'
KEY_DATALOADER = 'DataLoader'
KEY_TRAIN = 'Train'
KEY_DATASET = 'dataset'
KEY_TRANSFORM_OPS = 'transform_ops'
KEY_RESIZE_IMAGE = 'ResizeImage'
KEY_SIZE = 'size'
KEY_EVAL = 'Eval'
KEY_ARCH_NAME = 'Arch.name'
KEY_SAVE_INTERVAL = 'save_interval'
KEY_EVAL_INTERVAL = 'eval_interval'
KEY_TRAIN_NUM_WORKERS = 'DataLoader.Train.loader.num_workers'
KEY_TRAIN_BATCH_SIZE = 'DataLoader.Train.sampler.batch_size'
KEY_PRETRAINED_MODEL = 'Global.pretrained_model'
KEY_NORMALIZE_IMAGE = 'NormalizeImage'
KEY_RESNET = 'resnet'
# "https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/legendary_models/ResNet18_pretrained.pdparams",
PRETRAINED_MODEL_NAME_RESNET = 'ResNet18_pretrained'


def get_yaml(yaml_name):
    """
    读取指定YAML文件，并返回解析后的数据。如果读取失败，则返回None。
    
    Args:
        yaml_name (str): YAML文件的路径名。
    
    Returns:
        dict, optional: 返回一个字典类型，包含YAML文件中的内容；如果读取失败，则返回None。
    """
    with open(yaml_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
        return yaml_data
    return None


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


def convert_value_type(val):
    """
        convert string to real data type
    """
    if val.isdigit():
        return int(val)
    elif val.replace('.', '', 1).isdigit():
        return float(val)
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


def set_epoch(yaml_data, val):
    """
    set epoch
    """
    if KEY_GLOBAL in yaml_data:
        set_multi_key_value(yaml_data, KEY_EPOCH, str(val))

        save_interval = get_value(yaml_data[KEY_GLOBAL], KEY_SAVE_INTERVAL)
        if save_interval is None or int(save_interval) > int(val):
            set_value(yaml_data[KEY_GLOBAL], KEY_SAVE_INTERVAL, val)
            bcelogger.info('modify {}: {} -> {}'.format(KEY_SAVE_INTERVAL, save_interval, val))

        eval_interval = get_value(yaml_data[KEY_GLOBAL], KEY_EVAL_INTERVAL)
        if eval_interval is None or int(eval_interval) > int(val):
            set_value(yaml_data[KEY_GLOBAL], KEY_EVAL_INTERVAL, val)
            bcelogger.info('modify {}: {} -> {}'.format(KEY_EVAL_INTERVAL, eval_interval, val))
    else:
        bcelogger.error('do NOT find key: {}'.format(KEY_GLOBAL))


def set_target_size(yaml_data, eval_width, eval_height):
    """
    设置目标大小，如果不支持该大小则报错。
    如果配置文件中存在train reader和batch transforms，并且包含batch random resize，则修改其target size为指定的大小。
    
    Args:
        yaml_data (dict): YAML格式的数据字典，包含train reader和batch transforms等信息。
        eval_width (int): 评估图像的宽度。
        eval_height (int): 评估图像的高度。
    
    Returns:
        None.
    
    Raises:
        ValueError: 如果不支持指定的目标大小。
    """
    cwh_list = [3, int(eval_height), int(eval_width)]
    if KEY_GLOBAL in yaml_data:
        set_value(yaml_data[KEY_GLOBAL], KEY_IMAGE_SHAPE, cwh_list)

    wh_list = [int(eval_height), int(eval_width)]
    if KEY_DATALOADER in yaml_data and KEY_TRAIN in yaml_data[KEY_DATALOADER] \
            and KEY_DATASET in yaml_data[KEY_DATALOADER][KEY_TRAIN] \
            and KEY_TRANSFORM_OPS in yaml_data[KEY_DATALOADER][KEY_TRAIN][KEY_DATASET]:
        for i in range(len(yaml_data[KEY_DATALOADER][KEY_TRAIN][KEY_DATASET][KEY_TRANSFORM_OPS])):
            if KEY_RESIZE_IMAGE in yaml_data[KEY_DATALOADER][KEY_TRAIN][KEY_DATASET][KEY_TRANSFORM_OPS][i]:
                set_value(yaml_data[KEY_DATALOADER][KEY_TRAIN][KEY_DATASET][KEY_TRANSFORM_OPS][i][KEY_RESIZE_IMAGE],
                          KEY_SIZE, wh_list)
                bcelogger.info('set {}.{}.{}.{} size: {}'.format(KEY_DATALOADER, KEY_TRAIN,
                                                                 KEY_DATASET, KEY_TRANSFORM_OPS, wh_list))

    if KEY_DATALOADER in yaml_data and KEY_EVAL in yaml_data[KEY_DATALOADER] \
            and KEY_DATASET in yaml_data[KEY_DATALOADER][KEY_EVAL] \
            and KEY_TRANSFORM_OPS in yaml_data[KEY_DATALOADER][KEY_EVAL][KEY_DATASET]:
        for i in range(len(yaml_data[KEY_DATALOADER][KEY_EVAL][KEY_DATASET][KEY_TRANSFORM_OPS])):
            if KEY_RESIZE_IMAGE in yaml_data[KEY_DATALOADER][KEY_EVAL][KEY_DATASET][KEY_TRANSFORM_OPS][i]:
                set_value(yaml_data[KEY_DATALOADER][KEY_EVAL][KEY_DATASET][KEY_TRANSFORM_OPS][i][KEY_RESIZE_IMAGE],
                          KEY_SIZE, wh_list)
                bcelogger.info('set {}.{}.{}.{} size: {}'.format(KEY_EVAL, KEY_DATASET,
                                                                 KEY_TRANSFORM_OPS, KEY_RESIZE_IMAGE, wh_list))


def get_pretrained_model_name(pretrained_model_path):
    """
        get pretrained model absolute path
    """
    for filepath in os.listdir(pretrained_model_path):
        if filepath.endswith('.pdparams'):
            bcelogger.info('find pretrained pth file: {}'.format(filepath))
            return os.path.join(pretrained_model_path, os.path.splitext(filepath)[0])
    return None


def get_mean_std(yaml_data):
    """
        get train mean/std
    """
    transform_ops = yaml_data[KEY_DATALOADER][KEY_TRAIN][KEY_DATASET][KEY_TRANSFORM_OPS]
    for _, v in enumerate(transform_ops):
        if KEY_NORMALIZE_IMAGE in v:
            return v[KEY_NORMALIZE_IMAGE]['mean'], v[KEY_NORMALIZE_IMAGE]['std']
    return [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]


def generate_train_config(
        advanced_parameters: dict,
        train_config_name: str
):
    """
        modify parameter by template config
    """
    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parameter.yaml')
    yaml_data = get_yaml(input_yaml_name)
    mean, std = get_mean_std(yaml_data)

    # 更新mean std
    advanced_parameters.update({'mean': f'{mean}', 'std': f'{std}'})

    # 1. set correlative parameters
    correlative_parameter_keys = [KEY_EVAL_WIDTH, KEY_EVAL_HEIGHT, KEY_EPOCH, KEY_NETWORK_ARCHITECTURE]
    # 1.1 target size
    set_target_size(yaml_data, advanced_parameters[KEY_EVAL_WIDTH], advanced_parameters[KEY_EVAL_HEIGHT])

    # 1.2 epoch
    set_epoch(yaml_data, int(advanced_parameters[KEY_EPOCH]))

    # 1.3 network architecture，默认 ResNet18
    advanced_parameters[KEY_ARCH_NAME] = 'ResNet18'
    if advanced_parameters[KEY_NETWORK_ARCHITECTURE].endswith('18'):
        advanced_parameters[KEY_ARCH_NAME] = 'ResNet18'
    if advanced_parameters[KEY_NETWORK_ARCHITECTURE].endswith('50'):
        advanced_parameters[KEY_ARCH_NAME] = 'ResNet50'

    # 2. set get-though parameters by key-value of dict
    shadow_parameters = [KEY_TRAIN_NUM_WORKERS, KEY_TRAIN_BATCH_SIZE]
    for key, val in advanced_parameters.items():
        if key not in correlative_parameter_keys:
            if KEY_PRETRAINED_MODEL == key:
                val = get_pretrained_model_name(advanced_parameters[KEY_PRETRAINED_MODEL])
            set_multi_key_value(yaml_data, key, val)
            if key in shadow_parameters:
                set_multi_key_value(yaml_data, key.replace('Train', 'Eval'), val)

    bcelogger.info('begin to save yaml. {}'.format(train_config_name))
    save_yaml(yaml_data, train_config_name)
    bcelogger.info('write train config finish.')


def parse_opt():
    """ parser opt
        Args:

        Returns:
            opt -- command line parameter
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--advanced_parameters', type=str, default="", help='train parameter dict')
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
    from bcelogger.base_logger import setup_logger

    opt = parse_opt()
    setup_logger(config=dict(file_name=os.path.join('/ssd2/lyg/GAEA-PIPE/resnet18', "worker.log")))
    # labels: [{'name':, 'id': }, ...]
    labels = json.load(open('/ssd2/lyg/Dataset/zhiguan_clas/labels.json', "r"))
    advanced_parameters = {'Global.epochs': '1', 'Optimizer.lr.learning_rate': '0.001', \
                           'DataLoader.Train.loader.num_workers': '2', 'eval_height': '256', 'eval_width': '256', \
                           'DataLoader.Train.sampler.batch_size': '8', 'model_type': 'resnet'}
    opt.train_config_name = '/ssd2/lyg/GAEA-PIPE/resnet18/train_config.yaml'
    generate_train_config(advanced_parameters=advanced_parameters,
                          labels=labels, train_config_name=opt.train_config_name)
