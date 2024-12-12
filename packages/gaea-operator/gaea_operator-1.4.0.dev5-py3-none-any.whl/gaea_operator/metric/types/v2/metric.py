#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/10/21
# @Author  : yanxiaodong
# @File    : metric.py
"""
from enum import Enum


class MetricCategory(Enum):
    """
    Metric category
    """
    category_image = "Image/Image"
    category_bbox = "Image/BBox"


class MetricDisplayType(Enum):
    """
    Metric display type
    """
    table = "table"  # 表格展示
    chart = "chart"  # 曲线图展示
    card = "card"  # 卡片展示


class TaskType(Enum):
    """
    Metric display type
    """
    statistical_analysis = "statisticalAnalysis"
    metric_analysis = "metricAnalysis"


class DisplayFormatter(Enum):
    """
    Display formatter
    """
    int_ = "int"
    float_ = "float"
    percentage = "percentage"