#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/1
# @Author  : xuxiaowen02
# @File    : metric_api.py
"""
from typing import List, Union, Optional
from pydantic import BaseModel

from .metric import Label, BaseMetric, BaseTrainMetric, TrainMetric, ConfusionMatrixMetric
from .object_detection_metric import BoundingBoxLabelMetric, \
    BoundingBoxMeanAveragePrecision, \
    BoundingBoxMeanAverageRecall, \
    BoundingBoxLabelAveragePrecision


class SegLabelConfidenceMetric(BaseModel):
    """
    Seg Mask Label Metric
    """
    precision: Optional[float] = None
    recall: Optional[float] = None


class SegLabelMetricResult(BaseModel):
    """
    Seg Mask Label Metric
    """
    iouThreshold: Optional[float] = None
    averagePrecision: Optional[float] = None
    labelName: Optional[str] = None
    confidenceMetrics: Optional[List[SegLabelConfidenceMetric]] = None


class SegLabelMetric(BaseModel):
    """
    Seg Mask Label Metric
    """
    name: Optional[str] = None  # SegLabelMetric
    displayName: Optional[str] = None
    result: Optional[List[SegLabelMetricResult]] = None


class SegMeanAveragePrecision(BaseModel):
    """
    Seg Mask Mean Average Precision Metric
    """
    name: Optional[str] = None  # SegMeanAveragePrecision
    displayName: Optional[str] = None
    result: Optional[float] = None


class SegMeanAverageRecall(BaseModel):
    """
    Seg Mask Mean Average Recall Metric
    """
    name: Optional[str] = None  # SegMeanAverageRecall
    displayName: Optional[str] = None
    result: Optional[float] = None


class SegLabelAveragePrecisionResult(BaseModel):
    """
    Seg Mask Mean Average Precision Metric
    """
    labelName: Optional[str] = None
    averagePrecision: Optional[float] = None


class SegLabelAveragePrecision(BaseModel):
    """
    Seg Mask Label Average Precision Metric
    """
    name: Optional[str] = None  # SegLabelAveragePrecision
    displayName: Optional[str] = None
    result: Optional[List[SegLabelAveragePrecisionResult]] = None


class InstanceSegmentationMetric(BaseMetric):
    """
    Object Detection Metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        BoundingBoxLabelMetric,  # eval
        BoundingBoxMeanAveragePrecision, # eval-
        BoundingBoxMeanAverageRecall, # eval-
        BoundingBoxLabelAveragePrecision,  # eval
        ConfusionMatrixMetric,  # eval bbox/seg
        SegLabelMetric,  # eval
        SegMeanAveragePrecision, # eval-
        SegMeanAverageRecall, # eval-
        SegLabelAveragePrecision  # eval
    ]]] = None


class BoundingBoxLabelAveragePrecisionResult(BaseModel):
    """
    Bounding Box Mean Average Precision Metric
    """
    labelName: Optional[str] = None
    averagePrecision: Optional[float] = None


class BoundingBoxLabelConfidenceMetric(BaseModel):
    """
    Bounding Box Label Metric
    """
    recall: Optional[float] = None
    precision: Optional[float] = None


class BoundingBoxLabelMetricResult(BaseModel):
    """
    Bounding Box Label Metric
    """
    iouThreshold: Optional[float] = None
    averagePrecision: Optional[float] = None
    labelName: Optional[str] = None
    confidenceMetrics: Optional[List[BoundingBoxLabelConfidenceMetric]] = None
