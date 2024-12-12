#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/25
# @Author  : yanxiaodong
# @File    : types.py
"""
from typing import List, Dict
from pydantic import BaseModel


class Image(BaseModel):
    """
    Image
    """
    kind: str
    name: str


class Properties(BaseModel):
    """
    Properties
    """
    accelerator: str = ""
    computeTips: Dict[str, List] = {}
    flavourTips: Dict[str, str] = {}
    images: List[Image] = []
    modelFormats: Dict[str, Dict[str, List]] = {}