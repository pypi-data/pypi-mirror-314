#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/19
# @Author  : yanxiaodong
# @File    : time.py
"""
from datetime import datetime


def format_time():
    """
    Format time to string.
    """
    dt_object = datetime.now()
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

