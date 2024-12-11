#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/23
# @Author  : yanxiaodong
# @File    : label_count_metric.py
"""
from typing import List, Dict, Any, Union
import os
import numpy as np
import math

from ..operator import RatioStatistic
from ..types.metric import \
    AnnotationRatioMetricResult, \
    ImageAnnotationRatioMetric, \
    LabelAnnotationRatio, \
    LabelMetricResult
from gaea_operator.utils import write_file
from collections import defaultdict


class ImageMetricAnalysis(object):
    """
    Label statistic metric analysis.
    """
    manual_task_kind = "Manual"

    def __init__(self, category: str, labels: List = None, images: List[Dict] = None, ):
        self.labels = labels
        self.images = images
        self.category = category

        self.image_dict = {}
        self.img_id_str2int = {}
        self.labels = []
        self.label_id2index: Union[dict, list] = []
        self.label_index2id: Union[dict, list] = []
        self.label_id2name: Union[dict, list] = []
        self.label_name2id: Union[dict, list] = []
        self.label_index2name: Union[dict, list] = []
        self.metric = None
        self.task_kind = self.manual_task_kind
        self.task_labels = defaultdict(lambda: defaultdict(list))

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        if isinstance(self.metric, list):
            for metric in self.metric:
                metric.reset()
        else:
            # 如果不是 list，直接调用 reset
            self.metric.reset()

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        if images is None:
            return
        self.images = images
        self.image_dict = {item["image_id"]: item for item in images}
        self.img_id_str2int = {key: idx + 1 for idx, key in enumerate(self.image_dict)}

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        if labels is None:
            return
        if self.category in ("Image/ImageClassification/MultiTask", ):
            # 构建 key 为 parentID，value 为 单任务 labels 的字典
            self.labels = [{"id": int(label["id"]),
                            "name": label["name"],
                            "parentID": label.get("parentID")} for label in labels]
            ## 处理每个属性的标签
            for label in labels:
                if label.get('parentID') == '' or label.get('parentID') is None:
                    task_id = int(label['id'])
                    label_name = label['name']
                    # 自动为 task_id 初始化 label_name 和嵌套的空列表
                    self.task_labels[task_id]['label_name'] = label_name
                else:
                    parent_id = int(label['parentID'])
                    # 自动为 parent_id 初始化 labels 列表
                    self.task_labels[parent_id]['labels'].append({"id": int(label["id"]),
                                                                  "name": label["name"],
                                                                  "parentID": label.get("parentID")})
            for task_id, item in self.task_labels.items():
                self.label_id2index.append({label["id"]: idx for idx, label in enumerate(item['labels'])})
                self.label_index2id.append({idx: label["id"] for idx, label in enumerate(item['labels'])})
                self.label_id2name.append({label["id"]: label["name"] for label in item['labels']})
                self.label_name2id.append({label["name"]: label["id"] for idx, label in enumerate(item['labels'])})
                self.label_index2name.append({idx: label["name"] for idx, label in enumerate(item['labels'])})
        else:
            self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
            self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
            self.label_index2id = {idx: label["id"] for idx, label in enumerate(self.labels)}
            self.label_id2name = {label["id"]: label["name"] for label in self.labels}
            self.label_name2id = {label["name"]: label["id"] for idx, label in enumerate(self.labels)}
            self.label_index2name = {idx: label["name"] for idx, label in enumerate(self.labels)}
        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        if self.category in ("Image/ImageClassification/MultiTask", ):
            self.format_input = self._format_to_multitask_classification
            self.format_result = self._format_multitask_classification_result
            self.metric = []
            for task_id, item in self.task_labels.items():
                self.metric.append(RatioStatistic(num_classes=len(item['labels']), labels=item['labels']))

        else:
            self.format_input = self._format_input
            self.format_result = self._format_result
            self.metric = RatioStatistic(num_classes=len(self.labels), labels=self.labels)

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        self.task_kind = kwargs.get("task_kind", self.manual_task_kind)
        annotations = predictions if predictions is not None else references
        assert annotations is not None, "annotations should be not None"
        assert self.images is not None, "images should be not None"

        annotated_array, image_array = self.format_input(annotations)
        if isinstance(self.metric, list):
            for idx, metric in enumerate(self.metric):
                metric.update(annotated_images=annotated_array[idx], images=image_array[idx])
        else:
            self.metric.update(annotated_images=annotated_array, images=image_array)

    def _format_input(self, annotations: List[Dict]):
        """
        Format predictions and references.
        """
        num_images = len(self.images)  # 使用 self.images 计算总图像数量
        annotated_array = np.zeros((num_images, len(self.labels)))  # 每个图像和标签的标注数量
        image_id_2_index = {item["image_id"]: idx for idx, item in enumerate(self.images)}
        image_array = np.ones((num_images, len(self.labels)))

        for item in annotations:
            if item["image_id"] not in image_id_2_index:
                continue
            if item.get("annotations") is None:
                continue
            for anno in item["annotations"]:
                if self.category == "Image/TextDetection" or self.category == "Image/OCR":
                    anno["labels"] = [{"id": 0, "name": "文字"}]
                for label in anno.get("labels", []):
                    label_id = label.get("id")
                    if label_id is None:
                        continue
                    if isinstance(label_id, str):
                        label_id = int(label_id)
                    if label_id is None or math.isnan(label_id):
                        continue
                    if int(label_id) not in self.label_id2index:
                        continue
                    column_index = self.label_id2index[int(label_id)]
                    annotated_array[image_id_2_index[item["image_id"]], column_index] = 1  # 增加标注数量

        return annotated_array, image_array

    def _format_to_multitask_classification(self, annotations: List[Dict]):
        """
        Format predictions and references.
        """
        num_images = len(self.images)  # 使用 self.images 计算总图像数量
        annotated_arrays = []
        image_arrays = []
        for task_id, item in self.task_labels.items():
            annotated_arrays.append(np.zeros((num_images, len(item["labels"]))))
            image_arrays.append(np.ones((num_images, len(item["labels"]))))
        image_id_2_index = {item["image_id"]: idx for idx, item in enumerate(self.images)}

        for item in annotations:
            if item["image_id"] not in image_id_2_index:
                continue
            if item.get("annotations") is not None:
                for anno in item["annotations"]:
                    for label in anno.get("labels", []):
                        label_id = label.get("id")
                        if label_id is None:
                            continue
                        if isinstance(label_id, str):
                            label_id = int(label_id)
                        if label_id is None or math.isnan(label_id):
                            continue
                        if not any(int(label_id) in sublist for sublist in self.label_id2index):
                            continue
                        task_index = list(self.task_labels.keys()).index(int(label["parent_id"]))
                        column_index = self.label_id2index[task_index][int(label_id)]
                        annotated_arrays[task_index][image_id_2_index[item["image_id"]], column_index] = 1  # 增加标注数量

        return annotated_arrays, image_arrays

    def _format_multitask_classification_result(self, metric_result: Any):
        """
        Format metric results into the desired structure.
        """
        results = []
        label_annotation_ratio = LabelAnnotationRatio(
            name="AnnotationRatio",
            displayName="标注比例统计",
            result=[]
        )
        # metric_result 是一个包含 annotated_array, image_array 和 ratio 的元组
        for task_idx, result in enumerate(metric_result):
            annotation_result = AnnotationRatioMetricResult(
                labelName=self.task_labels[list(self.task_labels.keys())[task_idx]]['label_name'],
                imageCount=[],
                annotatedImageCount=[],
                ratio=[]
            )
            annotated_image, image, ratio = result
            for idx, label_name in self.label_index2name[task_idx].items():
                # 创建 AnnotationRatioMetricResult 对象
                annotation_result.imageCount.append(LabelMetricResult(labelName=label_name, result=image[idx]))
                annotation_result.annotatedImageCount.append(LabelMetricResult(labelName=label_name,
                                                                               result=annotated_image[idx]))
                annotation_result.ratio.append(LabelMetricResult(labelName=label_name, result=ratio[idx]))
        # 创建 LabelAnnotationRatio 对象
            label_annotation_ratio.result.append(annotation_result)

        # 将结果添加到列表中
        results.append(label_annotation_ratio)
        # 创建 ImageAnnotationRatioMetric 对象
        image_annotation_metric = ImageAnnotationRatioMetric(
            labels=self.labels,
            metrics=results
        )

        # 返回度量的字典表示形式
        return image_annotation_metric.dict()

    def _format_result(self, metric_result: Any):
        """
        Format metric results into the desired structure.
        """
        results = []

        # metric_result 是一个包含 annotated_array, image_array 和 ratio 的元组
        annotated_image, image, ratio = metric_result
        annotation_result_list = list()
        for idx, label_name in self.label_index2name.items():
            # 创建 AnnotationRatioMetricResult 对象
            annotation_result = AnnotationRatioMetricResult(
                labelName=label_name,
                imageCount=image[idx],
                annotatedImageCount=annotated_image[idx],
                ratio=ratio[idx]
            )
            annotation_result_list.append(annotation_result)
        # 创建 LabelAnnotationRatio 对象
        label_annotation_ratio = LabelAnnotationRatio(
            name="AnnotationRatio",
            displayName="标注比例统计",
            result=annotation_result_list
        )

        # 将结果添加到列表中
        results.append(label_annotation_ratio)

        # 创建 ImageAnnotationRatioMetric 对象
        image_annotation_metric = ImageAnnotationRatioMetric(
            labels=self.labels,
            metrics=results
        )

        # 返回度量的字典表示形式
        return image_annotation_metric.dict(by_alias=True, exclude_none=True)

    def compute(self):
        """
        Compute metric.
        """
        if isinstance(self.metric, list):
            metric_result = []
            for metric in self.metric:
                metric_result.append(metric.compute())
            metric_result = self.format_result(metric_result=metric_result)
        else:
            metric_result = self.format_result(metric_result=self.metric.compute())

        return metric_result

    def save(self, metric_result: Dict, output_uri: str):
        """
        Save metric.
        """
        if os.path.splitext(output_uri)[1] == "":
            output_dir = output_uri
            file_name = "annotated_ratio.json"
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
