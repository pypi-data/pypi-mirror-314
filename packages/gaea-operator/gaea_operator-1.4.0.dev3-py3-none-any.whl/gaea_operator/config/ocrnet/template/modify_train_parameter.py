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

KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_WIDTH = 'eval_width'
KEY_TARGET_SIZE = 'target_size'
KEY_MODEL = 'model'
KEY_TRAIN_DATASET = 'train_dataset'
KEY_VAL_DATASET = 'val_dataset'
KEY_TRANSFORMS = 'transforms'
KEY_CROP_SIZE = 'crop_size'
KEY_PRETRAINED = 'model.backbone.pretrained'
KEY_PRETRAINED_TYPE = 'model.backbone.type'
KEY_LOSS_TYPES = 'loss'

# model_type -> [type, name]
MODEL_TYPE_NAME_DICT = {
    'ocrnet': ['HRNet_W18', 'ocrnet_hrnet_w18_ssld.pdparams'],
    'change-ocrnet': ['HRNet_W18', 'ocrnet_hrnet_w18_ssld.pdparams'],
}


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
    wh_list = [int(eval_width), int(eval_height)]
    if KEY_TRAIN_DATASET in yaml_data and KEY_TRANSFORMS in yaml_data[KEY_TRAIN_DATASET]:
        for _, v in enumerate(yaml_data[KEY_TRAIN_DATASET][KEY_TRANSFORMS]):
            if KEY_TARGET_SIZE in v:
                v[KEY_TARGET_SIZE] = wh_list
                bcelogger.info('set target size: {}'.format(wh_list))

            if KEY_CROP_SIZE in v:
                v[KEY_CROP_SIZE] = wh_list
                bcelogger.info('set crop size: {}'.format(wh_list))

    if KEY_VAL_DATASET in yaml_data and KEY_TRANSFORMS in yaml_data[KEY_VAL_DATASET]:
        for _, v in enumerate(yaml_data[KEY_VAL_DATASET][KEY_TRANSFORMS]):
            if KEY_TARGET_SIZE in v:
                v[KEY_TARGET_SIZE] = wh_list
                bcelogger.info('set target size: {}'.format(wh_list))


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
    

def set_transforms_value(transforms_config_dict, keys, val):
    '''
        set transforms parameter
    '''
    if keys[0] == KEY_TRAIN_DATASET:
        for _, v in enumerate(transforms_config_dict):
            if v["type"] in keys:
                if keys[-1] == "min_scale_factor" and keys[-1] in v:
                    v[keys[-1]] = convert_value_type(val)
                elif keys[-1] == "max_scale_factor" and keys[-1] in v:
                    v[keys[-1]] = convert_value_type(val)
                elif keys[-1] == "scale_step_size" and keys[-1] in v:
                    v[keys[-1]] = convert_value_type(val)
                break
 
 
def set_loss_value(loss_config_dict, keys, val):
    '''
        Decide which loss to modify and modify the corresponding parameters
    '''
    if keys[1] == "types":
        
        if keys[2] == "MixedLoss":
            if keys[3] == "one":
                loss_config_dict = loss_config_dict[keys[1]][0]
            elif keys[3] == "two":
                loss_config_dict = loss_config_dict[keys[1]][1]
            
            if len(keys) == 6:
                loss_config_dict_coef = loss_config_dict["coef"]
                if keys[5] == "DiceLoss":
                    loss_config_dict_coef[0] = convert_value_type(val)
                                
                elif keys[5] == "CrossEntropyLoss":
                    loss_config_dict_coef[1] = convert_value_type(val)
                    
                elif keys[5] == "LovaszSoftmaxLoss":
                    loss_config_dict_coef[2] = convert_value_type(val)
                    
                if convert_value_type(val) == 0.00001:
                    loss_config_dict_losses = loss_config_dict["losses"]
                    for config in loss_config_dict_losses:
                        if keys[5] == config['type']:
                            loss_config_dict_losses.remove(config)
                    
    elif keys[1] == "coef":
        loss_config_dict = loss_config_dict["coef"]
        if keys[2] == "first":
            loss_config_dict[0] = convert_value_type(val)
        elif keys[2] == "second":
            loss_config_dict[1] = convert_value_type(val)


def set_multi_key_value(yaml_data, multi_key, val):
    """
        set all do not care parameter
    """
    keys = multi_key.split('.')
    config_dict = yaml_data
    for i, key in enumerate(keys):
        if key in config_dict:
            if key == "transforms":
                set_transforms_value(config_dict[key], keys, val)
                break
            elif key == "loss":
                set_loss_value(config_dict[key], keys, val)
                break
            elif i + 1 == len(keys):
                config_dict[key] = convert_value_type(val)
            else:
                config_dict = config_dict[key]
        else:
            bcelogger.error('do NOT find key: {} of {}'.format(key, multi_key))
            break


