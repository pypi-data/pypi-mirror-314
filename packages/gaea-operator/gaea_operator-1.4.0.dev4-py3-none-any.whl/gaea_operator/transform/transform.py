#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/17
# @Author  : yanxiaodong
# @File    : transform.py
"""
import os

from gaea_operator.utils import DEFAULT_TRANSFORM_CONFIG_FILE_NAME
from .cvt_copy_model import cvt_copy_model


class Transform(object):
    """
    Transform model class.
    """
    def __init__(self, windmill_client):
        self.windmill_client = windmill_client

    def transform(self, transform_config_dir: str, src_model_uri: str, dst_model_uri: str):
        """
        Transform the model from src_model_uri to dst_model_uri.
        """
        transform_config_filepath = os.path.join(transform_config_dir, DEFAULT_TRANSFORM_CONFIG_FILE_NAME)
        cvt_copy_model(transform_config_filepath, src_model_uri, dst_model_uri)