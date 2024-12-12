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
import os
import yaml
import argparse

import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE

KEY_EPOCH = 'epoch'
KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_WIDTH = 'eval_width'
KEY_EVAL_SIZE = 'eval_size'
KEY_PRETRAIN_WEIGHTS = 'pretrain_weights'
KEY_DEPTH_MULT = 'depth_mult'
KEY_WIDTH_MULT = 'width_mult'
KEY_SNAPSHOT_EPOCH = 'snapshot_epoch'
KEY_LEARNING_RATE = 'LearningRate'
KEY_SCHEDULERS = 'schedulers'
KEY_MAX_EPOCHS = 'max_epochs'
KEY_TRAIN_READER = 'TrainReader'
KEY_BATCH_TRANSFORMS = 'batch_transforms'
KEY_BATCH_RANDOM_RESIZE = 'BatchRandomResize'
KEY_TARGET_SIZE = 'target_size'
KEY_TRAIN_BATCH_SIZE = 'TrainReader.batch_size'
KEY_EVAL_BATCH_SIZE = 'EvalReader.batch_size'

def get_target_size(src: str) -> dict:
    """
    获取原始图片大小，生成resize尺寸。
    
    Args:
        src (str): 原始图像尺寸。
    
    Returns:
        target_size_map (dict): anchor列表。

    Example:
        >>> target_size_map = get_target_size('320,320')
        >>> {'320,320': '[192, 224, 256, 288, 320, 352, 384, 416, 448]'}
    """
    target_size_map = {}
    target_size = src
    

    if not isinstance(target_size, str):
        raise ValueError('--target_size must be a string in the format "width,height"')
    width, height = map(int, target_size.split(','))
    if width % 32 or height % 32:
        raise ValueError('--target_size must be multiple of 32')
    if width == 0 or height == 0:
        raise ValueError('--target_size must be positive')
    
    if src in TARGET_SIZE_MAP:
        result = TARGET_SIZE_MAP[src]
        target_size_map[src] = result
    else:
        result = []
        if width != height:
            cur = [height // 32, width // 32] 
            right = [item + 5 for item in cur]
            left = [item - 10 for item in cur]

            min_left = min(left)
           
            if min_left <= 0:
                left = [i - min_left + 1 for i in left]
               

            left_result = [item * 32 for item in range(left[0], right[0])]
            right_result = [item * 32 for item in range(left[1], right[1])]

            for i, j in zip(left_result, right_result):
                result.append([i, j])


        else:
            cur = width // 32
            right = cur + 4
            left = cur - 20 if cur - 20 > 0 else 1
            result = [item * 32 for item in range(left, right + 1)]

        result = str(result)
        target_size_map[src] = result
    return target_size_map

TARGET_SIZE_MAP = {'320,320': '[192, 224, 256, 288, 320, 352, 384, 416, 448]',
                   '416,416': '[192,224,256,288,320,352,384,416,448,480,512,544]',
                   '640,640': '[320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768]',
                   '960,544': '[[224, 640], [256, 672], [288, 704], [320, 736], [352,768], [384,800], [416, 832], \
                        [448, 864], [480, 896], [512, 928], [544, 960], [576, 992], [608, 1024], \
                            [640, 1056], [672, 1088]]',
                   '1280,736': '[[416, 960], [448, 992], [480, 1024], [512, 1056], [544, 1088], [576, 1120], \
                        [608, 1152], \
                        [640, 1184], [672, 1216], [704, 1248], [736, 1280], [768, 1312], [800, 1344], [832, 1376]]',
                   '960,960': '[320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768, \
                        864, 960, 1056, 1152]'
                   }

PRETRAIN_MODEL_NAMES = { \
    's': ['ppyoloe_crn_s_obj365_pretrained.pdparams', 0.33, 0.50],
    'm': ['ppyoloe_crn_m_obj365_pretrained.pdparams', 0.67, 0.75],
    'l': ['ppyoloe_crn_l_obj365_pretrained.pdparams', 1.0, 1.0],
    'x': ['ppyoloe_crn_x_obj365_pretrained.pdparams', 1.33, 1.25]
}


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


def set_epoch(yaml_data, val):
    """
    设置给定的yaml_data中的epoch值为指定的val。如果原来的epoch值不等于val，则会记录日志。
    此外，如果学习率的scheduler中有max_epochs字段，并且大于当前的epoch值，则会将其修改为当前的epoch值。
    
    Args:
        yaml_data (dict): YAML格式的数据，包含epoch和learning rate相关的信息。
        val (int): 需要设置的epoch值，应该是一个整数。
    
    Returns:
        None; 无返回值，直接修改了yaml_data中的epoch值和learning rate的scheduler中的max_epochs值（如果存在）。
    """
    set_value(yaml_data, KEY_EPOCH, val)
    snapshot_epoch = get_value(yaml_data, KEY_SNAPSHOT_EPOCH)
    if snapshot_epoch is not None and int(snapshot_epoch) > val:
        set_value(yaml_data, KEY_SNAPSHOT_EPOCH, val)
    if KEY_LEARNING_RATE in yaml_data and KEY_SCHEDULERS in yaml_data[KEY_LEARNING_RATE]:
        for i in range(len(yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS])):
            if KEY_MAX_EPOCHS in yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i] and \
                    int(yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i][KEY_MAX_EPOCHS]) > val:
                yaml_data[KEY_LEARNING_RATE][KEY_SCHEDULERS][i][KEY_MAX_EPOCHS] = val
                bcelogger.info('set-epoch modify max_epochs. {}'.format(val))


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


