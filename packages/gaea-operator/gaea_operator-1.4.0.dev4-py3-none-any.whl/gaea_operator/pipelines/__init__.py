#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__init__.py
"""
from gaea_operator.pipelines.ocrnet_pipeline.pipeline import pipeline as ocrnet_pipeline
from gaea_operator.pipelines.ppyoloe_plus_pipeline.pipeline import pipeline as ppyoloe_plus_pipeline
from gaea_operator.pipelines.resnet_pipeline.pipeline import pipeline as resnet_pipeline
from gaea_operator.pipelines.change_ppyoloe_plus_pipeline.pipeline import pipeline as change_ppyoloe_plus_pipeline
from gaea_operator.pipelines.change_ocrnet_pipeline.pipeline import pipeline as change_ocrnet_pipeline
from gaea_operator.pipelines.codetr_pipeline.pipeline import pipeline as codetr_pipeline
from gaea_operator.pipelines.dbnet_pipeline.pipeline import pipeline as dbnet_pipeline
from gaea_operator.pipelines.svtr_lcnet_pipeline.pipeline import pipeline as svtr_lcnet_pipeline
from gaea_operator.pipelines.cvresnet_pipeline.pipeline import pipeline as cvresnet_pipeline
from gaea_operator.pipelines.yoloseg_pipeline.pipeline import pipeline as yoloseg_pipeline

category_to_ppls = {
    "Image/SemanticSegmentation": [ocrnet_pipeline],
    "Image/ObjectDetection": [ppyoloe_plus_pipeline, codetr_pipeline],
    "Image/ImageClassification/OneClass": [resnet_pipeline],
    "Image/ChangeDetection/ObjectDetection": [change_ppyoloe_plus_pipeline],
    "Image/ChangeDetection/SemanticSegmentation": [change_ocrnet_pipeline],
    "Image/OCR": [svtr_lcnet_pipeline],
    "Image/TextDetection": [dbnet_pipeline],
    "Image/ImageClassification/MultiTask": [cvresnet_pipeline],
    "Image/InstanceSegmentation": [yoloseg_pipeline],
}

name_to_display_name = {
    "ocrnet": "通用语义分割模型",
    "ppyoloe_plus": "通用目标检测模型",
    "resnet": "轻量级分类模型",
    "change_ppyoloe_plus": "通用变化检测模型",
    "change_ocrnet": "通用变化分割模型",
    "codetr": "高精度目标检测模型",
    "svtr_lcnet": "文字识别模型",
    "dbnet": "文字检测模型",
    "cvresnet": "图像分类多任务模型",
    "yoloseg": "实例分割模型",
}

name_to_local_name = {
    "ocrnet": "SemanticSegmentation",
    "ppyoloe_plus": "ObjectDetection",
    "resnet": "LightClassification",
    "change_ppyoloe_plus": "ChangeObjectDetection",
    "change_ocrnet": "ChangeSemanticSegmentation",
    "codetr": "HighPrecisionObjectDetection",
    "svtr_lcnet": "OCR",
    "dbnet": "TextDetection",
    "cvresnet": "MultiTaskClassification",
    "yoloseg": "InstanceSegmentation",
}
