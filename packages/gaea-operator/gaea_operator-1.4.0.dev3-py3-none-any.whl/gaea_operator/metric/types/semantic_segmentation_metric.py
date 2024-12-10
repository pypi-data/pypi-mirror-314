#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/26
# @Author  : yanxiaodong
# @File    : semantic_segmentation_metric.py
"""
from typing import Optional, List, Union
from pydantic import BaseModel

from .metric import BaseMetric, Label


class MeanIntersectionOverUnionMetric(BaseModel):
    """
    Mean intersection over union metric.
    """
    name: Optional[str] = None  # meanIntersectionOverUnionMetric
    displayName: Optional[str] = None
    result: Optional[float] = None


class PixelAccuracyMetric(BaseModel):
    """
    Pixel Accuracy metric.
    """
    name: Optional[str] = None  # pAcc
    displayName: Optional[str] = None
    result: Optional[float] = None


class LabelIntersectionOverUnionMetricResult(BaseModel):
    """
    Mean intersection over union metric.
    """
    labelName: Optional[str] = None
    iou: Optional[float] = None


class LabelIntersectionOverUnionMetric(BaseModel):
    """
    Mean intersection over union metric.
    """
    name: Optional[str] = None  # labelIntersectionOverUnionMetric
    displayName: Optional[str] = None
    result: Optional[List[LabelIntersectionOverUnionMetricResult]] = None


class SemanticSegmentationMetric(BaseMetric):
    """
    Semantic segmentation metric.
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        MeanIntersectionOverUnionMetric,
        PixelAccuracyMetric,
        LabelIntersectionOverUnionMetric]]] = None