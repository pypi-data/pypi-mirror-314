#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/26
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from .config import Config, KEY_NETWORK_ARCHITECTURE
from .ppyoloe_plus.ppyoloeplus_config import PPYOLOEPLUSMConfig
from .resnet.resnet_config import ResNetConfig
from .ocrnet.ocrnet_config import OCRNetConfig
from .convnext.convnext_config import ConvNextConfig
from .codetr.codetr_config import CoDETRConfig
from .repvit.repvit_config import RepViTConfig
from .dbnet.dbnet_config import DBNetConfig
from .svtr_lcnet.svtr_lcnet_config import SVTRLCNetConfig
from .std_algorithm.generate_std_pdc_input_config import generate_task

__all__ = ["PPYOLOEPLUSMConfig",
           "KEY_NETWORK_ARCHITECTURE",
           "Config",
           "ResNetConfig",
           "OCRNetConfig",
           "ConvNextConfig",
           "CoDETRConfig",
           "RepViTConfig",
           "DBNetConfig",
           "SVTRLCNetConfig",
           "generate_task"]
