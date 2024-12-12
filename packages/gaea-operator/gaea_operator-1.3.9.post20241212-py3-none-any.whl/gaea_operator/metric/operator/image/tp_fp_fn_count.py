#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : precision_recall_f1score.py
@Author        : yanxiaodong
@Date          : 2023/5/24
@Description   :
"""
from typing import List, Union, Optional, Any
import numpy as np

from gaea_operator.utils import paddle, torch, PTensor, TTensor, Tensor
from gaea_operator.utils import METRIC
from gaea_operator.utils import list2ndarray
from .precision_recall_f1score import _tp_fp_fn, PrecisionRecallF1score
from ..metric import MetricOperator
from ..check import check_input_dim, check_input_type, check_input_num_classes, check_input_value


@METRIC.register_module('tp_fp_fn_count')
class TPFPFNCount(MetricOperator):
    """
    A collection of metrics for multi-class classification task, It includes tp, fp, fn.
    """
    metric_name = 'tp_fp_fn_count'

    def __init__(self,
                 thresholds: Optional[float] = 0.5,
                 **kwargs):
        super(TPFPFNCount, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.thresholds = thresholds
        if self.name in kwargs:
            self.thresholds = float(kwargs[self.name]['thresholds'])

        self.add_state("tp_sum", default=0)
        self.add_state("pred_sum", default=0)
        self.add_state("gt_sum", default=0)

    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Computes and returns the middle states, such as TP, FP, FN.
        """
        check_input_type(predictions=predictions, references=references)

        predictions = list2ndarray(predictions)
        references = list2ndarray(references)

        predictions, references = check_input_value(predictions=predictions, references=references)

        check_input_dim(predictions=predictions, num_classes=self.num_classes)

        if isinstance(predictions, np.ndarray):
            if self.num_classes == 2:
                if not all((predictions == 1) | (predictions == 0)):
                    predictions = (predictions >= self.thresholds).astype(np.int32)

                gt_positive = np.eye(self.num_classes, dtype=np.int64)[references]
                pred_positive = np.eye(self.num_classes, dtype=np.int64)[predictions]
            else:
                if predictions.ndim == 1:
                    gt_positive = np.eye(self.num_classes, dtype=np.int64)[references]
                    pred_positive = np.eye(self.num_classes, dtype=np.int64)[predictions]
                else:
                    check_input_num_classes(predictions=predictions, num_classes=self.num_classes)

                    pred_label = predictions.argmax(axis=1)

                    gt_positive = np.eye(self.num_classes, dtype=np.int64)[references]
                    pred_positive = np.eye(self.num_classes, dtype=np.int64)[pred_label]

        elif isinstance(predictions, PTensor):
            if self.num_classes == 2:
                if not all((predictions == 1) | (predictions == 0)):
                    predictions = (predictions > self.thresholds).cast(paddle.int32)

                gt_positive = paddle.nn.functional.one_hot(references.flatten().cast(paddle.int64),
                                                           self.num_classes).cast(paddle.int64)
                pred_positive = paddle.nn.functional.one_hot(predictions.cast(paddle.int64),
                                                             self.num_classes).cast(paddle.int64)
            else:
                if predictions.ndim == 1:
                    gt_positive = paddle.nn.functional.one_hot(references.flatten().cast(paddle.int64),
                                                               self.num_classes).cast(paddle.int64)
                    pred_positive = paddle.nn.functional.one_hot(predictions.cast(paddle.int64),
                                                                 self.num_classes).cast(paddle.int64)
                else:
                    check_input_num_classes(predictions=predictions, num_classes=self.num_classes)

                    _, pred_label = paddle.topk(predictions, k=1)
                    pred_label = pred_label.flatten()

                    gt_positive = paddle.nn.functional.one_hot(references.flatten().cast(paddle.int64),
                                                               self.num_classes).cast(paddle.int64)
                    pred_positive = paddle.nn.functional.one_hot(pred_label.cast(paddle.int64),
                                                                 self.num_classes).cast(paddle.int64)

        elif isinstance(predictions, TTensor):
            if self.num_classes == 2:
                if not all((predictions == 1) | (predictions == 0)):
                    predictions = (predictions > self.thresholds).int()

                gt_positive = torch.nn.functional.one_hot(references.flatten().to(torch.int64), self.num_classes)
                pred_positive = torch.nn.functional.one_hot(predictions.to(torch.int64), self.num_classes)
            else:
                if predictions.ndim == 1:
                    gt_positive = torch.nn.functional.one_hot(references.flatten().to(torch.int64), self.num_classes)
                    pred_positive = torch.nn.functional.one_hot(predictions.to(torch.int64), self.num_classes)
                else:
                    check_input_num_classes(predictions=predictions, num_classes=self.num_classes)

                    _, pred_label = torch.topk(predictions, k=1)
                    pred_label = pred_label.flatten()

                    gt_positive = torch.nn.functional.one_hot(references.flatten().to(torch.int64), self.num_classes)
                    pred_positive = torch.nn.functional.one_hot(pred_label.to(torch.int64), self.num_classes)

        else:
            raise TypeError(f"The input data type {type(predictions)} is not supported.")

        tp_sum, pred_sum, gt_sum = _tp_fp_fn(pred_positive=pred_positive,
                                             gt_positive=gt_positive,
                                             average=PrecisionRecallF1score.average_options[1])

        self.tp_sum += tp_sum
        self.pred_sum += pred_sum
        self.gt_sum += gt_sum

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        if self.num_classes == 2:
            return int(self.tp_sum[-1]), int(self.pred_sum[-1]), int(self.gt_sum[-1])
        else:
            return self.tp_sum.astype(int), self.pred_sum.astype(int), self.gt_sum.astype(int)