def set_pretrained(yaml_data, model_type, pretrained_model_path):
    """
        modify pretrained model path & type by model_type parameter
    """
    if model_type in MODEL_TYPE_NAME_DICT:
        model_type_name = MODEL_TYPE_NAME_DICT[model_type]
        set_multi_key_value(yaml_data, KEY_PRETRAINED_TYPE, model_type_name[0])
        set_multi_key_value(yaml_data, KEY_PRETRAINED, os.path.join(pretrained_model_path, model_type_name[1]))
    else:
        bcelogger.error('do NOT support model type. {}'.format(model_type))


def get_mean_std(yaml_data):
    """
        get train mean/std
    """
    transform_ops = yaml_data[KEY_VAL_DATASET][KEY_TRANSFORMS]
    for _, v in enumerate(transform_ops):
        if 'mean' in v and 'std' in v:
            return v['mean'], v['std']
    return [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]


def set_loss_types(yaml_data, loss_types):
    """
        set loss types
    """
    # 如果yaml_data中有loss
    if KEY_LOSS_TYPES in yaml_data:
        # 获取loss.types
        loss_types_dict = yaml_data[KEY_LOSS_TYPES]['types']
        # 遍历loss.types(两个列表)，更改他的type名称
        for i, loss in enumerate(loss_types_dict):  
            loss['type'] = loss_types


def filter_losses(standard_mixedloss, loss_config):
    '''
        filter losses
    '''
    A_losses_types = [loss['type'] for loss in standard_mixedloss['losses']]
    indices_to_keep = [A_losses_types.index(loss['type']) 
                       for loss in loss_config['losses'] if loss['type'] in A_losses_types]
    new_coef = [loss_config['coef'][i] for i in indices_to_keep]
    loss_config['coef'] = new_coef
    return loss_config


def updata_loss(yaml_data):
    '''
        update loss parameter
    '''   
    if KEY_LOSS_TYPES in yaml_data:
        loss_types_dict = yaml_data[KEY_LOSS_TYPES]['types']
        for i, loss_config in enumerate(loss_types_dict):  
            if loss_config['type'] == 'CrossEntropyLoss':
                del loss_config['coef']
                del loss_config['losses']
            
            elif loss_config['type'] == 'MixedLoss':
                standard_mixedloss = {'losses': [{'type': 'DiceLoss'}, 
                                                 {'type': 'CrossEntropyLoss'}, 
                                                 {'type': 'LovaszSoftmaxLoss'}]}
                loss_config = filter_losses(standard_mixedloss, loss_config)


def generate_train_config(
        advanced_parameters: dict,
        train_config_name: str
):
    """
        modify parameter by template config
    """
    if advanced_parameters[KEY_NETWORK_ARCHITECTURE].startswith('change-'):
        input_yaml_name = 'parameter_c.yaml'
    else:
        input_yaml_name = 'parameter.yaml'
    
    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_yaml_name)
    bcelogger.info('train parameter name: {}'.format(input_yaml_name))

    yaml_data = get_yaml(input_yaml_name)
    mean, std = get_mean_std(yaml_data)
    # 更新metadata
    advanced_parameters.update({'mean': f'{mean}', 'std': f'{std}'})

    # 1. set correlative parameters
    correlative_parameter_keys = [KEY_EVAL_WIDTH, 
                                  KEY_EVAL_HEIGHT, 
                                  KEY_NETWORK_ARCHITECTURE, 
                                  KEY_PRETRAINED, 
                                  KEY_LOSS_TYPES]    # 1.1 target size
        # 1.1 target size
    set_target_size(yaml_data, advanced_parameters[KEY_EVAL_WIDTH], advanced_parameters[KEY_EVAL_HEIGHT])

    # 1.2 pretrained
    set_pretrained(yaml_data, advanced_parameters[KEY_NETWORK_ARCHITECTURE], advanced_parameters[KEY_PRETRAINED])

    # 1.3 set loss types
    set_loss_types(yaml_data, advanced_parameters[KEY_LOSS_TYPES])
    

    # 2. set get-though parameters by key-value of dict
    for key, val in advanced_parameters.items():
        if key not in correlative_parameter_keys:
            set_multi_key_value(yaml_data, key, val)
    
    # 3. update loss
    updata_loss(yaml_data)

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
    opt = parse_opt()
    from bcelogger.base_logger import setup_logger

    setup_logger(config=dict(file_name=os.path.join("/ssd2/lyg/GAEA-PIPE/ocrnet", "worker.log")))
    meta = {'algorithmParameters': {'evalHeight': 512, 'evalWidth': 512},
            'experimentName': None, 'experimentRunID': None, 'extraLoadModel': None,
            'inputSize': {'height': 512, 'width': 512},
            'jobName': None, 'labels': [], 'maxBoxNum': None}
    advanced_parameters = {"iters": "100", 
                           "lr_scheduler.learning_rate": "0.001",
                           "eval_height": "512", 
                           "eval_width": "512", 
                           "batch_size": "6", 
                           "model_type": "change-ocrnet",
                           "model.backbone.pretrained": "/ssd2/lyg/GAEA-PIPE/ocrnet/pretrained_model"}
    opt.train_config_name = '/ssd2/lyg/GAEA-PIPE/ocrnet/train_config.yaml'
    generate_train_config(advanced_parameters=advanced_parameters,
                          metadata=meta, train_config_name=opt.train_config_name)
