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
from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import check_input_dim, check_input_type, check_input_num_classes, check_input_length, check_input_value
from gaea_operator.utils import list2ndarray, numpy_round2list, torch_round2list, paddle_round2list


def _tp_fp_fn(pred_positive: Tensor, gt_positive: Tensor, average: str):
    class_correct = pred_positive & gt_positive
    if average == PrecisionRecallF1score.average_options[0]:
        tp_sum = class_correct.sum()
        pred_sum = pred_positive.sum()
        gt_sum = gt_positive.sum()
    else:
        tp_sum = class_correct.sum(0)
        pred_sum = pred_positive.sum(0)
        gt_sum = gt_positive.sum(0)

    return tp_sum, pred_sum, gt_sum


@METRIC.register_module('precision_recall_f1score')
class PrecisionRecallF1score(MetricOperator):
    """
    A collection of metrics for multi-class classification task, It includes precision, recall, f1-score.
    """
    average_options = ['micro', 'macro', 'none']
    metric_name = 'precision_recall_f1score'

    def __init__(self,
                 average: Optional[str] = 'macro',
                 thresholds: Optional[float] = 0.5,
                 **kwargs):
        super(PrecisionRecallF1score, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.average = average
        self.reference_length_is_zero = False
        if self.average in kwargs:
            self.average = kwargs[self.name]['average']

        assert self.average in self.average_options, f'Invalid `average` argument: {self.average}, ' \
                                                     f'please specify from {self.average_options}.'

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
        if not check_input_length(references=references):
            self.reference_length_is_zero = True
            return

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

        if isinstance(predictions, PTensor):
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

        if isinstance(predictions, TTensor):
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

        tp_sum, pred_sum, gt_sum = _tp_fp_fn(pred_positive=pred_positive,
                                             gt_positive=gt_positive,
                                             average=self.average)

        self.tp_sum += tp_sum
        self.pred_sum += pred_sum
        self.gt_sum += gt_sum

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        if self.reference_length_is_zero:
            if self.average != self.average_options[-1]:
                return -1, -1, -1
            else:
                return [-1] * self.num_classes, [-1] * self.num_classes, [-1] * self.num_classes

        if isinstance(self.pred_sum, TTensor):
            # use torch with torch.Tensor
            precision = self.tp_sum / torch.clamp(self.pred_sum, min=1)
            recall = self.tp_sum / torch.clamp(self.gt_sum, min=1)
            f1_score = 2 * precision * recall / torch.clamp(
                precision + recall, min=torch.finfo(torch.float32).eps)
        elif isinstance(self.pred_sum, PTensor):
            # use paddle with paddle.Tensor
            precision = self.tp_sum / paddle.clip(self.pred_sum, min=1)
            recall = self.tp_sum / paddle.clip(self.gt_sum, min=1)
            f1_score = 2 * precision * recall / paddle.clip(precision + recall, min=1e-8)
        else:
            # use numpy with numpy.ndarray
            precision = self.tp_sum / np.clip(self.pred_sum, 1, np.inf)
            recall = self.tp_sum / np.clip(self.gt_sum, 1, np.inf)
            f1_score = 2 * precision * recall / np.clip(precision + recall,
                                                        np.finfo(np.float32).eps,
                                                        np.inf)
        if self.num_classes == 2:
            if self.average != self.average_options[-1]:
                precision = round(float(precision[-1]), self.decimals)
                recall = round(float(recall[-1]), self.decimals)
                f1_score = round(float(f1_score[-1]), self.decimals)
            else:
                if isinstance(precision, PTensor):
                    precision = paddle_round2list(precision, decimals=self.decimals)
                    recall = paddle_round2list(recall, decimals=self.decimals)
                    f1_score = paddle_round2list(f1_score, decimals=self.decimals)
                if isinstance(precision, TTensor):
                    precision = torch_round2list(precision, decimals=self.decimals)
                    recall = torch_round2list(recall, decimals=self.decimals)
                    f1_score = torch_round2list(f1_score, decimals=self.decimals)
                if isinstance(precision, np.ndarray):
                    precision = numpy_round2list(precision, decimals=self.decimals)
                    recall = numpy_round2list(recall, decimals=self.decimals)
                    f1_score = numpy_round2list(f1_score, decimals=self.decimals)
        else:
            if self.average == self.average_options[1]:
                precision = round(float(precision.mean()), self.decimals)
                recall = round(float(recall.mean()), self.decimals)
                f1_score = round(float(f1_score.mean()), self.decimals)
            elif self.average == self.average_options[0]:
                precision = round(float(precision), self.decimals)
                recall = round(float(recall), self.decimals)
                f1_score = round(float(f1_score), self.decimals)
            else:
                if isinstance(precision, PTensor):
                    precision = paddle_round2list(precision, decimals=self.decimals)
                    recall = paddle_round2list(recall, decimals=self.decimals)
                    f1_score = paddle_round2list(f1_score, decimals=self.decimals)
                if isinstance(precision, TTensor):
                    precision = torch_round2list(precision, decimals=self.decimals)
                    recall = torch_round2list(recall, decimals=self.decimals)
                    f1_score = torch_round2list(f1_score, decimals=self.decimals)
                if isinstance(precision, np.ndarray):
                    precision = numpy_round2list(precision, decimals=self.decimals)
                    recall = numpy_round2list(recall, decimals=self.decimals)
                    f1_score = numpy_round2list(f1_score, decimals=self.decimals)

        return precision, recall, f1_score


@METRIC.register_module('precision')
class Precision(PrecisionRecallF1score):
    """
    Precision is the fraction of correctly labeled positive examples out of all of the examples
    that were labeled as positive.
    """
    metric_name = 'precision'

    def compute(self) -> Any:
        """
        Computes and returns the metric.
        """
        precision, _, _ = super(Precision, self).compute()
        return precision


@METRIC.register_module('recall')
class Recall(PrecisionRecallF1score):
    """
    Recall is the fraction of the positive examples that were correctly labeled by the model as positive.
    """
    metric_name = 'recall'

    def compute(self) -> Any:
        """
        Computes and returns the metric.
        """
        _, recall, _ = super(Recall, self).compute()
        return recall


@METRIC.register_module('f1score')
class F1score(PrecisionRecallF1score):
    """
    The F1 score is the harmonic mean of the precision and recall..
    """
    metric_name = 'f1score'

    def compute(self) -> Any:
        """
        Computes and returns the metric.
        """
        _, _, f1_score = super(F1score, self).compute()
        return f1_score
