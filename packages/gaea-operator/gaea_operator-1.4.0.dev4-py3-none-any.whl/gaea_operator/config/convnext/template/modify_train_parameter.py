# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify input train parameter yaml
Authors: liyinggang
Date:    2023-04-
"""
import os
import yaml
import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE

IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)
IMAGENET_INCEPTION_MEAN = (0.5, 0.5, 0.5)
IMAGENET_INCEPTION_STD = (0.5, 0.5, 0.5)
KEY_EPOCH = 'epochs'
KEY_INPUT_SIZE = 'input_size'
KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_WIDTH = 'eval_width'
KEY_TRAIN_NUM_WORKERS = 'num_workers'
KEY_TRAIN_BATCH_SIZE = 'batch_size'
KEY_PRETRAINED_MODEL = 'pretrained'
KEY_MODEL = 'model'

KEY_PRETRAINED_MODEL_MAP = {
    'convnext_tiny': 'convnext_tiny_22k_224.pth',
    'convnext_small': 'convnext_small_22k_224.pth',
    'convnext_base': 'convnext_base_22k_224.pth',
    'convnext_large': 'convnext_large_22k_224.pth',
    'convnext_xlarge': 'convnext_xlarge_22k_224.pth',
    "repvit_m0_9" : "repvit_m0_9_distill_450e.pth",
    "repvit_m1_0": "repvit_m1_0_distill_450e.pth",
    "repvit_m1_1": "repvit_m1_1_distill_450e.pth",
    "repvit_m1_5": "repvit_m1_5_distill_450e.pth",
    "repvit_m2_3": "repvit_m2_3_distill_450e.pth",
}


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


def get_pretrained_model_name(model_type, pretrained_model_path):
    """
        get pretrained model absolute path
    """
    if model_type in KEY_PRETRAINED_MODEL_MAP:
        return os.path.join(pretrained_model_path, KEY_PRETRAINED_MODEL_MAP[model_type])
    else:
        raise ValueError('model_type: {} is not supported'.format(model_type))


def generate_train_config(
        advanced_parameters: dict,
        metadata: dict,
        train_config_name: str
    ):
    """
    modify parameter by template config
    """
    input_yaml_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parameter.yaml')
    yaml_data = None
    with open(input_yaml_name) as f:
        yaml_data = yaml.load(f, Loader=yaml.Loader)
    if yaml_data is None:
        bcelogger.error('Parse parameter.yaml failed -> yaml data is None.')
    imagenet_default_mean_and_std = yaml_data['imagenet_default_mean_and_std']
    mean = IMAGENET_INCEPTION_MEAN if not imagenet_default_mean_and_std else IMAGENET_DEFAULT_MEAN
    std = IMAGENET_INCEPTION_STD if not imagenet_default_mean_and_std else IMAGENET_DEFAULT_STD

    # 更新metadata
    metadata["algorithmParameters"].update({'mean': mean, 'std': std})

    # 1. set correlative parameters
    correlative_parameter_keys = [KEY_EVAL_WIDTH, KEY_EVAL_HEIGHT, KEY_NETWORK_ARCHITECTURE]
    # 1.1 target size
    yaml_data[KEY_INPUT_SIZE][0] = int(advanced_parameters[KEY_EVAL_WIDTH])
    yaml_data[KEY_INPUT_SIZE][1] = int(advanced_parameters[KEY_EVAL_HEIGHT])
    # 1.2 model 
    yaml_data[KEY_MODEL] = advanced_parameters[KEY_NETWORK_ARCHITECTURE]
    # 
    for key, val in advanced_parameters.items():
        if key not in correlative_parameter_keys:
            if KEY_PRETRAINED_MODEL == key:
                val = get_pretrained_model_name(advanced_parameters[KEY_NETWORK_ARCHITECTURE],
                                                advanced_parameters[KEY_PRETRAINED_MODEL])
            set_multi_key_value(yaml_data, key, val)

    bcelogger.info('begin to save yaml. {}'.format(train_config_name))
    with open(train_config_name, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
    bcelogger.info('write train config finish.')