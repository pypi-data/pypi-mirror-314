#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/25
# @Author  : yanxiaodong
# @File    : types.py
"""
from typing import List, Dict, Optional
from pydantic import BaseModel


class Image(BaseModel):
    """
    Image
    """
    kind: str
    name: str


class TimeProfilerParams(BaseModel):
    """
    TimeProfilerParams
    """
    trainImageCount: Optional[int] = None
    valImageCount: Optional[int] = None
    evalImageCount: Optional[int] = None

    networkArchitecture: Optional[str] = None
    epoch: Optional[int] = None
    batchSize: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    evalSize: Optional[str] = None
    workerNum: Optional[int] = None
    precision: Optional[str] = None

    gpuNum: Optional[int] = None

    qps: Optional[int] = None


class Properties(BaseModel):
    """
    Properties
    """
    accelerator: Optional[str] = ""
    computeTips: Optional[Dict[str, List]] = {}
    flavourTips: Optional[Dict[str, str]] = {}
    images: Optional[List[Image]] = []
    modelFormats: Optional[Dict[str, Dict[str, List]]] = {}
    timeProfilerParams: Optional[TimeProfilerParams] = None