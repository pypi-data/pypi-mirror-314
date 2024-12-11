#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/21
# @Author  : yanxiaodong
# @File    : inference_metric.py
"""
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

from windmillmodelv1.client.model_api_model import Label

from ..metric import BaseMetric
from .metric import MetricDisplayType, TaskType


class MetricName(Enum):
    """
    Metric
    """
    accuracy = "accuracy"
    precision = "precision"
    recall = "recall"
    f1_score = "f1Score"
    false_positive = "falsePositive"
    false_negative = "falseNegative"
    true_positive_rate = "truePositiveRate"
    average_precision = "averagePrecision"
    average_recall = "averageRecall"

    image_label_metric = "labelMetric"
    image_confusion_matrix = "confusionMatrix"

    bounding_box_metric = "boundingBoxMetric"
    bounding_box_precision_recall_curve = "boundingBoxPrecisionRecallCurve"
    bounding_box_label_metric = "boundingBoxLabelMetric"
    bounding_box_confusion_matrix = "boundingBoxConfusionMatrix"


class MetricDisplayName(Enum):
    """
    Metric display name
    """
    accuracy = "Accuracy(准确率)"
    precision = "Precision(精确率)"
    recall = "Recall(召回率)"
    f1_score = "F1Score(调和平均数)"
    false_positive = "误报数"
    false_negative = "漏报数"
    true_positive_rate = "检出率"
    average_precision = "(AP)平均精确率"
    average_recall = "(AR)平均召回率"

    label_metric = "图像级别评估结果"
    confusion_matrix = "混淆矩阵"

    bounding_box_precision_recall_curve = "P-R曲线"
    bounding_box_label_metric = "框级别评估结果"


class MetricDescription(Enum):
    """
    Description of the metric
    """
    accuracy = "指模型对测试集标签的正确预测数占总数的比例\n计算公式为：accuracy = (TP + TN) / (TP + TN + FP + FN)，" \
               "其中TP为真正例，TN为真负例，FP为假正例，FN为假负例"
    precision = "指分类器所预测的正样本中，真实正样本的比例\n计算公式为：Precision = TP / (TP + FP)"
    recall = "指分类器正确预测的正样本数量占所有真实正类的数量的比例\n计算公式为：Recall = TP / (TP + FN)"
    f1_score = "精确率和召回率的调和平均数，综合反映了模型的精度和召回率之间的平衡"
    false_positive = "实际不是正样本，但预测为正样本的数量"
    false_negative = "实际是正样本，但预测不是正样本的数量"
    true_positive_rate = "模型推理结果检出有目标的图片数量/图片总数"
    average_precision = "AP是衡量模型在单个类别下检测精度的指标"
    average_recall = "AR表示模型成功检测到的真实实例的比例，AR指标越高，说明模型成功检测到的真实实例比例越高"


class ConfusionMatrixRow(BaseModel):
    """
    Confusion Matrix Result
    """
    row: Optional[List[int]] = None


class ConfusionMatrixMetricResult(BaseModel):
    """
    Confusion Matrix Result
    """
    lower_bound: Optional[int] = Field(None, alias="lowerBound")
    upper_bound: Optional[int] = Field(None, alias="upperBound")
    rows: Optional[List[ConfusionMatrixRow]] = None


class AnnotationSpecs(BaseModel):
    """
    Annotation Specs
    """
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    description: Optional[str] = None


class ConfusionMatrixMetric(BaseModel):
    """
    Confusion Matrix
    """
    name: Optional[str] = MetricName.image_confusion_matrix.value
    display_name: Optional[str] = Field(MetricDisplayName.confusion_matrix.value, alias="displayName")
    column_annotation_specs: Optional[Union[List[List[AnnotationSpecs]], List[AnnotationSpecs]]] = \
        Field(None, alias="columnAnnotationSpecs")
    row_annotation_specs: Optional[Union[List[List[AnnotationSpecs]], List[AnnotationSpecs]]] = \
        Field(None, alias="rowAnnotationSpecs")
    display_formatter: Optional[str] = Field(None, alias="displayFormatter")
    label_names: Optional[List[str]] = Field(None, alias="labelNames")
    category: Optional[str] = None
    display_type: Optional[str] = Field(MetricDisplayType.table.value, alias="displayType")
    task_type: Optional[str] = Field(TaskType.metric_analysis.value, alias="taskType")
    result: Optional[Union[List[ConfusionMatrixMetricResult], ConfusionMatrixMetricResult]] = None


class LabelResult(BaseModel):
    """
    Metric result
    """
    label_name: Optional[str] = Field(None, alias="labelName")
    result: Optional[float] = None


class LabelMetricResult(BaseModel):
    """
    Inference label metric result
    """
    label_name: Optional[str] = Field(None, alias="labelName")
    precision: Optional[Union[float, List[LabelResult]]] = None
    recall: Optional[Union[float, List[LabelResult]]] = None
    accuracy: Optional[Union[float, List[LabelResult]]] = None
    f1_score: Optional[Union[float, List[LabelResult]]] = Field(None, alias="f1Score")
    false_positive: Optional[Union[float, List[LabelResult]]] = Field(None, alias="falsePositive")
    false_negative: Optional[Union[float, List[LabelResult]]] = Field(None, alias="falseNegative")
    true_positive_rate: Optional[Union[float, List[LabelResult]]] = Field(None, alias="truePositiveRate")

    average_precision: Optional[Union[float, List[LabelResult]]] = Field(None, alias="averagePrecision")
    average_recall: Optional[Union[float, List[LabelResult]]] = Field(None, alias="averageRecall")


class InferenceLabelMetric(BaseModel):
    """
    Inference label metric
    """
    name: Optional[str] = MetricName.image_label_metric.value
    display_name: Optional[str] = Field(MetricDisplayName.label_metric.value, alias="displayName")
    column_annotation_specs: Optional[List[AnnotationSpecs]] = Field(None, alias="columnAnnotationSpecs")
    display_formatter: Optional[List[str]] = Field(None, alias="displayFormatter")
    category: Optional[str] = None
    display_type: Optional[str] = Field(MetricDisplayType.table.value, alias="displayType")
    task_type: Optional[str] = Field(TaskType.metric_analysis.value, alias="taskType")
    result: Optional[List[LabelMetricResult]] = None


class InferenceSingleMetric(BaseModel):
    """
    Inference image metric
    """
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")
    display_formatter: Optional[str] = Field(None, alias="displayFormatter")
    category: Optional[str] = None
    display_type: Optional[str] = Field(MetricDisplayType.card.value, alias="displayType")
    task_type: Optional[str] = Field(TaskType.metric_analysis.value, alias="taskType")
    result: Optional[float] = None


class BoundingBoxLabelConfidenceMetric(BaseModel):
    """
    Bounding Box Label Metric
    """
    recall: Optional[float] = None
    precision: Optional[float] = None


class BoundingBoxPRCurveMetricResult(BaseModel):
    """
    Bounding Box Label Metric
    """
    iou_threshold: Optional[float] = Field(None, alias="iouThreshold")
    average_precision: Optional[float] = Field(None, alias="averagePrecision")
    label_name: Optional[str] = Field(None, alias="labelName")
    confidence_metrics: Optional[List[BoundingBoxLabelConfidenceMetric]] = Field(None, alias="confidenceMetrics")


class BoundingBoxPRCurveMetric(BaseModel):
    """
    Bounding Box Label Metric
    """
    name: Optional[str] = MetricName.bounding_box_precision_recall_curve.value
    displayName: Optional[str] = MetricDisplayName.bounding_box_precision_recall_curve.value
    horizontal_axis_annotation_specs: Optional[str] = Field(None, alias="horizontalAxisAnnotationSpecs")
    vertical_axis_annotation_specs: Optional[str] = Field(None, alias="verticalAxisAnnotationSpecs")
    display_formatter: Optional[str] = Field(None, alias="displayFormatter")
    category: Optional[str] = None
    display_type: Optional[str] = Field(MetricDisplayType.chart.value, alias="displayType")
    task_type: Optional[str] = Field(TaskType.metric_analysis.value, alias="taskType")
    result: Optional[List[BoundingBoxPRCurveMetricResult]] = None


class InferenceMetric(BaseMetric):
    """
    Object Detection Metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        InferenceLabelMetric,
        InferenceSingleMetric,
        ConfusionMatrixMetric,
        BoundingBoxPRCurveMetric]]] = None