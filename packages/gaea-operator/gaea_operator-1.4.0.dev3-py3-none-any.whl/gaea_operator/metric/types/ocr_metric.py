#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/23
# @Author  : yanxiaodong
# @File    : text_recognition.py
"""
from typing import List, Union, Optional

from .metric import BaseMetric
from .text_detection_metric import PrecisionMetric, RecallMetric
from .image_classification_metric import AccuracyMetric


class OCRMetric(BaseMetric):
    """
    ImageClassification MultiClass Metric
    """
    metrics: Optional[List[Union[PrecisionMetric, RecallMetric, AccuracyMetric]]] = None