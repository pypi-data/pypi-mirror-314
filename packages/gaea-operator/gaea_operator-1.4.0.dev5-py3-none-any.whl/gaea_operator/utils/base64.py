#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/11
# @Author  : yanxiaodong
# @File    : base64.py
"""
import base64


def is_base64(s):
    """
    判断一个字符串是否是base64编码的
    """
    try:
        decoded = base64.b64decode(s, validate=True)
        return base64.b64encode(decoded).decode('utf-8') == s
    except Exception:
        return False