#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/17
# @Author  : yanxiaodong
# @File    : metric.py
"""
from typing import Optional, List, Union
from pydantic import BaseModel

LOSS_METRIC_NAME = "Loss"
MAP_METRIC_NAME = "mAP"
AP50_METRIC_NAME = "AP50"
AR_METRIC_NAME = "AR"
MIOU_METRIC_NAME = "mIOU"
PACC_METRIC_NAME = "pAcc"
ACCURACY_METRIC_NAME = "ACC"
SEG_MAP_METRIC_NAME = "segmAP"
SEG_AP50_METRIC_NAME = "segAP50"
SEG_AR_METRIC_NAME = "segAR"
HMEAN_METRIC_NAME = "Hmean"
PRECISION_METRIC_NAME = "precision"
RECALL_METRIC_NAME = "recall"
OCR_ACCURACY_METRIC_NAME = "accuracy"
PRECISION_RECALL_CURVE_METRIC_NAME = "precisionRecallCurve"
BOUNDING_BOX_LABEL_METRIC_NAME = "boundingBoxLabelMetric"
INSTANCE_SEG_LABEL_METRIC_NAME = "segLabelMetric"
BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME = "boundingBoxMeanAveragePrecision"
BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME = "boundingBoxMeanAverageRecall"
BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME = "boundingBoxLabelAveragePrecision"
INSTANCE_SEG_MEAN_AVERAGE_PRECISION_METRIC_NAME = "segMeanAveragePrecision"
INSTANCE_SEG_MEAN_AVERAGE_RECALL_METRIC_NAME = "segMeanAverageRecall"
INSTANCE_SEG_LABEL_AVERAGE_PRECISION_METRIC_NAME = "segLabelAveragePrecision"
CONFUSION_MATRIX_METRIC_NAME = "confusionMatrix"
BOUNDING_BOX_CONFUSION_MATRIX_METRIC_NAME = "boundingBoxConfusionMatrix"
INSTANCE_SEG_CONFUSION_MATRIX_METRIC_NAME = "segConfusionMatrix"
CLASSIFICATION_ACCURACY_METRIC_NAME = "accuracy"
CLASSIFICATION_LABEL_PRECISION_METRIC_NAME = "labelPrecision"
SEMANTIC_SEGMENTATION_MIOU_METRIC_NAME = "meanIntersectionOverUnionMetric"
SEMANTIC_SEGMENTATION_LABEL_IOU_METRIC_NAME = "labelIntersectionOverUnionMetric"
LABEL_STATISTIC_METRIC = "labelStatisticMetric"
ANNOTATION_CONFIDENCE_STATISTIC_METRIC = "annotationConfidenceStatisticMetric"
ANNOTATION_AREA_STATISTIC_METRIC = "annotationAreaStatisticMetric"
ANNOTATION_HEIGHT_STATISTIC_METRIC = "annotationHeightStatisticMetric"
ANNOTATION_WIDTH_STATISTIC_METRIC = "annotationWidthStatisticMetric"
INFERENCE_LABEL_METRIC_NAME = "labelMetric"
ANNOTATION_RATIO = "annotationRatio"
ANNOTATED_IMAGE = "annotatedImage"
IMAGE = "image"


class Label(BaseModel):
    """
    Labeled Object
    """
    id: int
    name: str
    parentID: Optional[Union[int, str]] = None


class BaseMetric(BaseModel):
    """
    Metric Object
    """
    artifactName: Optional[str] = None
    datasetName: Optional[str] = None
    annotationSetName: Optional[str] = None
    baselineJobName: Optional[str] = None
    taskKind: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class BaseTrainMetric(BaseModel):
    """
    Loss Metric
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[float] = None


class TrainMetric(BaseModel):
    """
    Object Detection Metric
    """
    epoch: Optional[str] = None
    step: Optional[str] = None
    metrics: Optional[List[BaseTrainMetric]] = None


class StatisticMetric(BaseModel):
    """
    Confidence Cut
    """
    lowerBound: Optional[float] = None
    upperBound: Optional[float] = None
    bboxCount: Optional[int] = None


class LabelCutStatisticResult(BaseModel):
    """
    Label confidence statistics result
    """
    labelName: Optional[str] = None
    statisticStep: Optional[float] = None
    statisticMetrics: Optional[List[StatisticMetric]] = None


class LabelCutStatistic(BaseModel):
    """
    Label confidence statistics metric
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[List[LabelCutStatisticResult]] = None


class LabelCountStatisticResult(BaseModel):
    """
    Label count statistics result
    """
    labelName: Optional[str] = None
    labelCount: Optional[Union[int, List['LabelCountStatisticResult']]] = None


class LabelCountStatistic(BaseModel):
    """
    Label count statistics metric
    """
    name: Optional[str] = None  # labelStatisticMetric
    displayName: Optional[str] = None
    result: Optional[List[LabelCountStatisticResult]] = None


class LabelStatisticsMetric(BaseMetric):
    """
    Label statistics metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        LabelCountStatistic,
        LabelCutStatistic]]] = None


class InferenceLabelMetricResult(BaseModel):
    """
    Inference label metric result
    """
    labelName: Optional[str] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    accuracy: Optional[float] = None


class InferenceLabelMetric(BaseModel):
    """
    Inference label metric
    """
    name: Optional[str] = None  # labelMetric
    displayName: Optional[str] = None
    result: Optional[List[InferenceLabelMetricResult]] = None


class InferenceMetric(BaseMetric):
    """
    Label statistics metric
    """
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[InferenceLabelMetric]]] = None


class ConfusionMatrixAnnotationSpec(BaseModel):
    """
    Confusion Matrix Result
    """
    id: Optional[int] = None
    labelName: Optional[str] = None


class ConfusionMatrixRow(BaseModel):
    """
    Confusion Matrix Result
    """
    row: Optional[List[int]] = None


class ConfusionMatrixMetricResult(BaseModel):
    """
    Confusion Matrix Result
    """
    lowerBound: Optional[int] = None
    upperBound: Optional[int] = None
    annotationSpecs: Optional[List[ConfusionMatrixAnnotationSpec]] = None
    rows: Optional[List[ConfusionMatrixRow]] = None


class ConfusionMatrixMetric(BaseModel):
    """
    Confusion Matrix
    """
    name: Optional[str] = None  # confusionMatrix
    displayName: Optional[str] = None
    result: Optional[ConfusionMatrixMetricResult] = None


class LabelMetricResult(BaseModel):
    """
    Metric result
    """
    labelName: Optional[str] = None
    result: Optional[float] = None


class AnnotationRatioMetricResult(BaseModel):
    """
    Annotation Ratio
    """
    labelName: Optional[str] = None
    imageCount: Optional[Union[int, List[LabelMetricResult]]] = None
    annotatedImageCount: Optional[Union[int, List[LabelMetricResult]]] = None
    ratio: Optional[Union[float, List[LabelMetricResult]]] = None


class LabelAnnotationRatio(BaseModel):
    """
    Annotation Ratio for a specific label
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: List[AnnotationRatioMetricResult]


class ImageAnnotationRatioMetric(BaseModel):
    """
    Image Annotation Ratio Metric
    """
    labels: Optional[List[Label]] = None
    metrics: List[LabelAnnotationRatio] = None