def height_width_str2list(height_width_str):
    """
    字符串转列表
    """
    size_list = []
    s = height_width_str.strip()
    if s[0] == '[' and s[-1] == ']':
        s = s[1: -1].strip()
        if s[0] == '[' and s[-1] == ']':
            # height width independ
            s = s.replace('[', ' ').replace(']', ' ').split(',')
            for i in range(len(s) // 2):
                size_list.append([int(s[i * 2]), int(s[i * 2 + 1])])
        else:
            ws = s.split(',')
            for _, v in enumerate(ws):
                size_list.append(int(v))
    else:
        bcelogger.error('invalid height-width-string. {}'.format(height_width_str))
    return size_list


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
    eval_wh_str = str(eval_width) + ',' + str(eval_height)
    # 支持用户自定义输入target size（32整数倍宽高）
    # if eval_wh_str not in TARGET_SIZE_MAP:
    #     bcelogger.error('do NOT support target size. width: {}, height: {}'.format(eval_width, eval_height))
    # else:
    if KEY_TRAIN_READER in yaml_data and KEY_BATCH_TRANSFORMS in yaml_data[KEY_TRAIN_READER]:
        for _, v in enumerate(yaml_data[KEY_TRAIN_READER][KEY_BATCH_TRANSFORMS]):
            if KEY_BATCH_RANDOM_RESIZE in v and KEY_TARGET_SIZE in v[KEY_BATCH_RANDOM_RESIZE]:
                # v[KEY_BATCH_RANDOM_RESIZE][KEY_TARGET_SIZE] = height_width_str2list(TARGET_SIZE_MAP[eval_wh_str])
                new_size_map = get_target_size(eval_wh_str)
                v[KEY_BATCH_RANDOM_RESIZE][KEY_TARGET_SIZE] = height_width_str2list(new_size_map[eval_wh_str])
                bcelogger.info('set target size: {}'.format(eval_wh_str))


def set_model_type(yaml_data, val, pretrain_model_uri):
    """
    设置模型类型
    """
    model_type = val.strip().split('_')[-1]
    if model_type in PRETRAIN_MODEL_NAMES:
        name, depth_mult, width_mult = PRETRAIN_MODEL_NAMES[model_type]
        set_value(yaml_data, KEY_PRETRAIN_WEIGHTS, os.path.join(pretrain_model_uri, name))
        set_value(yaml_data, KEY_DEPTH_MULT, depth_mult)
        set_value(yaml_data, KEY_WIDTH_MULT, width_mult)
    else:
        bcelogger.error('do NOT known model type value. {}'.format(val))


def generate_train_config(
        advanced_parameters: dict,
        pretrain_model_uri: str,
        train_config_name: str
):
    """
        modify parameter by template config
    """
    # 0. modify width/height var
    width = advanced_parameters[KEY_EVAL_WIDTH]
    height = advanced_parameters[KEY_EVAL_HEIGHT]
    var_name_vals = [[KEY_EVAL_WIDTH, width], [KEY_EVAL_HEIGHT, height]]

    if advanced_parameters[KEY_NETWORK_ARCHITECTURE].startswith('change-'):
        input_yaml_name = 'parameter_c.yaml'
    else:
        input_yaml_name = 'parameter.yaml'

    bcelogger.info('train parameter name: {}'.format(input_yaml_name))

    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_yaml_name)
    yaml_data = modify_var_value(input_yaml_name, var_name_vals)

    # 1. set correlative parameters
    correlative_parameter_keys = [KEY_EVAL_WIDTH, KEY_EVAL_HEIGHT, KEY_EPOCH, KEY_NETWORK_ARCHITECTURE]
    # 1.1 target size
    set_target_size(yaml_data, advanced_parameters[KEY_EVAL_WIDTH], advanced_parameters[KEY_EVAL_HEIGHT])

    # 1.2 epoch
    set_epoch(yaml_data, int(advanced_parameters[KEY_EPOCH]))

    # 1.3 model_type
    set_model_type(yaml_data, advanced_parameters[KEY_NETWORK_ARCHITECTURE], pretrain_model_uri)

    # 2. set get-though parameters by key-value of dict
    for key, val in advanced_parameters.items():
        if key not in correlative_parameter_keys:
            set_multi_key_value(yaml_data, key, val)

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

    generate_train_config(str2dict(opt.advanced_parameters), opt.pretrain_model_uri, opt.train_config_name)
