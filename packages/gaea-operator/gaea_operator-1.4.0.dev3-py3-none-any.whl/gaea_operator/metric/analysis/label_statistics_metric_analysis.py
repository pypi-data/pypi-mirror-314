#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/23
# @Author  : yanxiaodong
# @File    : label_count_metric.py
"""
from typing import List, Dict, Union
import os
import numpy as np
import math

from gaea_operator.utils import write_file
from ..operator import CountStatistic, HistogramStatistic
from ..types.metric import LabelStatisticsMetric, \
    LabelCountStatistic, \
    LabelCountStatisticResult, \
    LabelCutStatistic, \
    LabelCutStatisticResult, \
    StatisticMetric, \
    LABEL_STATISTIC_METRIC, \
    ANNOTATION_AREA_STATISTIC_METRIC, \
    ANNOTATION_CONFIDENCE_STATISTIC_METRIC, \
    ANNOTATION_WIDTH_STATISTIC_METRIC, \
    ANNOTATION_HEIGHT_STATISTIC_METRIC
from collections import defaultdict


class LabelStatisticMetricAnalysis(object):
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
        self.metric = {}
        self.task_kind = self.manual_task_kind
        self.task_labels = defaultdict(lambda: defaultdict(list))

        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        for _, metric in self.metric.items():
            if isinstance(metric, list):
                # 如果 metric 是 list，则循环调用 reset
                for m in metric:
                    m.reset()
            else:
                # 如果不是 list，直接调用 reset
                metric.reset()

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

        if self.category in ("Image/ImageClassification/MultiTask",):
            # 构建 key 为 parentID，value 为 单任务 labels 的字典
            ## 处理每个属性
            self.labels = [{"id": int(label["id"]),
                            "name": label["name"],
                            "parentID": label.get("parentID")} for label in labels]
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
        if self.category in ("Image/ImageClassification/MultiTask",):
            self.format_input = self._format_to_multitask_classification
            self.format_result = self._format_multitask_classification_result
            self.metric = {LABEL_STATISTIC_METRIC: [],
                           ANNOTATION_CONFIDENCE_STATISTIC_METRIC: [],
                           ANNOTATION_AREA_STATISTIC_METRIC: [],
                           ANNOTATION_WIDTH_STATISTIC_METRIC: [],
                           ANNOTATION_HEIGHT_STATISTIC_METRIC: []}
            for task_id, item in self.task_labels.items():
                self.metric[LABEL_STATISTIC_METRIC].append(CountStatistic(num_classes=len(item['labels']),
                                                                          labels=item['labels']))
                self.metric[ANNOTATION_CONFIDENCE_STATISTIC_METRIC].append(
                    HistogramStatistic(num_classes=len(item['labels']), labels=item['labels'], range=(0, 1)))
                self.metric[ANNOTATION_AREA_STATISTIC_METRIC].append(
                    HistogramStatistic(num_classes=len(item['labels']), labels=item['labels']))
                self.metric[ANNOTATION_WIDTH_STATISTIC_METRIC].append(
                    HistogramStatistic(num_classes=len(item['labels']), labels=item['labels']))
                self.metric[ANNOTATION_HEIGHT_STATISTIC_METRIC].append(
                    HistogramStatistic(num_classes=len(item['labels']), labels=item['labels']))

        else:
            self.format_input = self._format_input
            self.format_result = self._format_result
            self.metric = {LABEL_STATISTIC_METRIC: CountStatistic(num_classes=len(self.labels), labels=self.labels),
                           ANNOTATION_CONFIDENCE_STATISTIC_METRIC: HistogramStatistic(num_classes=len(self.labels),
                                                                                      labels=self.labels,
                                                                                      range=(0, 1)),
                           ANNOTATION_AREA_STATISTIC_METRIC: HistogramStatistic(num_classes=len(self.labels),
                                                                                labels=self.labels),
                           ANNOTATION_WIDTH_STATISTIC_METRIC: HistogramStatistic(num_classes=len(self.labels),
                                                                                 labels=self.labels),
                           ANNOTATION_HEIGHT_STATISTIC_METRIC: HistogramStatistic(num_classes=len(self.labels),
                                                                                  labels=self.labels)}

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        self.task_kind = kwargs.get("task_kind", self.manual_task_kind)
        annotations = predictions if predictions is not None else references
        assert annotations is not None, "annotations should not be None"
        annotation_dict = self.format_input(annotations)

        for key, item in self.metric.items():
            if isinstance(item, list):
                for idx, metric in enumerate(item):
                    if key in annotation_dict:
                        if key == LABEL_STATISTIC_METRIC:
                            annos = [arr[idx] for arr in annotation_dict[key]]
                        else:
                            annos = annotation_dict[key][idx]
                        metric.update(annotations=annos)
            else:
                if key in annotation_dict:
                    item.update(annotations=annotation_dict[key])

    def _format_input(self, annotations: List[Dict]):
        """
        Format predictions and references.
        """
        annotation_dict = {LABEL_STATISTIC_METRIC: [],
                           ANNOTATION_CONFIDENCE_STATISTIC_METRIC: {name: [] for name in self.label_name2id},
                           ANNOTATION_AREA_STATISTIC_METRIC: {name: [] for name in self.label_name2id},
                           ANNOTATION_WIDTH_STATISTIC_METRIC: {name: [] for name in self.label_name2id},
                           ANNOTATION_HEIGHT_STATISTIC_METRIC: {name: [] for name in self.label_name2id}}

        for item in annotations:
            if item.get("annotations") is None:
                continue
            for anno in item["annotations"]:
                if self.category == "Image/TextDetection" or self.category == "Image/OCR":
                    anno["labels"] = [{"id": 0, "name": "文字"}]
                for idx in range(len(anno["labels"])):
                    pred_array = np.zeros(len(self.labels))
                    if isinstance(anno["labels"][idx]["id"], str):
                        anno["labels"][idx]["id"] = int(anno["labels"][idx]["id"])
                    if anno["labels"][idx]["id"] is None or math.isnan(anno["labels"][idx]["id"]):
                        continue
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if int(anno["labels"][idx]["id"]) not in self.label_id2index:
                        continue
                    column_index = self.label_id2index[int(anno["labels"][idx]["id"])]
                    label_name = self.label_index2name[column_index]
                    if self.task_kind != self.manual_task_kind:
                        confidence = anno["labels"][idx].get("confidence", 1)
                        annotation_dict[ANNOTATION_CONFIDENCE_STATISTIC_METRIC][label_name].append(confidence)
                    pred_array[column_index] = 1
                    annotation_dict[LABEL_STATISTIC_METRIC].append(pred_array)
                    if self.category in ("Image/ObjectDetection",
                                         "Image/SemanticSegmentation",
                                         "Image/TextDetection",
                                         "Image/InstanceSegmentation"):
                        if "area" in anno:
                            annotation_dict[ANNOTATION_AREA_STATISTIC_METRIC][label_name].append(anno["area"])
                        if "bbox" in anno:
                            annotation_dict[ANNOTATION_WIDTH_STATISTIC_METRIC][label_name].append(anno["bbox"][2])
                            annotation_dict[ANNOTATION_HEIGHT_STATISTIC_METRIC][label_name].append(anno["bbox"][3])

        for key, anno in annotation_dict.items():
            if key == LABEL_STATISTIC_METRIC:
                if len(anno) == 0:
                    annotation_dict[key] = [np.zeros(len(self.labels))]
            # 过滤掉都是零值
            if key in [ANNOTATION_CONFIDENCE_STATISTIC_METRIC,
                       ANNOTATION_AREA_STATISTIC_METRIC,
                       ANNOTATION_WIDTH_STATISTIC_METRIC,
                       ANNOTATION_HEIGHT_STATISTIC_METRIC]:

                new_anno = {}
                for label_name, value in anno.items():
                    if len(value) > 0:
                        new_anno[label_name] = value
                annotation_dict[key] = new_anno

        return annotation_dict

    def _format_to_multitask_classification(self, annotations: List[Dict]):
        """
        Format predictions and references.
        """
        annotation_dict = defaultdict(list)
        for item in self.label_name2id:
            annotation_dict[ANNOTATION_CONFIDENCE_STATISTIC_METRIC].append({name: [] for name in item})
            annotation_dict[ANNOTATION_AREA_STATISTIC_METRIC].append({name: [] for name in item})
            annotation_dict[ANNOTATION_WIDTH_STATISTIC_METRIC].append({name: [] for name in item})
            annotation_dict[ANNOTATION_HEIGHT_STATISTIC_METRIC].append({name: [] for name in item})

        for item in annotations:
            if item.get("annotations") is None:
                continue
            for anno in item["annotations"]:
                for idx in range(len(anno["labels"])):
                    pred_array = [np.zeros(len(i["labels"])) for _, i in self.task_labels.items()]
                    if isinstance(anno["labels"][idx]["id"], str):
                        anno["labels"][idx]["id"] = int(anno["labels"][idx]["id"])
                    if anno["labels"][idx]["id"] is None or math.isnan(anno["labels"][idx]["id"]):
                        continue
                    task_index = list(self.task_labels.keys()).index(int(anno["labels"][idx]["parent_id"]))
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if anno["labels"][idx]["id"] not in \
                            self.label_id2index[task_index]:
                        continue
                    column_index = self.label_id2index[task_index][int(anno["labels"][idx]["id"])]
                    label_name = self.label_index2name[task_index][column_index]
                    if self.task_kind != self.manual_task_kind:
                        confidence = anno["labels"][idx].get("confidence", 1)
                        annotation_dict[ANNOTATION_CONFIDENCE_STATISTIC_METRIC][task_index][label_name] \
                            .append(confidence)
                    pred_array[task_index][column_index] = 1
                    annotation_dict[LABEL_STATISTIC_METRIC].append(pred_array)

        for key, anno in annotation_dict.items():
            if key == LABEL_STATISTIC_METRIC:
                if len(anno) == 0:
                    annotation_dict[key] = [np.zeros(len(i["labels"])) for _, i in self.task_labels.items()]
            # 过滤掉都是零值
            if key in [ANNOTATION_CONFIDENCE_STATISTIC_METRIC,
                       ANNOTATION_AREA_STATISTIC_METRIC,
                       ANNOTATION_WIDTH_STATISTIC_METRIC,
                       ANNOTATION_HEIGHT_STATISTIC_METRIC]:
                new_anno_list = []
                for item in anno:
                    new_anno = {}
                    for label_name, value in item.items():
                        if len(value) > 0:
                            new_anno[label_name] = value
                    new_anno_list.append(new_anno)
                annotation_dict[key] = new_anno_list

        return annotation_dict

    def _format_result(self, metric_result: Dict):
        metric = LabelStatisticsMetric(labels=self.labels, metrics=[])
        label_count = LabelCountStatistic(name=LABEL_STATISTIC_METRIC,
                                          displayName="标签统计",
                                          result=[])
        label_confidence_cut = LabelCutStatistic(name=ANNOTATION_CONFIDENCE_STATISTIC_METRIC,
                                                 displayName="标注框置信度统计",
                                                 result=[])
        label_area_cut = LabelCutStatistic(name=ANNOTATION_AREA_STATISTIC_METRIC,
                                           displayName="标注框面积统计",
                                           result=[])
        label_width_cut = LabelCutStatistic(name=ANNOTATION_WIDTH_STATISTIC_METRIC,
                                            displayName="标注框宽统计",
                                            result=[])
        label_height_cut = LabelCutStatistic(name=ANNOTATION_HEIGHT_STATISTIC_METRIC,
                                             displayName="标注框高统计",
                                             result=[])
        key2statistic = {ANNOTATION_CONFIDENCE_STATISTIC_METRIC: label_confidence_cut,
                         ANNOTATION_AREA_STATISTIC_METRIC: label_area_cut,
                         ANNOTATION_WIDTH_STATISTIC_METRIC: label_width_cut,
                         ANNOTATION_HEIGHT_STATISTIC_METRIC: label_height_cut}
        for key, result in metric_result.items():
            result = result[self.metric[key].global_name()]
            if key == LABEL_STATISTIC_METRIC:
                for idx, label_name in self.label_index2name.items():
                    label_count_statistic_result = LabelCountStatisticResult(labelName=label_name,
                                                                             labelCount=result[idx])

                    label_count.result.append(label_count_statistic_result)
            else:
                for idx, label_name in self.label_index2name.items():
                    label_cut_statistic_result = LabelCutStatisticResult(labelName=label_name,
                                                                         statisticMetrics=[])

                    self._format_cut_statistic(result[label_name], label_cut_statistic_result)
                    key2statistic[key].result.append(label_cut_statistic_result)

        metric.metrics.extend([label_count])
        if self.task_kind != self.manual_task_kind:
            metric.metrics.extend([label_confidence_cut])
        if self.category in ("Image/ObjectDetection",
                             "Image/SemanticSegmentation",
                             "Image/TextDetection",
                             "Image/InstanceSegmentation"):
            metric.metrics.extend([label_area_cut,
                                   label_width_cut,
                                   label_height_cut])
        return metric.dict(by_alias=True, exclude_none=True)

    def _format_multitask_classification_result(self, metric_result: Dict):
        label_names = [
            {'id': task_id, 'name': task_item['label_name']}
            for task_id, task_item in self.task_labels.items()]
        metric = LabelStatisticsMetric(labels=self.labels, metrics=[])
        label_count = LabelCountStatistic(name=LABEL_STATISTIC_METRIC,
                                          displayName="标签统计",
                                          result=[])
        for key, result in metric_result.items():
            result = result[self.metric[key][0].global_name()]
            if key == LABEL_STATISTIC_METRIC:
                for task_idx, name in enumerate(label_names):
                    label_count_statistic_result = LabelCountStatisticResult(labelName=name['name'], labelCount=[])

                    for idx, label_name in self.label_index2name[task_idx].items():
                        label_count_statistic_result.labelCount.append(LabelCountStatisticResult
                                                                       (labelName=label_name,
                                                                        labelCount=result[task_idx][idx]))

                    label_count.result.append(label_count_statistic_result)

        metric.metrics.extend([label_count])
        return metric.dict(by_alias=True, exclude_none=True)

    def _format_cut_statistic(self, anno_res, statistic: LabelCutStatisticResult):
        for value in anno_res:
            cut_statistic = StatisticMetric(bboxCount=value[0], lowerBound=value[1], upperBound=value[2])
            statistic.statisticMetrics.append(cut_statistic)

    def compute(self):
        """
        Compute metric.
        """
        results = {}
        for key, item in self.metric.items():
            # 初始化结果字典
            if key not in results:
                results[key] = {}
            if isinstance(item, list):
                for metric in item:
                    if metric.name not in results[key]:
                        results[key][metric.name] = []
                    results[key][metric.name].append(metric.compute())
            else:
                results[key][item.name] = item.compute()

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

    def __call__(self, predictions: List[Dict], references: List[Dict], output_uri: str):
        self.update(predictions=predictions, references=references)
        metric_result = self.compute()

        self.save(metric_result=metric_result, output_uri=output_uri)
