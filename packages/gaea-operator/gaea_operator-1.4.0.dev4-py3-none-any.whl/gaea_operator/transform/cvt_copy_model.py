# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
transform model
Authors: wanggaofei03
Date:    2023-11-08
"""

import argparse
import os
import yaml
import bcelogger
import sys
import shutil

from gaea_transform.core.engine.local_test import Runner

def get_yaml(yaml_name):
    """
    获取指定名称的Yaml文件的数据。
    
    Args:
        yaml_name (str): 要获取的文件名。
    
    Returns:
        Optional[Dict]: 如果读取成功，则返回解析后的Yaml数据；否则，返回None。
    
    """
    with open(yaml_name, 'r', encoding='utf-8') as f:
        file_data = f.read()

        yaml_data = yaml.load(file_data, Loader=yaml.FullLoader)
        return yaml_data
    return None

def get_cvt_model_folder(config_file_name):
    """
    根据配置文件名称获取转换模型存储路径
    
    Args:
        config_file_name (str): 配置文件名称，支持相对路径和绝对路径
    
    Returns:
        Optional[str]: 返回转换模型存储路径, 若配置文件不存在或不包含 'pipeline' 字段则返回 None
    
    """
    cfg_data = get_yaml(config_file_name)
    if cfg_data is not None and cfg_data.get('pipeline') is not None:
        final_step = cfg_data['pipeline'][-1]
        return final_step['type']
    return None

def rename_postfix(dir_path, postfix, new_name):
    """
    rename all files endswith postfix to new_name
    Args:
        dir_path -- directory path
        postfix -- file name postfix
        new_name -- new file name
    """
    path_files = os.listdir(dir_path)
    same_postfixs = []
    for file_name in path_files:
        if len(file_name) > len(postfix) and file_name[-len(postfix):] == postfix:
            same_postfixs.append(file_name)
    if len(same_postfixs) == 1:
        old_file_name = os.path.join(dir_path, same_postfixs[0])
        new_file_name = os.path.join(dir_path, new_name)
        if os.path.isfile(old_file_name):
            os.rename(old_file_name, new_file_name)
def copy_all_files(src, dst):
    """
        only copy files in the src folder
    """
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst)

def cvt_copy_model(transform_config_path, src_model_path, dst_model_path):
    """ cvt copy model
        Args:
            transform_config_path -- transform config file path
            src_model_path -- src model path
            dst_model_path -- dst model path
        Returns:
            None
    """
    # 1. convert model
    dst_tmp_path = '/root/tmp_convert_path'
    if(os.path.exists(dst_tmp_path) is False):
        os.makedirs(dst_tmp_path)

    run = Runner(src_path=src_model_path, dst_path=dst_tmp_path, cfg_path=transform_config_path)
    run.run()
    
    # 2. copy dst model
    cvt_model_folder = get_cvt_model_folder(transform_config_path)
    if cvt_model_folder is None:
        bcelogger.error('transform config do NOT have output parameter. {}'.format(transform_config_path))
    else:
        copy_all_files(os.path.join(dst_tmp_path, cvt_model_folder), dst_model_path)
        rename_postfix(dst_model_path, '.om', 'model.om')

def parse_opt():
    """ parser opt
        Args:

        Returns:
            opt -- command line parameter
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--transform_config_path', type=str,
                        default="/root/transform_config", help='transform config file path')
    parser.add_argument('--src_model_path', type=str, default="/root/src_model", help='src model path')
    parser.add_argument('--dst_model_path', type=str, default="/root/dst_model", help='dst model path')

    option = parser.parse_args()
    return option

if __name__ == '__main__':
    opt = parse_opt()
    bcelogger.info("args: {}".format(opt))
    cvt_copy_model(opt.transform_config_path, opt.src_model_path, opt.dst_model_path)
