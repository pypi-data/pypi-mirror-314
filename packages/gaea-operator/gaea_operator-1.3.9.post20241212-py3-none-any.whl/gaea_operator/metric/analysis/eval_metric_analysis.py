#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : eval_metric.py
"""
import os
from typing import List, Dict, Union
from collections import defaultdict
import math
import bcelogger

from gaea_operator.utils import write_file
from gaea_operator.dataset import Dataset, CocoDataset
from gaea_operator.metric.operator import MeanAveragePrecision, \
    BboxConfusionMatrix, \
    Accuracy, \
    PrecisionRecallF1score, \
    ConfusionMatrix, \
    MeanIoU, \
    PrecisionRecallAccuracy, \
    PixelAccuracy, \
    PrecisionRecallHmean, \
    MaskConfusionMatrix
from gaea_operator.metric.types.metric import BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME, \
    CONFUSION_MATRIX_METRIC_NAME, \
    BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME, \
    BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME, \
    BOUNDING_BOX_LABEL_METRIC_NAME, \
    ConfusionMatrixMetric, \
    ConfusionMatrixMetricResult, \
    ConfusionMatrixAnnotationSpec, \
    ConfusionMatrixRow, \
    CLASSIFICATION_LABEL_PRECISION_METRIC_NAME, \
    CLASSIFICATION_ACCURACY_METRIC_NAME, \
    SEMANTIC_SEGMENTATION_MIOU_METRIC_NAME, \
    SEMANTIC_SEGMENTATION_LABEL_IOU_METRIC_NAME, \
    PACC_METRIC_NAME, \
    BOUNDING_BOX_CONFUSION_MATRIX_METRIC_NAME, \
    INSTANCE_SEG_CONFUSION_MATRIX_METRIC_NAME, \
    INSTANCE_SEG_LABEL_METRIC_NAME, \
    INSTANCE_SEG_LABEL_AVERAGE_PRECISION_METRIC_NAME, \
    INSTANCE_SEG_MEAN_AVERAGE_PRECISION_METRIC_NAME, \
    INSTANCE_SEG_MEAN_AVERAGE_RECALL_METRIC_NAME
from gaea_operator.metric.types.text_detection_metric import PrecisionMetric, \
    RecallMetric, \
    HarmonicMeanMetric, \
    TextDetectionMetric
from gaea_operator.metric.types.ocr_metric import OCRMetric
from gaea_operator.metric.types.object_detection_metric import ObjectDetectionMetric, \
    BoundingBoxMeanAveragePrecision, \
    BoundingBoxMeanAverageRecall, \
    BoundingBoxLabelAveragePrecision, \
    BoundingBoxLabelAveragePrecisionResult, \
    BoundingBoxLabelMetric, \
    BoundingBoxLabelMetricResult, \
    BoundingBoxLabelConfidenceMetric
from gaea_operator.metric.types.image_classification_metric import ImageClassificationMetric, \
    LabelPrecisionMetric, \
    LabelPrecisionMetricResult, \
    AccuracyMetric, \
    MultiAttributeImageClassificationMetric, \
    SingleAttrImageClassificationMetric
from gaea_operator.metric.types.semantic_segmentation_metric import SemanticSegmentationMetric, \
    LabelIntersectionOverUnionMetric, \
    LabelIntersectionOverUnionMetricResult, \
    MeanIntersectionOverUnionMetric, \
    PixelAccuracyMetric
from gaea_operator.metric.types.instance_segmentation_metric import InstanceSegmentationMetric, \
    SegLabelMetric, \
    SegLabelAveragePrecision, \
    SegLabelAveragePrecisionResult, \
    SegLabelMetricResult, \
    SegLabelConfidenceMetric, \
    SegMeanAveragePrecision, \
    SegMeanAverageRecall


class EvalMetricAnalysis(object):
    """
    Evaluation metric analysis.
    """

    def __init__(self,
                 category: str,
                 labels: List = None,
                 images: List[Dict] = None,
                 conf_threshold: float = 0,
                 iou_threshold: float = 0.5):
        self.labels = labels
        self.images = images
        self.category = category
        self.data_format_valid = True
        self.conf_threshold = float(conf_threshold)
        self.iou_threshold = float(iou_threshold)

        self.image_dict = {}
        self.img_id_str2int = {}
        self.labels = []
        self.label_id2index: Union[dict, list] = []
        self.label_index2id: Union[dict, list] = []
        self.label_id2name: Union[dict, list] = []
        self.label_index2name: Union[dict, list] = []
        self.metric = []
        self.format_input = None
        self.format_result = None

        # 标准化任务
        self.task_labels = defaultdict(lambda: defaultdict(list))

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        if self.category in ("Image/ImageClassification/MultiTask",):
            for item in self.metric:
                for metric in item:
                    metric.reset()
        else:
            for metric in self.metric:
                metric.reset()
        self.data_format_valid = True

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        if images is None:
            return
        self.images = images
        self.image_dict = {item["image_id"]: item for item in images}
        self.img_id_str2int = {key: idx + 1 for idx, key in enumerate(self.image_dict)}

    def _set_semantic_segmentation(self):
        if len(self.labels) > 0 and self.labels[0]["id"] == 0 and self.labels[0]["name"] == "背景":
            return
        self.labels.insert(0, {"id": 0, "name": "背景"})

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        if labels is None:
            return

        if self.category in ("Image/ImageClassification/MultiTask",):
            # 构建 key 为 parentID，value 为 单任务 labels 的字典
            ## 处理每个属性
            for label in labels:
                if label.get('parentID') == '' or label.get('parentID') is None:
                    task_id = label['id']
                    label_name = label['name']
                    # 自动为 task_id 初始化 label_name 和嵌套的空列表
                    self.task_labels[task_id]['label_name'] = label_name
                else:
                    parent_id = label['parentID']
                    # 自动为 parent_id 初始化 labels 列表
                    self.task_labels[parent_id]['labels'].append(label)
            for task_id, item in self.task_labels.items():
                self.labels.append([{"id": int(label["id"]), "name": label["name"]} for label in item['labels']])
                self.label_id2index.append({label["id"]: idx for idx, label in enumerate(item['labels'])})
                self.label_index2id.append({idx: label["id"] for idx, label in enumerate(item['labels'])})
                self.label_id2name.append({label["id"]: label["name"] for label in item['labels']})
                self.label_index2name.append({idx: label["name"] for idx, label in enumerate(item['labels'])})
        elif self.category in ("Image/SemanticSegmentation", "Image/ChangeDetection/SemanticSegmentation"):
            self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
            self._set_semantic_segmentation()

            self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
            self.label_index2id = {idx: label["id"] for idx, label in enumerate(self.labels)}
            self.label_id2name = {label["id"]: label["name"] for label in self.labels}
            self.label_index2name = {idx: label["name"] for idx, label in enumerate(self.labels)}
        else:
            self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
            self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
            self.label_index2id = {idx: label["id"] for idx, label in enumerate(self.labels)}
            self.label_id2name = {label["id"]: label["name"] for label in self.labels}
            self.label_index2name = {idx: label["name"] for idx, label in enumerate(self.labels)}

        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        if self.category in ("Image/ObjectDetection", "Image/ChangeDetection/ObjectDetection"):
            self.metric = [MeanAveragePrecision(labels=self.labels,
                                                num_classes=len(self.labels),
                                                classwise=True),
                           BboxConfusionMatrix(labels=self.labels,
                                               conf_threshold=self.conf_threshold,
                                               iou_threshold=self.iou_threshold,
                                               num_classes=len(self.labels))]
            self.format_input = self._format_to_object_detection
            self.format_result = self._format_object_detection_result
        elif self.category in ("Image/ImageClassification/MultiClass", "Image/ImageClassification/OneClass"):
            self.metric = [Accuracy(num_classes=len(self.labels)),
                           PrecisionRecallF1score(num_classes=len(self.labels), average="none"),
                           ConfusionMatrix(num_classes=len(self.labels))]
            self.format_input = self._format_to_classification
            self.format_result = self._format_classification_result
        elif self.category in ("Image/ImageClassification/MultiTask",):
            # 所有任务的平均 ACC
            self.metric = [[Accuracy(num_classes=len(self.task_labels))]]

            # 所有任务的 ACC, PRC, CM
            for task_id, task_item in self.task_labels.items():
                task_labels = task_item['labels']
                self.metric.append([
                    Accuracy(num_classes=len(task_labels)),
                    PrecisionRecallF1score(num_classes=len(task_labels), average="none"),
                    ConfusionMatrix(num_classes=len(task_labels))])

            self.format_input = self._format_to_multitask_classification
            self.format_result = self._format_multitask_classification_result
        elif self.category in ("Image/SemanticSegmentation", "Image/ChangeDetection/SemanticSegmentation"):
            self.metric = [MeanIoU(num_classes=len(self.labels)), PixelAccuracy(num_classes=len(self.labels))]
            self.format_input = self._format_to_semantic_segmentation
            self.format_result = self._format_semantic_segmentation_result
        elif self.category in ("Image/TextDetection",):
            self.metric = [PrecisionRecallHmean(conf_threshold=self.conf_threshold,
                                                iou_threshold=self.iou_threshold,
                                                num_classes=len(self.labels))]
            self.format_input = self._format_to_text_detection
            self.format_result = self._format_to_text_detection_result
        elif self.category in ("Image/OCR",):
            self.metric = [PrecisionRecallAccuracy(labels=self.labels,
                                                   num_classes=len(self.labels), average="none")]
            self.format_input = self._format_to_ocr
            self.format_result = self._format_to_ocr_result
        elif self.category in ("Image/InstanceSegmentation",):
            self.metric = [MeanAveragePrecision(labels=self.labels,
                                                num_classes=len(self.labels),
                                                classwise=True),
                           BboxConfusionMatrix(labels=self.labels,
                                               conf_threshold=self.conf_threshold,
                                               iou_threshold=self.iou_threshold,
                                               num_classes=len(self.labels)),
                           MaskConfusionMatrix(labels=self.labels,
                                               conf_threshold=self.conf_threshold,
                                               iou_threshold=self.iou_threshold,
                                               num_classes=len(self.labels))]
            self.format_input = self._format_to_instance_segment
            self.format_result = self._format_instance_segment_result
        else:
            raise ValueError(f"Unknown category: {self.category}")

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        if predictions is None or references is None:
            bcelogger.warning(f"Predictions {type(predictions)} or references {type(references)} is None.")
            self.data_format_valid = False
            return

        predictions, references = self.format_input(predictions, references)

        if self.category in ("Image/ImageClassification/MultiTask",):
            for index, task_metric in enumerate(self.metric):
                for metric in task_metric:
                    metric.update(predictions=predictions[index], references=references[index])
        else:
            for metric in self.metric:
                metric.update(predictions=predictions, references=references)

    def _format_to_object_detection(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to object detection metric.
        """
        references = CocoDataset.coco_annotation_from_vistudio_v1(annotations=references)
        predictions = CocoDataset.coco_annotation_from_vistudio_v1(annotations=predictions)

        reference_dict = defaultdict(list)
        for item in references:
            # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
            if "category_id" in item and item["category_id"] not in self.label_id2index:
                continue
            im_id = item["image_id"]
            img = self.image_dict[im_id]
            im_id_int = self.img_id_str2int[im_id]
            item["width"] = img["width"]
            item["height"] = img["height"]
            item["image_id"] = im_id_int
            reference_dict[im_id_int].append(item)

        new_predictions = []
        prediction_img_set = set()
        for item in predictions:
            im_id = item["image_id"]
            img = self.image_dict[im_id]
            im_id_int = self.img_id_str2int[im_id]
            # 只有同时拥有gt和预测结果才参与指标计算
            if im_id_int not in reference_dict:
                continue
            # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
            if "category_id" in item and item["category_id"] not in self.label_id2index:
                continue
            prediction_img_set.add(im_id_int)
            item["width"] = img["width"]
            item["height"] = img["height"]
            item["image_id"] = im_id_int
            new_predictions.append(item)

        new_references = []
        for im_id_int, anno in reference_dict.items():
            if im_id_int in prediction_img_set:
                new_references.extend(reference_dict[im_id_int])
        bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")

        return {"bbox": new_predictions}, {"bbox": new_references}

    def _format_object_detection_result(self, metric_result: Dict):
        metric = ObjectDetectionMetric(labels=self.labels, metrics=[])
        bbox_metric_result = metric_result[MeanAveragePrecision.global_name()]
        bounding_box_mean_average_precision = BoundingBoxMeanAveragePrecision(
            name=BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME,
            displayName="AP50指标",
            result=bbox_metric_result["bbox"][1])
        bounding_box_mean_average_recall = BoundingBoxMeanAverageRecall(
            name=BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME,
            displayName="AR50指标",
            result=bbox_metric_result["bbox"][8])
        bounding_box_label_average_precision = BoundingBoxLabelAveragePrecision(
            name=BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME,
            displayName="类别AP结果",
            result=[])
        confusion_matrix = ConfusionMatrixMetric(
            name=CONFUSION_MATRIX_METRIC_NAME,
            displayName="混淆矩阵",
            result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        bounding_box_label_metric = BoundingBoxLabelMetric(name=BOUNDING_BOX_LABEL_METRIC_NAME,
                                                           displayName="PR曲线",
                                                           result=[])
        for item in bbox_metric_result["bbox_results_per_label"]:
            bounding_box_label_average_precision.result.append(
                BoundingBoxLabelAveragePrecisionResult(labelName=item["labelName"],
                                                       averagePrecision=item["averagePrecision"]))
        for item in bbox_metric_result["pr_curve"]:
            bounding_box_label_metric_result = BoundingBoxLabelMetricResult(labelName=item[0],
                                                                            iouThreshold=0.5,
                                                                            averagePrecision=item[1],
                                                                            confidenceMetrics=[])
            for idx, p in enumerate(item[2]):
                bounding_box_label_metric_result.confidenceMetrics.append(
                    BoundingBoxLabelConfidenceMetric(
                        precision=p,
                        recall=item[3][idx]))
            bounding_box_label_metric.result.append(bounding_box_label_metric_result)
        lower_bound, upper_bound = 0, 0
        for idx, item in enumerate(metric_result[BboxConfusionMatrix.global_name()]):
            lower_bound = min(lower_bound, min(item))
            upper_bound = max(upper_bound, max(item))
            if idx not in self.label_index2id:
                label_id = max(self.label_index2id.values()) + 1
                label_name = "背景图"
            else:
                label_id = self.label_index2id[idx]
                label_name = self.label_index2name[idx]
            annotation_spec = ConfusionMatrixAnnotationSpec(id=label_id, labelName=label_name)
            row = ConfusionMatrixRow(row=item)
            confusion_matrix.result.annotationSpecs.append(annotation_spec)
            confusion_matrix.result.rows.append(row)
            confusion_matrix.result.lowerBound = lower_bound
            confusion_matrix.result.upperBound = upper_bound

        metric.metrics.extend([bounding_box_mean_average_precision,
                               bounding_box_mean_average_recall,
                               bounding_box_label_average_precision,
                               bounding_box_label_metric,
                               confusion_matrix])
        return metric.dict()

    def _format_to_classification(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to classification metric.
        """
        reference_dict = defaultdict(list)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 分类模型必须有标注，没有标注的跳过
            if item.get("annotations") is None:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][0]["id"], str):
                anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
            if anno["labels"][0]["id"] is None or math.isnan(anno["labels"][0]["id"]):
                continue
            # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
            if anno["labels"][0]["id"] not in self.label_id2index:
                continue
            index = self.label_id2index[anno["labels"][0]["id"]]
            reference_dict[im_id_int].append(index)

        prediction_dict = defaultdict(list)
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if item.get("annotations") is None or im_id_int not in reference_dict:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][0]["id"], str):
                anno["labels"][0]["id"] = int(anno["labels"][0]["id"])
            if anno["labels"][0]["id"] is None or math.isnan(anno["labels"][0]["id"]):
                continue
            # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
            if anno["labels"][0]["id"] not in self.label_id2index:
                continue
            index = self.label_id2index[anno["labels"][0]["id"]]
            prediction_dict[im_id_int].append(index)

        new_references = []
        new_predictions = []
        for img_id, anno in reference_dict.items():
            # 只有同时拥有gt和预测结果才参与指标计算
            if img_id in prediction_dict:
                new_references.extend(anno)
                new_predictions.extend(prediction_dict[img_id])
        bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")

        return new_predictions, new_references

    def _format_classification_result(self, metric_result: Dict):
        metric = ImageClassificationMetric(labels=self.labels, metrics=[])
        accuracy_metric = AccuracyMetric(name=CLASSIFICATION_ACCURACY_METRIC_NAME,
                                         displayName="准确率",
                                         result=metric_result[Accuracy.global_name()])
        label_precision_metric = LabelPrecisionMetric(name=CLASSIFICATION_LABEL_PRECISION_METRIC_NAME,
                                                      displayName="类别精确率",
                                                      result=[])
        confusion_matrix = ConfusionMatrixMetric(name=CONFUSION_MATRIX_METRIC_NAME,
                                                 displayName="混淆矩阵",
                                                 result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        precisions = metric_result[PrecisionRecallF1score.global_name()][0]
        recalls = metric_result[PrecisionRecallF1score.global_name()][1]
        for idx, precision in enumerate(precisions):
            label_precision_metric.result.append(LabelPrecisionMetricResult(labelName=self.label_index2name[idx],
                                                                            precision=precision,
                                                                            recall=recalls[idx]))

        for idx, item in enumerate(metric_result[ConfusionMatrix.global_name()]):
            annotation_spec = ConfusionMatrixAnnotationSpec(id=self.label_index2id[idx],
                                                            labelName=self.label_index2name[idx])
            row = ConfusionMatrixRow(row=item)
            confusion_matrix.result.annotationSpecs.append(annotation_spec)
            confusion_matrix.result.rows.append(row)

        metric.metrics.extend([accuracy_metric, label_precision_metric, confusion_matrix])

        return metric.dict()

    def _format_to_singletask_classification(self, predictions: List[Dict], references: List[Dict], task_index: int):
        """
        参考 _format_to_classification 对单任务进行格式化
        """
        reference_dict = defaultdict(list)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 分类模型必须有标注，没有标注的跳过
            if item.get("annotations") is None:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][task_index]["id"], str):
                anno["labels"][task_index]["id"] = int(anno["labels"][task_index]["id"])
            if anno["labels"][task_index]["id"] is None or math.isnan(anno["labels"][task_index]["id"]):
                continue
            # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
            if anno["labels"][task_index]["id"] not in self.label_id2index[task_index]:
                continue
            index = self.label_id2index[task_index][anno["labels"][task_index]["id"]]
            reference_dict[im_id_int].append(index)

        prediction_dict = defaultdict(list)
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if item.get("annotations") is None or im_id_int not in reference_dict:
                continue
            anno = item["annotations"][0]
            if isinstance(anno["labels"][task_index]["id"], str):
                anno["labels"][task_index]["id"] = int(anno["labels"][task_index]["id"])
            if anno["labels"][task_index]["id"] is None or math.isnan(anno["labels"][task_index]["id"]):
                continue
            # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
            if anno["labels"][task_index]["id"] not in self.label_id2index[task_index]:
                continue
            index = self.label_id2index[task_index][anno["labels"][task_index]["id"]]
            prediction_dict[im_id_int].append(index)

        new_references = []
        new_predictions = []
        for img_id, anno in reference_dict.items():
            # 只有同时拥有gt和预测结果才参与指标计算
            if img_id in prediction_dict:
                new_references.extend(anno)
                new_predictions.extend(prediction_dict[img_id])
        bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")

        return new_predictions, new_references

    def _format_to_multitask_classification(self, predictions: List[Dict], references: List[Dict]):
        """
        会将 predictions 和 references 按照多任务的形式进行格式化
        多属性的示例数据如下：
        predictions[0]: {
            'doc_type': 'annotation',
            'artifact_name': 'ensemble',
            'task_kind': 'Model',
            'image_id': 'adcddba2bb146fcf0d5fcd7b75f90e14',
            'annotations': [{
                'id': 1,
                'bbox': [0, 0, 0, 0],
                'segmentation': [],
                'labels': [{
                    'id': '13',
                    'confidence': 1.0
                }, {
                    'id': '12',
                    'confidence': 1.0
                }],
                'area': 0
            }]
        }
        references[0]: {
            'file_name': '/home//V2Xguangzhou136_20230615000000-camera1-1686841113252574976-439296_0.33_1.jpg',
            'text': '/home/V2Xguangzhou136_20230615000000-camera1-1686841113252574976-439296_0.33_1.jpg -1 -1 12',
            'image_id': 'bcc9afb737c6c6a196a2e891d58e8645',
            'annotations': [{
                'id': 1,
                'labels': [{
                    'id': '12',
                    'confidence': 1
                }, {
                    'id': '12',
                    'confidence': 1
                }]
            }]
        },
        """

        # 用与返回的 format 后的结果
        new_predictions = []
        new_references = []

        # 将所有任务进行汇总的结果，用于评测所有任务的平均 ACC
        total_predictions = []
        total_references = []

        for task_id, task_item in self.task_labels.items():
            format_predictions, format_references = self._format_to_singletask_classification(
                predictions, references, task_id)

            new_predictions.append(format_predictions)
            new_references.append(format_references)

            total_predictions.extend(format_predictions)
            total_references.extend(format_references)

        # 将汇总的结果放在第 0 个
        new_predictions.insert(0, total_predictions)
        new_references.insert(0, total_references)

        return new_predictions, new_references

    def _format_multitask_classification_result(self, metric_result: Dict):
        """
        多属性分类任务指标格式化
        """

        # 所有任务的平均 ACC
        total_accuracy = AccuracyMetric(
            name='accuracy', displayName='Acc', result=metric_result[0][Accuracy.global_name()])
        label_names = [
            {'id': task_id, 'name': task_item['label_name']}
            for task_id, task_item in self.task_labels.items()]
        multitask_class_schema_metric = MultiAttributeImageClassificationMetric(
            metrics=[total_accuracy], labels=label_names)

        # 每个任务的指标
        for task_id, task_item in self.task_labels.items():

            label_names = task_item['labels']
            class_schema_metric = SingleAttrImageClassificationMetric(labels=label_names, metrics=[])

            accuracy_metric = AccuracyMetric(name=CLASSIFICATION_ACCURACY_METRIC_NAME,
                                             displayName="准确率",
                                             result=metric_result[task_id + 1][Accuracy.global_name()])
            label_precision_metric = LabelPrecisionMetric(name=CLASSIFICATION_LABEL_PRECISION_METRIC_NAME,
                                                          displayName="类别精确率",
                                                          result=[])
            confusion_matrix = ConfusionMatrixMetric(name=CONFUSION_MATRIX_METRIC_NAME,
                                                     displayName="混淆矩阵",
                                                     result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
            precisions = metric_result[task_id + 1][PrecisionRecallF1score.global_name()][0]
            recalls = metric_result[task_id + 1][PrecisionRecallF1score.global_name()][1]
            for idx, precision in enumerate(precisions):
                label_precision_metric.result.append(
                    LabelPrecisionMetricResult(
                        labelName=self.label_index2name[task_id][idx],
                        precision=precision,
                        recall=recalls[idx]))

            for idx, item in enumerate(metric_result[task_id + 1][ConfusionMatrix.global_name()]):
                annotation_spec = ConfusionMatrixAnnotationSpec(id=self.label_index2id[task_id][idx],
                                                                labelName=self.label_index2name[task_id][idx])
                row = ConfusionMatrixRow(row=item)
                confusion_matrix.result.annotationSpecs.append(annotation_spec)
                confusion_matrix.result.rows.append(row)

            class_schema_metric.metrics.extend([accuracy_metric, label_precision_metric, confusion_matrix])
            multitask_class_schema_metric.metrics.append(class_schema_metric)

        return multitask_class_schema_metric.dict()

    def _format_to_semantic_segmentation(self, predictions: List[Dict], references: List[Dict]):
        references = Dataset.mask_from_vistudio_v1(annotations=references, images=self.images, labels=self.labels)
        predictions = Dataset.mask_from_vistudio_v1(annotations=predictions, images=self.images, labels=self.labels)

        reference_dict = defaultdict(dict)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            item["image_id"] = im_id_int
            reference_dict[im_id_int] = item

        new_predictions = []
        new_references = []
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 只有同时拥有gt和预测结果才参与指标计算
            if im_id_int not in reference_dict:
                continue
            new_references.append(reference_dict[im_id_int]["mask"])
            new_predictions.append(item["mask"])
        bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")

        return new_predictions, new_references

    def _format_semantic_segmentation_result(self, metric_result: Dict):
        metric = SemanticSegmentationMetric(labels=self.labels, metrics=[])

        mean_acc_result = metric_result[PixelAccuracy.global_name()]
        pixel_accuracy = PixelAccuracyMetric(name=PACC_METRIC_NAME, displayName="像素准确率", result=mean_acc_result)

        iou_result = metric_result[MeanIoU.global_name()]
        mean_iou = MeanIntersectionOverUnionMetric(
            name=SEMANTIC_SEGMENTATION_MIOU_METRIC_NAME,
            displayName="均交并比",
            result=iou_result[0])
        label_iou = LabelIntersectionOverUnionMetric(
            name=SEMANTIC_SEGMENTATION_LABEL_IOU_METRIC_NAME,
            displayName="标签交并比",
            result=[])
        for idx, iou in enumerate(iou_result[1]):
            label_iou.result.append(LabelIntersectionOverUnionMetricResult(labelName=self.label_index2name[idx],
                                                                           iou=iou))

        metric.metrics.extend([pixel_accuracy, mean_iou, label_iou])

        return metric.dict()

    def _format_to_text_detection(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to classification metric.
        """
        # Collect references and predictions
        references = format_to_text_detection(annotations=references)
        predictions = format_to_text_detection(annotations=predictions)

        reference_dict = defaultdict(list)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            item["image_id"] = im_id_int
            reference_dict[im_id_int].append(item)

        new_predictions = []
        prediction_img_set = set()
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            # 只有同时拥有gt和预测结果才参与指标计算
            if im_id_int not in reference_dict:
                continue
            item["image_id"] = im_id_int
            prediction_img_set.add(im_id_int)
            new_predictions.append(item)

        new_references = []
        for img_id, anno in reference_dict.items():
            if img_id in prediction_img_set:
                new_references.extend(reference_dict[img_id])

        return new_predictions, new_references

    def _format_to_text_detection_result(self, metric_result: Dict):
        harmonic_mean_metric = HarmonicMeanMetric(result=metric_result[PrecisionRecallHmean.global_name()][2])
        precision_metric = PrecisionMetric(result=metric_result[PrecisionRecallHmean.global_name()][0])
        recall_metric = RecallMetric(result=metric_result[PrecisionRecallHmean.global_name()][1])
        metric = TextDetectionMetric(metrics=[precision_metric, recall_metric, harmonic_mean_metric])

        return metric.dict()

    def _format_to_ocr(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to classification metric.
        """
        reference_dict = defaultdict(str)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            annotations = item.get("annotations")
            # 模型标注必须有ocr，没有ocr的跳过
            if len(annotations) < 1 or annotations[0].get("ocr") is None:
                reference_dict[im_id_int] = ""
            else:
                word = annotations[0].get("ocr").get("word", "")
                reference_dict[im_id_int] = word

        prediction_dict = defaultdict(str)
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            annotations = item.get("annotations")
            # 模型标注必须有ocr，没有ocr的跳过
            if len(annotations) < 1 or annotations[0].get("ocr") is None:
                prediction_dict[im_id_int] = ""
            else:
                word = annotations[0].get("ocr").get("word", "")
                prediction_dict[im_id_int] = word

        new_references = []
        new_predictions = []
        for img_id, word in reference_dict.items():
            # 只有同时拥有gt和预测结果才参与指标计算
            if img_id in prediction_dict:
                new_references.append(str(word))
                new_predictions.append(prediction_dict[img_id])
        bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")

        return new_predictions, new_references

    def _format_to_ocr_result(self, metric_result: Dict):

        accuracy_metric = AccuracyMetric(name=CLASSIFICATION_ACCURACY_METRIC_NAME,
                                         displayName="准确率",
                                         result=metric_result[PrecisionRecallAccuracy.global_name()][2])
        precision_metric = PrecisionMetric(result=metric_result[PrecisionRecallAccuracy.global_name()][0])
        recall_metric = RecallMetric(result=metric_result[PrecisionRecallAccuracy.global_name()][1])
        metric = OCRMetric(labels=self.labels, metrics=[precision_metric, recall_metric, accuracy_metric])

        return metric.dict()

    def _format_to_instance_segment(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to instance segment metric.
        """
        # mask
        references_mask = CocoDataset.coco_seg_annotation_from_vistudio_v1(annotations=references)
        predictions_mask = CocoDataset.coco_seg_annotation_from_vistudio_v1(annotations=predictions)

        # bbox
        references_bbox = CocoDataset.coco_annotation_from_vistudio_v1(annotations=references)
        predictions_bbox = CocoDataset.coco_annotation_from_vistudio_v1(annotations=predictions)

        def _cvt_ref_pred(predictions: List[Dict], references: List[Dict]):
            reference_dict = defaultdict(list)
            for item in references:
                # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                if "category_id" in item and item["category_id"] not in self.label_id2index:
                    continue
                im_id = item["image_id"]
                img = self.image_dict[im_id]
                im_id_int = self.img_id_str2int[im_id]
                item["width"] = img["width"]
                item["height"] = img["height"]
                item["image_id"] = im_id_int
                reference_dict[im_id_int].append(item)

            new_predictions = []
            prediction_img_set = set()
            for item in predictions:
                im_id = item["image_id"]
                img = self.image_dict[im_id]
                im_id_int = self.img_id_str2int[im_id]
                # 只有同时拥有gt和预测结果才参与指标计算
                if im_id_int not in reference_dict:
                    continue
                # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                if "category_id" in item and item["category_id"] not in self.label_id2index:
                    continue

                prediction_img_set.add(im_id_int)
                item["width"] = img["width"]
                item["height"] = img["height"]
                item["image_id"] = im_id_int
                new_predictions.append(item)

            new_references = []
            for im_id_int, anno in reference_dict.items():
                if im_id_int in prediction_img_set:
                    new_references.extend(reference_dict[im_id_int])

            bcelogger.info(f"Prediction length: {len(new_predictions)}, reference length: {len(new_references)}")
            return new_references, new_predictions

        new_references_bbox, new_predictions_bbox = \
            _cvt_ref_pred(predictions=predictions_bbox, references=references_bbox)
        new_references_mask, new_predictions_mask = \
            _cvt_ref_pred(predictions=predictions_mask, references=references_mask)

        return {"bbox": new_predictions_bbox, "mask": new_predictions_mask}, \
            {"bbox": new_references_bbox, "mask": new_references_mask}

    def _format_instance_segment_result(self, metric_result: Dict):
        metric = InstanceSegmentationMetric(labels=self.labels, metrics=[])
        bbox_metric_result = metric_result[MeanAveragePrecision.global_name()]

        bounding_box_label_average_precision = BoundingBoxLabelAveragePrecision(
            name=BOUNDING_BOX_LABEL_AVERAGE_PRECISION_METRIC_NAME,
            displayName="矩形框 类别AP结果",
            result=[])
        seg_label_average_precision = SegLabelAveragePrecision(
            name=INSTANCE_SEG_LABEL_AVERAGE_PRECISION_METRIC_NAME,
            displayName="分隔区域 类别AP结果",
            result=[])
        confusion_matrix = ConfusionMatrixMetric(
            name=BOUNDING_BOX_CONFUSION_MATRIX_METRIC_NAME,
            displayName="混淆矩阵（矩形框）",
            result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        seg_confusion_matrix = ConfusionMatrixMetric(
            name=INSTANCE_SEG_CONFUSION_MATRIX_METRIC_NAME,
            displayName="混淆矩阵（轮廓区域）",
            result=ConfusionMatrixMetricResult(annotationSpecs=[], rows=[]))
        bounding_box_label_metric = BoundingBoxLabelMetric(name=BOUNDING_BOX_LABEL_METRIC_NAME,
                                                           displayName="矩形框 P-R曲线",
                                                           result=[])
        seg_label_metric = SegLabelMetric(name=INSTANCE_SEG_LABEL_METRIC_NAME,
                                          displayName="分隔区域 P-R曲线",
                                          result=[])
        # ap-box/seg
        bounding_box_average_precision = BoundingBoxMeanAveragePrecision(
            name=BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME,
            displayName="AP50指标",
            result=bbox_metric_result["bbox"][1])

        seg_average_precision = SegMeanAveragePrecision(
            name=INSTANCE_SEG_MEAN_AVERAGE_PRECISION_METRIC_NAME,
            displayName="AP50指标",
            result=bbox_metric_result["segm"][1])

        # ar-box/seg
        bounding_box_average_recall = BoundingBoxMeanAverageRecall(
            name=BOUNDING_BOX_MEAN_AVERAGE_RECALL_METRIC_NAME,
            displayName="AR指标",
            result=bbox_metric_result["bbox"][8])

        seg_average_recall = SegMeanAverageRecall(
            name=INSTANCE_SEG_MEAN_AVERAGE_RECALL_METRIC_NAME,
            displayName="AR指标",
            result=bbox_metric_result["segm"][8])

        # ap
        for item in bbox_metric_result["bbox_results_per_label"]:
            bounding_box_label_average_precision.result.append(
                BoundingBoxLabelAveragePrecisionResult(labelName=item["labelName"],
                                                       averagePrecision=item["averagePrecision"]))

        for item in bbox_metric_result["segm_results_per_label"]:
            seg_label_average_precision.result.append(
                SegLabelAveragePrecisionResult(labelName=item["labelName"],
                                               averagePrecision=item["averagePrecision"]))

        # pr
        for item in bbox_metric_result["pr_curve"]:
            bounding_box_label_metric_result = BoundingBoxLabelMetricResult(labelName=item[0],
                                                                            iouThreshold=0.5,
                                                                            averagePrecision=item[1],
                                                                            confidenceMetrics=[])
            for idx, p in enumerate(item[2]):
                bounding_box_label_metric_result.confidenceMetrics.append(
                    BoundingBoxLabelConfidenceMetric(
                        precision=p,
                        recall=item[3][idx]))
            bounding_box_label_metric.result.append(bounding_box_label_metric_result)

        for item in bbox_metric_result["mask_pr_curve"]:
            seg_label_metric_result = SegLabelMetricResult(labelName=item[0],
                                                           iouThreshold=0.5,
                                                           averagePrecision=item[1],
                                                           confidenceMetrics=[])
            for idx, p in enumerate(item[2]):
                seg_label_metric_result.confidenceMetrics.append(
                    SegLabelConfidenceMetric(
                        precision=p,
                        recall=item[3][idx]))
            seg_label_metric.result.append(seg_label_metric_result)

        # confusion
        if True:
            lower_bound, upper_bound = 0, 0
            for idx, item in enumerate(metric_result[BboxConfusionMatrix.global_name()]):
                lower_bound = min(lower_bound, min(item))
                upper_bound = max(upper_bound, max(item))
                if idx not in self.label_index2id:
                    label_id = max(self.label_index2id.values()) + 1
                    label_name = "背景图"
                else:
                    label_id = self.label_index2id[idx]
                    label_name = self.label_index2name[idx]
                annotation_spec = ConfusionMatrixAnnotationSpec(id=label_id, labelName=label_name)
                row = ConfusionMatrixRow(row=item)
                confusion_matrix.result.annotationSpecs.append(annotation_spec)
                confusion_matrix.result.rows.append(row)
                confusion_matrix.result.lowerBound = lower_bound
                confusion_matrix.result.upperBound = upper_bound
        if True:
            lower_bound, upper_bound = 0, 0
            for idx, item in enumerate(metric_result[MaskConfusionMatrix.global_name()]):
                lower_bound = min(lower_bound, min(item))
                upper_bound = max(upper_bound, max(item))
                if idx not in self.label_index2id:
                    label_id = max(self.label_index2id.values()) + 1
                    label_name = "背景图"
                else:
                    label_id = self.label_index2id[idx]
                    label_name = self.label_index2name[idx]
                annotation_spec = ConfusionMatrixAnnotationSpec(id=label_id, labelName=label_name)
                row = ConfusionMatrixRow(row=item)
                seg_confusion_matrix.result.annotationSpecs.append(annotation_spec)
                seg_confusion_matrix.result.rows.append(row)
                seg_confusion_matrix.result.lowerBound = lower_bound
                seg_confusion_matrix.result.upperBound = upper_bound

        metric.metrics.extend([bounding_box_label_average_precision,
                               seg_label_average_precision,
                               bounding_box_label_metric,
                               seg_label_metric,
                               confusion_matrix,
                               seg_confusion_matrix,
                               bounding_box_average_precision,
                               seg_average_precision,
                               bounding_box_average_recall,
                               seg_average_recall])
        return metric.dict()

    def compute(self):
        """
        Compute metric.
        """
        if not self.data_format_valid:
            return {}

        if self.category in ("Image/ImageClassification/MultiTask",):
            results = []
            for item in self.metric:
                item_results = {}
                for metric in item:
                    item_results[metric.name] = metric.compute()
                results.append(item_results)
        else:
            results = {}
            for metric in self.metric:
                results[metric.name] = metric.compute()

        metric_result = self.format_result(metric_result=results)

        return metric_result

    def save(self, metric_result: Dict, output_uri: str):
        """
        Save metric.
        """
        if os.path.splitext(output_uri)[1] == "":
            output_dir = output_uri
            file_name = "metric.json"
        else:
            output_dir = os.path.dirname(output_uri)
            file_name = os.path.basename(output_uri)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        write_file(obj=metric_result, output_dir=output_dir, file_name=file_name)
        bcelogger.info(f"Metric result saved to {output_uri}")

    def __call__(self, predictions: List[Dict], references: List[Dict], output_uri: str):
        self.update(predictions=predictions, references=references)
        metric_result = self.compute()

        self.save(metric_result=metric_result, output_uri=output_uri)


def format_to_text_detection(annotations: List[Dict]):
    """
    Convert the annotation from Vistudio v1 to Coco format.
    """
    anno_id = 1
    new_annotations = []
    for item in annotations:
        im_id = item["image_id"]
        if item.get("annotations") is None:
            anno = {"id": anno_id, "image_id": im_id}
            anno_id += 1
            new_annotations.append(anno)
            continue
        for anno in item["annotations"]:
            if len(anno["quadrangle"]) == 0:
                anno = {"id": anno_id, "image_id": im_id}
                anno_id += 1
                new_annotations.append(anno)
                continue
            anno["image_id"] = im_id
            new_anno = {
                "id": anno_id,
                "image_id": im_id,
                "quadrangle": anno["quadrangle"],
                "confidence": anno.get("labels", [{"confidence": 1}])[0].get("confidence", 1)
            }
            new_annotations.append(new_anno)
            anno_id += 1

    return new_annotations
