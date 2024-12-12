#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/24
# @Author  : yanxiaodong
# @File    : inference.py
"""
import copy
from typing import List, Dict
import os
from collections import defaultdict
import bcelogger
import numpy as np
import math

from gaea_operator.utils import write_file
from gaea_operator.metric.operator import PrecisionRecallF1score, Accuracy
from gaea_operator.metric.types.metric import InferenceMetric, \
    InferenceLabelMetric, \
    INFERENCE_LABEL_METRIC_NAME, \
    InferenceLabelMetricResult


class InferenceMetricAnalysis(object):
    """
    Inference metric analysis.
    """

    def __init__(self,
                 labels: List = None,
                 images: List[Dict] = None,
                 conf_threshold: float = 0):
        self.labels = labels
        self.images = images
        self.conf_threshold = float(conf_threshold)

        self.image_dict = {}
        self.img_id_str2int = {}
        self.label_id2index = {}
        self.label_name2id = {}
        self.metric = {}
        self.set_images(images)
        self.set_labels(labels)

    def reset(self):
        """
        Reset metric.
        """
        for _, metric_list in self.metric.items():
            for metric in metric_list:
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
        self.labels = [{"id": int(label["id"]), "name": label["name"]} for label in labels]
        self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
        self.label_name2id = {label["name"]: label["id"] for label in self.labels}
        self.set_metric()

    def set_metric(self):
        """
        Set metric.
        """
        _metric = [Accuracy(num_classes=2), PrecisionRecallF1score(num_classes=2)]
        self.metric = {label["name"]: copy.deepcopy(_metric) for label in self.labels}

    def update(self, predictions: List[Dict], references: List[Dict], **kwargs):
        """
        Update metric.
        """
        predictions, references = self._format_input(predictions, references)

        for name, metric_list in self.metric.items():
            for metric in metric_list:
                index = self.label_id2index[self.label_name2id[name]]
                metric.update(predictions=predictions[:, index], references=references[:, index])

    def _format_input(self, predictions: List[Dict], references: List[Dict]):
        """
        Format to object detection metric.
        """
        reference_dict = defaultdict(list)
        for item in references:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            array_item = np.zeros(len(self.labels), dtype=np.int8)
            if item.get("annotations") is None:
                reference_dict[im_id_int].append(array_item)
                continue
            for anno in item["annotations"]:
                if anno.get("ocr") is not None and anno["ocr"].get("word", "") != "":
                    array_item = str(anno.get("ocr", {}).get("word", ""))
                    break
                if len(anno.get("quadrangle", [])) > 0:
                    array_item[0] = 1
                    break
                if "bbox" in anno and len(anno["bbox"]) == 0:
                    continue
                for idx in range(len(anno["labels"])):
                    if isinstance(anno["labels"][idx]["id"], str):
                        anno["labels"][idx]["id"] = int(anno["labels"][idx]["id"])
                    if anno["labels"][idx]["id"] is None or math.isnan(anno["labels"][idx]["id"]):
                        continue
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if anno["labels"][idx]["id"] not in self.label_id2index:
                        continue
                    index = self.label_id2index[anno["labels"][idx]["id"]]
                    array_item[index] = 1
            reference_dict[im_id_int].append(array_item)

        prediction_dict = defaultdict(list)
        for item in predictions:
            im_id = item["image_id"]
            im_id_int = self.img_id_str2int[im_id]
            array_item = np.zeros(len(self.labels), dtype=np.int8)
            # 如果预测结果不在 gt里面，是一张未标注的图片，不参与指标计算
            if item.get("annotations") is None or im_id_int not in reference_dict:
                prediction_dict[im_id_int].append(array_item)
                continue
            for anno in item["annotations"]:
                if anno.get("ocr") is not None and anno["ocr"].get("word", "") != "":
                    array_item = anno["ocr"].get("word", "")
                    break
                if len(anno.get("quadrangle", [])) > 0:
                    array_item[0] = 1
                    break
                for idx in range(len(anno["labels"])):
                    try:
                        if isinstance(anno["labels"][idx]["id"], str):
                            anno["labels"][idx]["id"] = int(anno["labels"][idx]["id"])
                    except:
                        bcelogger.info(f'label id is {anno["labels"][idx]["id"]}')
                        if anno["labels"][idx]["id"] not in self.label_name2id:
                            continue
                        anno["labels"][idx]["id"] = self.label_name2id[anno["labels"][idx]["id"]]
                    if anno["labels"][idx]["id"] is None or math.isnan(anno["labels"][idx]["id"]):
                        continue
                    # 如果预测结果标签id不在label,则跳过（修改了标签但是预测结果没有同步修改）
                    if anno["labels"][idx]["id"] not in self.label_id2index:
                        continue
                    if anno["labels"][idx]["confidence"] > self.conf_threshold:
                        index = self.label_id2index[anno["labels"][idx]["id"]]
                        array_item[index] = 1
            prediction_dict[im_id_int].append(array_item)

        reference_list = []
        prediction_list = []
        for img_id, anno in reference_dict.items():
            # 只有同时拥有gt和预测结果才参与指标计算
            if img_id in prediction_dict:
                prediction_anno = prediction_dict[img_id]
                array_item_ref = np.zeros(len(self.labels), dtype=np.int8)
                array_item_pred = np.zeros(len(self.labels), dtype=np.int8)

                if len(anno) > 0 and not isinstance(anno[0], np.ndarray):
                    is_negative_sample = anno[0] == ""
                    # 都为空字符串
                    if not is_negative_sample and anno[0] != prediction_anno[0]:
                        array_item_ref[0] = 1
                        array_item_pred[0] = 0
                    # 预测和真实标注相同且不为空字符串
                    elif anno[0] == prediction_anno[0] and not is_negative_sample:
                        array_item_ref[0] = 1
                        array_item_pred[0] = 1
                    # 真实标注为空，预测结果不为空
                    elif is_negative_sample and anno[0] != prediction_anno[0]:
                        array_item_ref[0] = 0
                        array_item_pred[0] = 1
                    # 真实标注不为空，预测结果为空
                    elif is_negative_sample and anno[0] == prediction_anno[0]:
                        array_item_ref[0] = 0
                        array_item_pred[0] = 0

                    reference_list.append(array_item_ref)
                    prediction_list.append(array_item_pred)
                else:
                    reference_list.extend(anno)
                    prediction_list.extend(prediction_anno)

        return np.array(prediction_list), np.array(reference_list)

    def _format_result(self, metric_result: Dict):
        metric = InferenceMetric(labels=self.labels, metrics=[])
        label_metric = InferenceLabelMetric(name=INFERENCE_LABEL_METRIC_NAME,
                                            displayName="类别指标",
                                            result=[])
        for name, result in metric_result.items():
            accuracy = result[self.metric[name][0].global_name()]
            precision = result[self.metric[name][1].global_name()][0]
            recall = result[self.metric[name][1].global_name()][1]

            inference_label_metric_result = InferenceLabelMetricResult(labelName=name,
                                                                       precision=precision,
                                                                       recall=recall,
                                                                       accuracy=accuracy)
            label_metric.result.append(inference_label_metric_result)

        metric.metrics.extend([label_metric])
        return metric.dict()

    def compute(self):
        """
        Compute metric.
        """
        results = {}
        for name, metric_list in self.metric.items():
            results[name] = {}
            for metric in metric_list:
                results[name][metric.name] = metric.compute()

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
