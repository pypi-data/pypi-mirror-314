#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/23
# @Author  : yanxiaodong
# @File    : text_detection.py
"""
from pydantic import BaseModel
from typing import List, Union, Optional

from .metric import BaseMetric, \
    PRECISION_METRIC_NAME, \
    RECALL_METRIC_NAME, \
    HMEAN_METRIC_NAME


class PrecisionMetric(BaseModel):
    """
    Precision Metric
    """
    name: Optional[str] = PRECISION_METRIC_NAME  # Precision
    displayName: Optional[str] = "Precision(精确率)"
    result: Optional[float] = None


class RecallMetric(BaseModel):
    """
    Recall Metric
    """
    name: Optional[str] = RECALL_METRIC_NAME  # Recall
    displayName: Optional[str] = "Recall(召回率)"
    result: Optional[float] = None


class HarmonicMeanMetric(BaseModel):
    """
    Harmonic Mean Metric
    """
    name: Optional[str] = HMEAN_METRIC_NAME  # Hmean
    displayName: Optional[str] = "Hmean(调和平均数)"
    result: Optional[float] = None


class TextDetectionMetric(BaseMetric):
    """
    ImageClassification MultiClass Metric
    """
    metrics: Optional[List[Union[PrecisionMetric, RecallMetric, HarmonicMeanMetric]]] = None