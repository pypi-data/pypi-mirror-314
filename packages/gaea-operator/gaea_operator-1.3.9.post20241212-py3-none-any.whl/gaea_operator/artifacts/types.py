#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/3
# @Author  : yanxiaodong
# @File    : types.py
"""
from pydantic import BaseModel


class Variable(BaseModel):
    """
    Variable
    """
    type: str = ""
    name: str = ""
    displayName: str = ""
    value: str = ""
    key: str = ""