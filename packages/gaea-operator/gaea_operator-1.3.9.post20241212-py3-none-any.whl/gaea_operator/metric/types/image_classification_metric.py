#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/26
# @Author  : yanxiaodong
# @File    : image_classification_mutilclass.py
"""
from typing import List, Optional, Union
from pydantic import BaseModel

from .metric import BaseMetric, Label, ConfusionMatrixMetric


class AccuracyMetric(BaseModel):
    """
    Accuracy Metric.
    """
    name: Optional[str] = None  # accuracy
    displayName: Optional[str] = None
    result: Optional[float] = None


class LabelPrecisionMetricResult(BaseModel):
    """
    Label Precision Result.
    """
    labelName: Optional[str] = None
    precision: Optional[float] = None
    recall: Optional[float] = None


class LabelPrecisionMetric(BaseModel):
    """
    Label Precision.
    """
    name: Optional[str] = None  # LabelPrecision
    displayName: Optional[str] = None
    result: Optional[List[LabelPrecisionMetricResult]] = None


class ImageClassificationMetric(BaseMetric):
    """
    ImageClassification MultiClass Metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        AccuracyMetric,
        LabelPrecisionMetric,
        ConfusionMatrixMetric]]] = None


class SingleAttrImageClassificationMetric(BaseModel):
    """为多属性分类任务开发的单属性分类指标"""
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        AccuracyMetric,
        LabelPrecisionMetric,
        ConfusionMatrixMetric]]] = None


class MultiAttributeImageClassificationMetric(BaseMetric):
    """
    MultiAttribute Image Classification Metric
    """
    labels: Optional[List[Label]] = None    # 存放所有属性名称
    metrics: Optional[List[Union[
        AccuracyMetric,              # 仅存放全体任务的平均指标
        SingleAttrImageClassificationMetric    # 存放每个属性的结果
    ]]] = None