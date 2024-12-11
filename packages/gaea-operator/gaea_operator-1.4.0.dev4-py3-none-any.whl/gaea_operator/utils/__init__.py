#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from .consts import DEFAULT_TRAIN_CONFIG_FILE_NAME, \
    DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME, \
    DEFAULT_TRANSFORM_CONFIG_FILE_NAME, \
    DEFAULT_META_FILE_NAME, \
    DEFAULT_METRIC_FILE_NAME, \
    DEFAULT_TRITON_CONFIG_FILE_NAME, \
    DEFAULT_PYTORCH_MODEL_FILE_NAME, \
    DEFAULT_DEPLOY_CONFIG_FILE_NAME
from .file import find_upper_level_folder, \
    write_file, \
    read_file, \
    read_yaml_file, \
    write_yaml_file, \
    find_dir
from .compress import get_filepaths_in_archive
from .time import format_time
from .accelerator import get_accelerator, Accelerator
from .model_template import ModelTemplate
from .registry import METRIC
from .import_module import paddle, torch, Tensor, PTensor, TTensor
from .tensor import list2ndarray, numpy_round2list, paddle_round2list, torch_round2list, list_round
from .base64 import is_base64
from .std_alg_common import NX_METRIC_MAP, NX_CATEGORY_MAP, _retrive_path, _copy_annotation_file_2_backup_path, \
    get_annotation_type, _modify_annotation, pre_listdir_folders, rle_to_polygon, \
    NX_ANNOTATION_TYPE_CLS, NX_ANNOTATION_TYPE_INSTANCE_SEG, generate_label_description

__all__ = ["find_upper_level_folder",
           "get_filepaths_in_archive",
           "write_file",
           "read_file",
           "write_yaml_file",
           "format_time",
           "read_yaml_file",
           "find_dir",
           "DEFAULT_TRAIN_CONFIG_FILE_NAME",
           "DEFAULT_TRANSFORM_CONFIG_FILE_NAME",
           "DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME",
           "DEFAULT_PYTORCH_MODEL_FILE_NAME",
           "DEFAULT_META_FILE_NAME",
           "DEFAULT_METRIC_FILE_NAME",
           "DEFAULT_TRITON_CONFIG_FILE_NAME",
           "DEFAULT_PYTORCH_MODEL_FILE_NAME",
           "DEFAULT_DEPLOY_CONFIG_FILE_NAME",
           "get_accelerator",
           "Accelerator",
           "ModelTemplate",
           "METRIC",
           "paddle",
           "torch",
           "Tensor",
           "PTensor",
           "TTensor",
           "list2ndarray",
           "numpy_round2list",
           "paddle_round2list",
           "torch_round2list",
           "list_round",
           "is_base64",
           "NX_METRIC_MAP", 
           "NX_CATEGORY_MAP", 
           "NX_ANNOTATION_TYPE_CLS",
           "NX_ANNOTATION_TYPE_INSTANCE_SEG",
           "_retrive_path", 
           "_copy_annotation_file_2_backup_path", 
           "get_annotation_type", 
           "_modify_annotation", 
           "pre_listdir_folders", 
           "rle_to_polygon"]
