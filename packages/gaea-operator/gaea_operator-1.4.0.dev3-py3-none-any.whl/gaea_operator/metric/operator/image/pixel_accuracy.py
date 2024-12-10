#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/10/8
# @Author  : yanxiaodong
# @File    : mean_iou.py
"""
from typing import List, Union, Any
import numpy as np

from gaea_operator.utils import METRIC
from gaea_operator.utils import paddle, torch, Tensor, PTensor, TTensor
from gaea_operator.utils import torch_round2list, paddle_round2list, numpy_round2list
from ..metric import MetricOperator
from ..check import check_input_type
from .mean_iou import _calculate_area_paddle, _calculate_area_torch, _calcuate_area_numpy


@METRIC.register_module('pixel_accuracy')
class PixelAccuracy(MetricOperator):
    """
    Pixel accuracy refers to the proportion of correctly labeled pixels out of all possible pixels.
    """
    metric_name = 'pixel_accuracy'

    def __init__(self, ignore_index: int = 255, reduce_labels: bool = False, **kwargs):
        super(PixelAccuracy, self).__init__(num_classes=kwargs.get('num_classes', 2))

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
        if isinstance(self.total_intersect_area, np.ndarray):
            mean_acc = numpy_round2list(np.sum(self.total_intersect_area) / np.sum(self.total_pred_area),
                                        decimals=self.decimals)
        elif isinstance(self.total_intersect_area, PTensor):
            mean_acc = numpy_round2list(paddle.sum(self.total_intersect_area) / paddle.sum(self.total_pred_area),
                                        decimals=self.decimals)
        elif isinstance(self.total_intersect_area, TTensor):
            mean_acc = numpy_round2list(torch.sum(self.total_intersect_area) / torch.sum(self.total_pred_area),
                                        decimals=self.decimals)
        else:
            raise TypeError(f"Unsupported type: {type(self.total_intersect_area)}")

        return mean_acc