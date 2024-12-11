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

import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE, \
    get_pretrained_model_path, \
    set_multi_key_value, \
    KEY_EVAL_HEIGHT, \
    KEY_EVAL_WIDTH
from gaea_operator.utils import write_yaml_file


def get_mean_std(config_data):
    """
        get train mean/std
    """
    transform_ops = config_data['Eval']['dataset']['transforms']
    for op in transform_ops:
        for key, value in op.items():
            if key == "NormalizeImage":
                return value['mean'], value['std']
    raise ValueError(f"No NormalizeImage in transform_ops {transform_ops}")


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
    advanced_parameters["Train.dataset.transforms.EastRandomCropData.size"] = [width, height]
    advanced_parameters["Eval.dataset.transforms.DetResizeForTest.resize_short"] = max(width, height)

    epoch = advanced_parameters["Global.epoch_num"]
    advanced_parameters["Train.dataset.transforms.MakeBorderMap.total_epoch"] = epoch
    advanced_parameters["Train.dataset.transforms.MakeShrinkMap.total_epoch"] = epoch

    if advanced_parameters[KEY_NETWORK_ARCHITECTURE].endswith('student'):
        config_filename = 'parameter_student.yaml'
    else:
        config_filename = 'parameter_teacher.yaml'

    bcelogger.info('train parameter name: {}'.format(config_filename))

    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_filename)
    with open(config_file) as f:
        config_data = yaml.load(f, Loader=yaml.Loader)

    # 获取 mean 和 std
    mean, std = get_mean_std(config_data)
    advanced_parameters.update({'mean': f'{mean}', 'std': f'{std}'})

    # get model pretrain model path
    paths = get_pretrained_model_path(pretrain_model_uri)
    advanced_parameters["Global.pretrained_model"] = paths[0] if len(paths) > 0 else None

    for key, val in advanced_parameters.items():
        set_multi_key_value(config_data, key, val)

    bcelogger.info('begin to save yaml. {}'.format(train_config_name))
    write_yaml_file(config_data, os.path.dirname(train_config_name), os.path.basename(train_config_name))
    bcelogger.info('write train config finish.')
