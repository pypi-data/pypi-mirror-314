#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/14
# @Author  : yanxiaodong
# @File    : metric_api.py
"""
from typing import List, Union, Optional
from pydantic import BaseModel

from .metric import Label, BaseMetric, BaseTrainMetric, TrainMetric, ConfusionMatrixMetric


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


class BoundingBoxLabelMetric(BaseModel):
    """
    Bounding Box Label Metric
    """
    name: Optional[str] = None  # boundingBoxLabelMetric
    displayName: Optional[str] = None
    result: Optional[List[BoundingBoxLabelMetricResult]] = None


class BoundingBoxMeanAveragePrecision(BaseModel):
    """
    Bounding Box Mean Average Precision Metric
    """
    name: Optional[str] = None  # boundingBoxMeanAveragePrecision
    displayName: Optional[str] = None
    result: Optional[float] = None


class BoundingBoxMeanAverageRecall(BaseModel):
    """
    Bounding Box Mean Average Recall Metric
    """
    name: Optional[str] = None  # boundingBoxMeanAverageRecall
    displayName: Optional[str] = None
    result: Optional[float] = None


class BoundingBoxLabelAveragePrecisionResult(BaseModel):
    """
    Bounding Box Mean Average Precision Metric
    """
    labelName: Optional[str] = None
    averagePrecision: Optional[float] = None


class BoundingBoxLabelAveragePrecision(BaseModel):
    """
    Bounding Box Label Average Precision Metric
    """
    name: Optional[str] = None  # boundingBoxLabelAveragePrecision
    displayName: Optional[str] = None
    result: Optional[List[BoundingBoxLabelAveragePrecisionResult]] = None


class ObjectDetectionMetric(BaseMetric):
    """
    Object Detection Metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        BoundingBoxLabelMetric,
        BoundingBoxMeanAveragePrecision,
        BoundingBoxMeanAverageRecall,
        BoundingBoxLabelAveragePrecision,
        ConfusionMatrixMetric]]] = None