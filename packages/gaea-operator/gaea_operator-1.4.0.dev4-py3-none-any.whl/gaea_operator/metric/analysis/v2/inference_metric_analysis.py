#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/24
# @Author  : yanxiaodong
# @File    : inference.py
"""
from typing import List, Dict, Union, Set
import os
from collections import defaultdict
import numpy as np
import math

import bcelogger

from gaea_operator.utils import write_file
from gaea_operator.dataset import CocoDataset
from gaea_operator.metric.operator import \
    PrecisionRecallF1score, \
    Accuracy, \
    ConfusionMatrix, \
    MeanAveragePrecision, \
    BboxConfusionMatrix, \
    precision_recall_f1_from_confusion_matrix, \
    TPFPFNCount, \
    MultilabelConfusionMatrix
from gaea_operator.metric.types.v2.metric import MetricCategory, DisplayFormatter
from gaea_operator.metric.types.v2.inference_metric import \
    InferenceMetric, \
    InferenceSingleMetric, \
    LabelMetricResult, \
    LabelResult, \
    AnnotationSpecs, \
    InferenceLabelMetric, \
    ConfusionMatrixMetric, \
    ConfusionMatrixMetricResult, \
    ConfusionMatrixRow, \
    BoundingBoxPRCurveMetric, \
    BoundingBoxPRCurveMetricResult, \
    BoundingBoxLabelConfidenceMetric
from gaea_operator.metric.types.v2.inference_metric import \
    MetricDisplayName, \
    MetricName, \
    MetricDisplayType, \
    MetricDescription


class InferenceMetricAnalysis(object):
    """
    Inference metric analysis.
    """

    def __init__(self,
                 labels: List = None,
                 images: List[Dict] = None,
                 conf_threshold: Union[float, List] = 0,
                 iou_threshold: Union[float, List] = 0.5):
        self.iou_threshold = iou_threshold
        self.conf_threshold = conf_threshold

        self.labels = []
        self.calculate_metric = {}

        self.image_dict: Dict[int, Dict] = defaultdict(dict)
        self.img_id_str2int: Dict[str, int] = {}
        self.label_sum = 0
        self.label_ids: Dict[int, List] = defaultdict(list)

        self.label_id2index: Dict[int, int] = {}
        self.label_index2id: Dict[int, int] = {}
        self.label_inner_id2index: Dict[int, Dict] = defaultdict(dict)
        self.label_id2name: Dict[int, str] = {}
        self.label_inner_id2name: Dict[int, Dict] = defaultdict(dict)
        self.metric: Dict[str, Dict] = defaultdict(dict)

        self.confusion_matrix_id2index: Dict[int, int] = {}
        self.confusion_matrix_id2name: Dict[int, str] = {}
        self.confusion_matrix_index2id: Dict[int, int] = {}

        self.data_format_valid = True

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        for _, metric_dict in self.metric.items():
            for _, metric_list in metric_dict.items():
                for metric in metric_list:
                    metric.reset()
        self.data_format_valid = True

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        if images is None:
            return
        self.image_dict = {item["image_id"]: item for item in images}
        self.img_id_str2int = {key: idx + 1 for idx, key in enumerate(self.image_dict)}

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        if labels is None:
            return

        index = 0
        confusion_matrix_index = 0
        for label in labels:
            label["id"] = int(label["id"])
            if label.get('parentID') == '' or label.get('parentID') is None:
                label["parentID"] = None
                self.label_ids[label["id"]].append({"id": label["id"], "index": index, "parent_id": -1})
                self.label_id2index[label["id"]] = index
                self.label_index2id[index] = label["id"]
                self.label_id2name[label["id"]] = label["name"]

                self.confusion_matrix_id2index[label["id"]] = confusion_matrix_index
                self.confusion_matrix_id2name[label["id"]] = label["name"]
                self.confusion_matrix_index2id[confusion_matrix_index] = label["id"]
                confusion_matrix_index += 1
            else:
                label["parentID"] = int(label["parentID"])
                self.label_ids[label["parentID"]].append({"id": label["id"],
                                                          "index": index,
                                                          "parent_id": label["parentID"]})
                self.label_inner_id2index[label["parentID"]].update({label["id"]: index})
                self.label_inner_id2name[label["parentID"]].update({label["id"]: label["name"]})
            index += 1
            self.labels.append(label)
        bcelogger.info(f"Set labels: {self.labels}")
        bcelogger.info(f"Set label ids: {self.label_ids}")

        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        # 初始化metric[图片]
        for idx, label in self.label_ids.items():
            for item in label:
                if item["parent_id"] == -1 and len(label) >= 2:
                    _metric = [Accuracy(num_classes=len(label) - 1, thresholds=self.conf_threshold),
                               ConfusionMatrix(num_classes=len(label) - 1, thresholds=self.conf_threshold)]
                    self.metric[MetricCategory.category_image.value].update({item["index"]: _metric})
                    continue
                _metric = [Accuracy(num_classes=2, thresholds=self.conf_threshold),
                           PrecisionRecallF1score(num_classes=2, thresholds=self.conf_threshold),
                           TPFPFNCount(num_classes=2, thresholds=self.conf_threshold)]
                self.metric[MetricCategory.category_image.value].update({item["index"]: _metric})
        if self.confusion_matrix_id2index == self.label_id2index:
            _metric = [MultilabelConfusionMatrix(num_classes=len(self.confusion_matrix_id2index),
                                                 thresholds=self.conf_threshold)]
            self.metric[MetricCategory.category_image.value].update({MetricName.image_confusion_matrix.value: _metric})
        self.calculate_metric[MetricCategory.category_image.value] = True

        # 初始化metric[框]
        _metric = [MeanAveragePrecision(labels=self.labels,
                                        num_classes=len(self.label_ids),
                                        iou_threshold=self.iou_threshold,
                                        classwise=True),
                   BboxConfusionMatrix(labels=self.labels,
                                       conf_threshold=self.conf_threshold,
                                       iou_threshold=self.iou_threshold,
                                       num_classes=len(self.confusion_matrix_id2index))]
        self.metric[MetricCategory.category_bbox.value].update({MetricName.bounding_box_metric.value: _metric})
        self.calculate_metric[MetricCategory.category_bbox.value] = True

        # 初始化metric[ocr]

        bcelogger.info(f"Set metric: {self.metric}")

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        if predictions is None or references is None:
            bcelogger.warning(f"Predictions {type(predictions)} or references {type(references)} is None.")
            self.data_format_valid = False
            return

        for category, metric_dict in self.metric.items():
            if category == MetricCategory.category_image.value:
                format_predictions, format_references = self._format_input_to_image(predictions, references)
                if format_predictions.size == 0 and format_references.size == 0:
                    bcelogger.info(f"No data found in {MetricCategory.category_image.value} and "
                                   f"it will skip calculation {metric_dict}")
                    self.calculate_metric[category] = False
                    continue
            elif category == MetricCategory.category_bbox.value:
                format_predictions, format_references = self._format_input_to_bounding_box(predictions, references)
                if len(format_predictions["bbox"]) == 0 and len(format_references["bbox"]) == 0:
                    bcelogger.info(f"No data found in {MetricCategory.category_bbox.value} and "
                                   f"it will skip calculation {metric_dict}")
                    self.calculate_metric[category] = False
                    continue
            else:
                raise ValueError(f"Unknown category: {category}")

            for index, metric_list in metric_dict.items():
                if index == MetricName.image_confusion_matrix.value:
                    new_predictions = format_predictions[:, list(self.label_id2index.values())]
                    new_references = format_references[:, list(self.label_id2index.values())]
                    ids = list(self.label_id2index.keys())
                    new_index = [self.confusion_matrix_id2index[id_] for id_ in ids]
                    new_predictions, new_references = new_predictions[:, new_index], new_references[:, new_index]
                elif index == MetricName.bounding_box_metric.value:
                    new_predictions, new_references = format_predictions, format_references
                else:
                    new_predictions, new_references = format_predictions[:, index], format_references[:, index]

                for metric in metric_list:
                    metric.update(predictions=new_predictions, references=new_references)

    def _format_input_to_image(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to image input.
        """
        self.label_sum = sum([len(label) for _, label in self.label_ids.items()])

        reference_dict: Dict[int, List] = defaultdict(list)
        image2task_id_dict: Dict[int, Set] = defaultdict(set)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            array_item = np.zeros(self.label_sum, dtype=np.int8)

            if item.get("annotations") is None:
                reference_dict[im_id_int].append(array_item)
                continue

            exist_label = True
            for anno in item["annotations"]:
                if "labels" not in anno or len(anno["labels"]) == 0:
                    exist_label = False
                    continue

                for idx in range(len(anno["labels"])):
                    label = anno["labels"][idx]

                    if label.get("parent_id") == "" or label.get("parent_id") is None:
                        label.pop("parent_id", None)

                    if isinstance(label["id"], str):
                        label["id"] = int(label["id"])
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if "parent_id" not in label and label["id"] not in self.label_id2index:
                        continue
                    if "parent_id" in label and isinstance(label["parent_id"], str):
                        label["parent_id"] = int(label["parent_id"])
                    # 如果多属性标注属性id等于-1,则跳过
                    if "parent_id" in label and label["id"] == -1:
                        image2task_id_dict[im_id_int].add(label["parent_id"])
                        array_item[self.label_id2index[label["parent_id"]]] = -1
                        continue
                    # 如果多属性标注属性id不在label,则跳过
                    if "parent_id" in label and \
                            label["id"] not in self.label_inner_id2index[label["parent_id"]]:
                        continue

                    if "parent_id" in label:
                        array_item[self.label_inner_id2index[label["parent_id"]][label["id"]]] = 1
                        array_item[self.label_id2index[label["parent_id"]]] = label["id"]
                        continue
                    array_item[self.label_id2index[label["id"]]] = 1
            if exist_label:
                reference_dict[im_id_int].append(array_item)
        bcelogger.info(f"The number of reference images {len(reference_dict)}")

        prediction_dict: Dict[int, List] = defaultdict(list)
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            array_item = np.zeros(self.label_sum, dtype=np.int8)

            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if im_id_int not in reference_dict:
                continue
            if item.get("annotations") is None:
                prediction_dict[im_id_int].append(array_item)
                continue

            exist_label = True
            for anno in item["annotations"]:
                if "labels" not in anno or len(anno["labels"]) == 0:
                    exist_label = False
                    continue

                for idx in range(len(anno["labels"])):
                    label = anno["labels"][idx]

                    if label.get("parent_id") == "" or label.get("parent_id") is None:
                        label.pop("parent_id", None)

                    if isinstance(label["id"], str):
                        label["id"] = int(label["id"])
                    if math.isnan(label["confidence"]):
                        continue
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if "parent_id" not in label and label["id"] not in self.label_id2index:
                        continue
                    if "parent_id" in label and isinstance(label["parent_id"], str):
                        label["parent_id"] = int(label["parent_id"])
                    # 如果多属性标注属性id不在label,则跳过
                    if "parent_id" in label and \
                            label["id"] not in self.label_inner_id2index[label["parent_id"]]:
                        continue
                    if "parent_id" in label and label["parent_id"] in image2task_id_dict[im_id_int]:
                        array_item[self.label_inner_id2index[label["parent_id"]][label["id"]]] = -1
                        array_item[self.label_id2index[label["parent_id"]]] = -1
                        continue
                    if "parent_id" in label:
                        array_item[self.label_inner_id2index[label["parent_id"]][label["id"]]] = 1
                        array_item[self.label_id2index[label["parent_id"]]] = label["id"]
                        continue
                    array_item[self.label_id2index[label["id"]]] = 1
            if exist_label:
                prediction_dict[im_id_int].append(array_item)
        bcelogger.info(f"The number of prediction images {len(prediction_dict)}")

        reference_list = []
        prediction_list = []
        for img_id, anno in reference_dict.items():
            # 只有同时拥有gt和预测结果才参与指标计算
            if img_id in prediction_dict:
                reference_list.extend(anno)
                prediction_list.extend(prediction_dict[img_id])
        bcelogger.info(f"The number of prediction images after filter {len(prediction_dict)} for image format")
        bcelogger.info(f"The number of reference images after filter {len(reference_dict)} for image format")

        return np.array(prediction_list), np.array(reference_list)

    def _format_input_to_bounding_box(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to bounding box input.
        """
        references = CocoDataset.coco_annotation_from_vistudio_v1(annotations=references)
        predictions = CocoDataset.coco_annotation_from_vistudio_v1(annotations=predictions)

        reference_dict: Dict[int, list] = defaultdict(list)
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
        bcelogger.info(f"Prediction length: {len(new_predictions)} for bbox format")
        bcelogger.info(f"Reference length: {len(new_references)} for bbox format")

        return {"bbox": new_predictions}, {"bbox": new_references}

    def _format_result(self, metric_result: Dict):
        """
        Format to result.
        """
        metric = InferenceMetric(labels=self.labels, metrics=[])

        if MetricCategory.category_image.value in metric_result:
            bcelogger.info(f"The image metric result is {metric_result[MetricCategory.category_image.value]}")
            self._format_result_to_image(metric, metric_result[MetricCategory.category_image.value])
            bcelogger.info(f"The image metric result is {metric.dict(by_alias=True, exclude_none=True)}")
        if MetricCategory.category_bbox.value in metric_result:
            bcelogger.info(f"The bounding box metric result is {metric_result[MetricCategory.category_bbox.value]}")
            self._format_result_to_bounding_box(metric, metric_result[MetricCategory.category_bbox.value])
            bcelogger.info(f"The bounding box metric result is {metric.dict(by_alias=True, exclude_none=True)}")

        bcelogger.info(f"The metric is {metric.dict(by_alias=True, exclude_none=True)}")

        return metric.dict(by_alias=True, exclude_none=True)

    def _format_result_to_image(self, metric: InferenceMetric, image_metric_result: Dict):
        """
        Format to image result.
        """
        image_accuracy_list = []
        image_label_list = []
        confusion_matrix_list = []
        confusion_matrix_label_ids = []
        if MetricName.image_confusion_matrix.value in image_metric_result:
            confusion_matrix_list.append(image_metric_result[MetricName.image_confusion_matrix.value][0])

        for idx, label in self.label_ids.items():
            _image_label_results = LabelMetricResult()
            _image_label_results.precision = []
            _image_label_results.recall = []
            _image_label_results.accuracy = []
            _image_label_results.false_positive = []
            _image_label_results.false_negative = []
            _image_label_results.true_positive_rate = []

            for item in label:
                result = image_metric_result[item["index"]]
                bcelogger.info(f"The label {item} result is {result}")

                if item["parent_id"] == -1 and len(label) >= 2:
                    image_accuracy_list.append(result[0])
                    _image_label_results.accuracy = result[0]
                    confusion_matrix_list.append(result[1])
                    confusion_matrix_label_ids.append(item["id"])
                elif item["parent_id"] == -1 and len(label) == 1:
                    _image_label_results.label_name = self.label_id2name[item["id"]]
                    _image_label_results.precision = result[1][0]
                    _image_label_results.recall = result[1][1]
                    _image_label_results.false_positive = result[2][1] - result[2][0]
                    _image_label_results.false_negative = result[2][2] - result[2][0]
                    _image_label_results.true_positive_rate = result[1][1]
                    _image_label_results.accuracy = result[0]
                else:
                    _image_label_results.label_name = self.label_id2name[item["parent_id"]]

                    _set_image_label_result = [("precision", result[1][0]),
                                               ("recall", result[1][1]),
                                               ("false_positive", result[2][1] - result[2][0]),
                                               ("false_negative", result[2][2] - result[2][0]),
                                               ("true_positive_rate", result[1][1])]
                    for name, result in _set_image_label_result:
                        _image_label_result = LabelResult()
                        _image_label_result.label_name = self.label_inner_id2name[item["parent_id"]][item["id"]]
                        _image_label_result.result = result
                        getattr(_image_label_results, name).append(_image_label_result)

            image_label_list.append(_image_label_results)

        # 标签指标结果解析
        if len(image_label_list) > 0:
            image_label = InferenceLabelMetric()
            image_label.category = MetricCategory.category_image.value
            image_label.display_type = MetricDisplayType.table.value

            image_label.display_formatter = [DisplayFormatter.percentage.value,
                                             DisplayFormatter.percentage.value,
                                             DisplayFormatter.percentage.value,
                                             DisplayFormatter.int_.value,
                                             DisplayFormatter.int_.value,
                                             DisplayFormatter.percentage.value]

            image_label.column_annotation_specs = []
            annotation_specs_names = [MetricName.precision.value,
                                      MetricName.recall.value,
                                      MetricName.accuracy.value,
                                      MetricName.false_positive.value,
                                      MetricName.false_negative.value,
                                      MetricName.true_positive_rate.value]
            annotation_specs_display_names = [MetricDisplayName.precision.value,
                                              MetricDisplayName.recall.value,
                                              MetricDisplayName.accuracy.value,
                                              MetricDisplayName.false_positive.value,
                                              MetricDisplayName.false_negative.value,
                                              MetricDisplayName.true_positive_rate.value]
            annotation_specs_description = [MetricDescription.precision.value,
                                            MetricDescription.recall.value,
                                            MetricDescription.accuracy.value,
                                            MetricDescription.false_positive.value,
                                            MetricDescription.false_negative.value,
                                            MetricDescription.true_positive_rate.value]
            for idx in range(len(annotation_specs_names)):
                annotation_specs = AnnotationSpecs()
                annotation_specs.name = annotation_specs_names[idx]
                annotation_specs.display_name = annotation_specs_display_names[idx]
                annotation_specs.description = annotation_specs_description[idx]
                image_label.column_annotation_specs.append(annotation_specs)

            image_label.result = image_label_list
            metric.metrics.append(image_label)

        if len(image_accuracy_list) > 0:
            image_accuracy = InferenceSingleMetric()
            image_accuracy.name = MetricName.accuracy.value
            image_accuracy.display_name = MetricDisplayName.accuracy.value
            image_accuracy.category = MetricCategory.category_image.value
            image_accuracy.display_type = MetricDisplayType.card.value
            image_accuracy.display_formatter = DisplayFormatter.percentage.value
            image_accuracy.result = round(sum(image_accuracy_list) / len(image_accuracy_list), Accuracy.decimals)
            metric.metrics.append(image_accuracy)

        # 混淆矩阵指标结果解析
        if len(confusion_matrix_list) > 0:
            confusion_matrix = ConfusionMatrixMetric()
            confusion_matrix.name = MetricName.image_confusion_matrix.value
            confusion_matrix.display_name = MetricDisplayName.confusion_matrix.value
            confusion_matrix.category = MetricCategory.category_image.value
            confusion_matrix.display_formatter = DisplayFormatter.int_.value
            confusion_matrix.column_annotation_specs = []
            confusion_matrix.row_annotation_specs = []
            confusion_matrix.display_type = MetricDisplayType.table.value
            if MetricName.image_confusion_matrix.value in image_metric_result:
                confusion_matrix.column_annotation_specs = []
                confusion_matrix.row_annotation_specs = []
                confusion_matrix.result = ConfusionMatrixMetricResult()
            else:
                confusion_matrix.column_annotation_specs = [[] for _ in range(len(confusion_matrix_list))]
                confusion_matrix.row_annotation_specs = [[] for _ in range(len(confusion_matrix_list))]
                confusion_matrix.result = [ConfusionMatrixMetricResult() for _ in range(len(confusion_matrix_list))]

            for index, confusion_matrix_result in enumerate(confusion_matrix_list):
                if MetricName.image_confusion_matrix.value in image_metric_result:
                    confusion_matrix.result.rows = []
                else:
                    confusion_matrix.result[index].rows = []
                lower_bound, upper_bound = 0, 0
                for inner_index, item in enumerate(confusion_matrix_result):
                    lower_bound = min(lower_bound, min(item))
                    upper_bound = max(upper_bound, max(item))
                    row = ConfusionMatrixRow(row=item)

                    annotation_specs = AnnotationSpecs()
                    annotation_specs.name = str(inner_index)

                    if MetricName.image_confusion_matrix.value in image_metric_result:
                        if inner_index not in self.confusion_matrix_index2id:
                            label_name = "背景图"
                        else:
                            label_name = self.label_id2name[self.confusion_matrix_index2id[inner_index]]

                        bcelogger.info(f"The image confusion matrix {label_name} is {item}")
                        annotation_specs.display_name = label_name
                        confusion_matrix.column_annotation_specs.append(annotation_specs)
                        confusion_matrix.row_annotation_specs.append(annotation_specs)
                        confusion_matrix.result.rows.append(row)
                        confusion_matrix.result.lower_bound = lower_bound
                        confusion_matrix.result.upper_bound = upper_bound
                    else:
                        parent_id = confusion_matrix_label_ids[index]
                        label_name = self.label_inner_id2name[parent_id][inner_index]

                        bcelogger.info(f"The image confusion matrix {label_name} is {item}")
                        annotation_specs.display_name = label_name

                        confusion_matrix.column_annotation_specs[index].append(annotation_specs)
                        confusion_matrix.row_annotation_specs[index].append(annotation_specs)
                        confusion_matrix.result[index].rows.append(row)
                        confusion_matrix.result[index].lower_bound = lower_bound
                        confusion_matrix.result[index].upper_bound = upper_bound

            metric.metrics.append(confusion_matrix)

    def _format_result_to_bounding_box(self, metric: InferenceMetric, bounding_box_metric_result: Dict):
        """
        Format to bounding box result.
        """
        bounding_box_metric_result = bounding_box_metric_result[MetricName.bounding_box_metric.value]

        # 标签指标结果解析
        bounding_box_label = InferenceLabelMetric()
        bounding_box_label.name = MetricName.bounding_box_label_metric.value
        bounding_box_label.display_name = MetricDisplayName.bounding_box_label_metric.value
        bounding_box_label.category = MetricCategory.category_bbox.value
        bounding_box_label.display_type = MetricDisplayType.table.value

        bounding_box_label.display_formatter = [DisplayFormatter.percentage.value,
                                                DisplayFormatter.percentage.value,
                                                DisplayFormatter.percentage.value,
                                                DisplayFormatter.percentage.value,
                                                DisplayFormatter.percentage.value]

        bounding_box_label.column_annotation_specs = []
        annotation_specs_names = [MetricName.precision.value,
                                  MetricName.recall.value,
                                  MetricName.f1_score.value,
                                  MetricName.average_precision.value,
                                  MetricName.average_recall.value]
        annotation_specs_display_names = [MetricDisplayName.precision.value,
                                          MetricDisplayName.recall.value,
                                          MetricDisplayName.f1_score.value,
                                          MetricDisplayName.average_precision.value,
                                          MetricDisplayName.average_recall.value]
        annotation_specs_description = [MetricDescription.precision.value,
                                        MetricDescription.recall.value,
                                        MetricDescription.f1_score.value,
                                        MetricDescription.average_precision.value,
                                        MetricDescription.average_recall.value]
        for idx in range(len(annotation_specs_names)):
            annotation_specs = AnnotationSpecs()
            annotation_specs.name = annotation_specs_names[idx]
            annotation_specs.display_name = annotation_specs_display_names[idx]
            annotation_specs.description = annotation_specs_description[idx]
            bounding_box_label.column_annotation_specs.append(annotation_specs)

        bounding_box_label.result = []
        for item, p, r, f1 in zip(bounding_box_metric_result[0]["bbox_results_per_label"],
                                  *precision_recall_f1_from_confusion_matrix(np.array(bounding_box_metric_result[1]))):
            bcelogger.info(f'The bounding box label metric {item["labelName"]} result is {item}')
            _result = LabelMetricResult()
            _result.label_name = item["labelName"]
            _result.precision = p
            _result.recall = r
            _result.f1_score = f1
            _result.average_precision = item["averagePrecision"]
            _result.average_recall = item["averageRecall"]
            bounding_box_label.result.append(_result)
        metric.metrics.append(bounding_box_label)

        # p-r曲线指标结果解析
        precision_recall_curve = BoundingBoxPRCurveMetric()
        precision_recall_curve.category = MetricCategory.category_bbox.value
        precision_recall_curve.display_type = MetricDisplayType.chart.value
        precision_recall_curve.horizontal_axis_annotation_specs = MetricDisplayName.precision.value
        precision_recall_curve.vertical_axis_annotation_specs = MetricDisplayName.recall.value
        precision_recall_curve.result = []
        for item in bounding_box_metric_result[0]["pr_curve"]:
            bcelogger.info(f'The bounding box precision recall curve {item[0]} result is {item}')
            _result = BoundingBoxPRCurveMetricResult()
            _result.label_name = item[0]
            _result.iou_threshold = item[4]
            _result.average_precision = item[1]
            _result.confidence_metrics = []
            for idx, p in enumerate(item[2]):
                confidence_metric = BoundingBoxLabelConfidenceMetric()
                confidence_metric.precision = p
                confidence_metric.recall = item[3][idx]
                _result.confidence_metrics.append(confidence_metric)
            precision_recall_curve.result.append(_result)
        metric.metrics.append(precision_recall_curve)

        # 混淆矩阵指标结果解析
        confusion_matrix = ConfusionMatrixMetric()
        confusion_matrix.name = MetricName.bounding_box_confusion_matrix.value
        confusion_matrix.display_name = MetricDisplayName.confusion_matrix.value
        confusion_matrix.category = MetricCategory.category_bbox.value
        confusion_matrix.display_formatter = DisplayFormatter.int_.value
        confusion_matrix.column_annotation_specs = []
        confusion_matrix.row_annotation_specs = []
        confusion_matrix.display_type = MetricDisplayType.table.value
        confusion_matrix.result = ConfusionMatrixMetricResult()
        confusion_matrix.result.rows = []

        lower_bound, upper_bound = 0, 0
        for idx, item in enumerate(bounding_box_metric_result[1]):
            lower_bound = min(lower_bound, min(item))
            upper_bound = max(upper_bound, max(item))
            row = ConfusionMatrixRow(row=item)
            if idx not in self.confusion_matrix_index2id:
                label_name = "背景图"
            else:
                label_name = self.label_id2name[self.confusion_matrix_index2id[idx]]

            bcelogger.info(f"The image confusion matrix {label_name} is {item}")

            annotation_specs = AnnotationSpecs()
            annotation_specs.name = str(idx)
            annotation_specs.display_name = label_name
            confusion_matrix.column_annotation_specs.append(annotation_specs)
            confusion_matrix.row_annotation_specs.append(annotation_specs)

            confusion_matrix.result.rows.append(row)
            confusion_matrix.result.lower_bound = lower_bound
            confusion_matrix.result.upper_bound = upper_bound
        metric.metrics.append(confusion_matrix)

    def compute(self):
        """
        Compute metric.
        """
        if not self.data_format_valid:
            return {}

        results: Dict[str, Dict] = defaultdict(dict)
        for category, metric_dict in self.metric.items():
            if not self.calculate_metric[category]:
                continue
            for index, metric_list in metric_dict.items():
                result_list = []
                for metric in metric_list:
                    result_list.append(metric.compute())
                results[category].update({index: result_list})

        metric_result = self._format_result(metric_result=results)

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

    def __call__(self, predictions: List[Dict], references: List[Dict], output_uri: str):
        self.update(predictions=predictions, references=references)
        metric_result = self.compute()

        self.save(metric_result=metric_result, output_uri=output_uri)
