#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : accuracy.py
@Author        : yanxiaodong
@Date          : 2023/5/24
@Description   :
"""
from typing import List, Union, Optional, Sequence, Tuple, Any
import numpy as np

from gaea_operator.utils import paddle, torch, Tensor, PTensor, TTensor
from gaea_operator.utils import METRIC
from ..metric import MetricOperator
from ..check import check_input_dim, check_input_type, check_input_length, check_input_value
from gaea_operator.utils import list2ndarray, list_round


def _numpy_topk(inputs: np.ndarray, k: int, axis: Optional[int] = None) -> Tuple:
    """
    A implementation of numpy top-k.
    This implementation returns the values and indices of the k largest
    elements along a given axis.
    Args:
        inputs: The input numpy array.
        k: The k in `top-k`.
        axis: The axis to sort along.
    """
    indices = np.argsort(inputs * -1.0, axis=axis)
    indices = np.take(indices, np.arange(k), axis=axis)
    values = np.take_along_axis(inputs, indices, axis=axis)
    return values, indices


def _status_stack(values: List[Tensor]) -> Tensor:
    if isinstance(values[0], np.ndarray):
        return np.concatenate(values, axis=0)
    elif isinstance(values[0], PTensor):
        return paddle.concat(values, axis=0)
    else:
        return torch.concat(values, axis=0)


@METRIC.register_module('accuracy')
class Accuracy(MetricOperator):
    """
    Accuracy is the proportion of correct predictions among the total number of cases processed.
    """
    metric_name = 'accuracy'

    def __init__(self,
                 topk: Union[int, Sequence[int]] = (1, ),
                 thresholds: Optional[float] = 0.5,
                 **kwargs):
        super(Accuracy, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.topk = topk
        self.reference_length_is_zero = False
        if self.topk in kwargs:
            self.topk = eval(kwargs[self.name]['topk'])
        if isinstance(self.topk, int):
            self.topk = (self.topk,)
        else:
            self.topk = tuple(self.topk)  # type: ignore
        self.maxk = max(self.topk)

        self.thresholds = thresholds
        if self.name in kwargs:
            self.thresholds = float(kwargs[self.name]['thresholds'])

        self.add_state("correct", default=[])

    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Computes and returns the middle states, such as correct number.
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

                corrects = (predictions == references)
                self.correct.append(corrects.astype(np.int32))
            else:
                if predictions.ndim == 1:
                    corrects = (predictions == references)
                    self.correct.append(corrects.astype(np.int32))
                else:
                    pred_scores, pred_label = _numpy_topk(predictions, self.maxk, axis=1)
                    pred_label = pred_label.T

                    references = np.broadcast_to(references.reshape(1, -1), pred_label.shape)
                    corrects = (pred_label == references)

                    corrects_per_sample = np.zeros((len(predictions), len(self.topk)))
                    for i, k in enumerate(self.topk):
                        corrects_per_sample[:, i] = corrects[:k].sum(0, keepdims=True).astype(np.int32)

                    self.correct.append(corrects_per_sample.astype(np.int32))

        if isinstance(predictions, PTensor):
            if self.num_classes == 2:
                if not paddle.all((predictions == 1) | (predictions == 0)):
                    predictions = (predictions > self.thresholds).cast(paddle.int32)

                corrects = (predictions.cast(references.dtype) == references)
                self.correct.append(corrects.cast(paddle.int32))
            else:
                if predictions.ndim == 1:
                    corrects = (predictions.cast(references.dtype) == references)
                    self.correct.append(corrects.cast(paddle.int32))
                else:
                    predictions = paddle.nn.functional.softmax(predictions, axis=-1)
                    pred_scores, pred_label = paddle.topk(predictions, self.maxk)
                    pred_label = pred_label.t()

                    corrects = (pred_label == references.reshape((1, -1)).expand_as(pred_label))

                    corrects_per_sample = paddle.zeros((len(predictions), len(self.topk)), 'int32')
                    for i, k in enumerate(self.topk):
                        corrects_per_sample[:, i] = corrects[:k].sum(0, keepdim=False).cast(paddle.int32)
                    self.correct.append(corrects_per_sample)

        if isinstance(predictions, TTensor):
            if self.num_classes == 2:
                if not torch.all((predictions == 1) | (predictions == 0)):
                    predictions = (predictions > self.thresholds).int()

                corrects = (predictions.int() == references)
                self.correct.append(corrects.int())
            else:
                if predictions.ndim == 1:
                    corrects = (predictions.int() == references)
                    self.correct.append(corrects.int())
                else:
                    predictions = torch.nn.functional.softmax(predictions, dim=-1)
                    pred_scores, pred_label = predictions.topk(self.maxk)
                    pred_label = pred_label.t()

                    corrects = (pred_label == references.view((1, -1)).expand_as(pred_label))

                    corrects_per_sample = torch.zeros((len(predictions), len(self.topk)))
                    for i, k in enumerate(self.topk):
                        corrects_per_sample[:, i] = corrects[:k].sum(0, keepdim=False).int()
                    self.correct.append(corrects_per_sample)

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        if self.reference_length_is_zero:
            if len(self.topk) == 1:
                return -1
            else:
                metric_results = [-1 for _ in self.topk]
                return metric_results

        self.correct = _status_stack(self.correct)

        if self.correct.ndim == 1:
            return round(float(sum(self.correct) / len(self.correct)), self.decimals)

        metric_results = []
        for i, k in enumerate(self.topk):
            corrects = [result[i] for result in self.correct]
            acc = float(sum(corrects) / len(corrects))
            metric_results.append(acc)

        metric_results = list_round(metric_results, decimals=self.decimals)

        return metric_results[0] if len(metric_results) == 1 else metric_results




