#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/10/8
# @Author  : yanxiaodong
# @File    : mean_iou.py
"""
from typing import List, Union, Any
import numpy as np

from gaea_operator.utils import paddle, torch, Tensor, PTensor, TTensor
from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import check_input_type
from gaea_operator.utils import torch_round2list, paddle_round2list, numpy_round2list


def _calculate_area_paddle(pred: PTensor, label: PTensor, num_classes: int, ignore_index: int = 255):
    pred_area = []
    label_area = []
    intersect_area = []
    mask = label != ignore_index

    for i in range(num_classes):
        pred_i = paddle.logical_and(pred == i, mask)
        label_i = label == i
        intersect_i = paddle.logical_and(pred_i, label_i)
        pred_area.append(paddle.sum(pred_i.astype(paddle.int32)))
        label_area.append(paddle.sum(label_i.astype(paddle.int32)))
        intersect_area.append(paddle.sum(intersect_i.astype(paddle.int32)))

    pred_area = paddle.concat(pred_area)
    label_area = paddle.concat(label_area)
    intersect_area = paddle.concat(intersect_area)

    return pred_area, label_area, intersect_area


def _calculate_area_torch(pred: TTensor, label: TTensor, num_classes: int, ignore_index: int = 255):
    pred_area = []
    label_area = []
    intersect_area = []
    mask = label != ignore_index

    for i in range(num_classes):
        pred_i = torch.logical_and(pred == i, mask)
        label_i = label == i
        intersect_i = torch.logical_and(pred_i, label_i)
        pred_area.append(torch.sum(pred_i.type(torch.int32)))
        label_area.append(torch.sum(label_i.type(torch.int32)))
        intersect_area.append(torch.sum(intersect_i).type(torch.int32))

    pred_area = torch.concat(pred_area)
    label_area = torch.concat(label_area)
    intersect_area = torch.concat(intersect_area)

    return pred_area, label_area, intersect_area


def _calcuate_area_numpy(pred: np.ndarray, label: np.ndarray, num_classes: int, ignore_index: int = 255):
    mask = np.not_equal(label, ignore_index)
    pred = pred[mask]
    label = np.array(label)[mask]

    intersect = pred[pred == label]

    pred_area = np.histogram(pred, bins=num_classes, range=(0, num_classes - 1))[0]
    label_area = np.histogram(label, bins=num_classes, range=(0, num_classes - 1))[0]
    intersect_area = np.histogram(intersect, bins=num_classes, range=(0, num_classes - 1))[0]

    return pred_area, label_area, intersect_area


@METRIC.register_module('mean_iou')
class MeanIoU(MetricOperator):
    """
    MeanIoU is the area of overlap between the predicted segmentation and the ground truth divided by the area of union
    between the predicted segmentation and the ground truth.
    """
    metric_name = 'mean_iou'

    def __init__(self, ignore_index: int = 255, reduce_labels: bool = False, **kwargs):
        super(MeanIoU, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.ignore_index = ignore_index
        self.reduce_labels = reduce_labels

        self.add_state("total_pred_area", default=0)
        self.add_state("total_label_area", default=0)
        self.add_state("total_intersect_area", default=0)

    def update(self, predictions: Union[List[Tensor], Tensor], references: Union[List[Tensor], Tensor]) -> None:
        """
        Computes and returns the middle states, such as area.
        """
        check_input_type(predictions=predictions, references=references)

        # if reduce_labels, change the backgrond label to 255
        if self.reduce_labels:
            references[references == 0] = 255
            references = references - 1
            references[references == 254] = 255
        if not isinstance(predictions, list):
            predictions = [predictions]
        if not isinstance(references, list):
            references = [references]

        for pred, ref in zip(predictions, references):
            if isinstance(pred, PTensor):
                pred_area, label_area, intersect_area = _calculate_area_paddle(pred,
                                                                               ref,
                                                                               self.num_classes,
                                                                               self.ignore_index)
            elif isinstance(pred, TTensor):
                pred_area, label_area, intersect_area = _calculate_area_torch(pred,
                                                                              ref,
                                                                              self.num_classes,
                                                                              self.ignore_index)
            else:
                pred_area, label_area, intersect_area = _calcuate_area_numpy(pred,
                                                                             ref,
                                                                             self.num_classes,
                                                                             self.ignore_index)

            self.total_pred_area += pred_area
            self.total_label_area += label_area
            self.total_intersect_area += intersect_area

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        iou = self.total_intersect_area / (
                    self.total_pred_area + self.total_label_area - self.total_intersect_area + 1e-8)
        if isinstance(self.total_pred_area, np.ndarray):
            mean_iou = round(iou.mean(), 4)
        else:
            mean_iou = round(iou.mean().item(), 4)

        if isinstance(self.total_intersect_area, np.ndarray):
            iou = numpy_round2list(iou, decimals=self.decimals)
        if isinstance(self.total_intersect_area, PTensor):
            iou = paddle_round2list(iou, decimals=self.decimals)
        if isinstance(self.total_intersect_area, TTensor):
            iou = torch_round2list(iou, decimals=self.decimals)

        return mean_iou, iou