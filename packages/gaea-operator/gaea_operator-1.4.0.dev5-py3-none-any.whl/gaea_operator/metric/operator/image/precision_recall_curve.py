#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : average_precision.py    
@Author        : yanxiaodong
@Date          : 2023/5/25
@Description   :
"""
from typing import List, Union, Optional, Any
import numpy as np

from gaea_operator.utils import paddle, torch, PTensor, TTensor, Tensor
from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import average_precision_check_input_dim, check_input_type
from gaea_operator.utils import list2ndarray, numpy_round2list, torch_round2list, paddle_round2list


def _dim_zero_cat(x: Union[PTensor, TTensor, List[Tensor]]):
    """
    Concatenation along the zero dimension.
    """
    x = x if isinstance(x, (list, tuple)) else [x]
    _x = []
    for y in x:
        if isinstance(y, np.ndarray):
            if y.size == 1 and y.ndim == 0:
                _x.append(np.expand_dims(y, axis=0))
            else:
                _x.append(y)
        if isinstance(y, PTensor):
            if y.size == 1 and y.ndim == 1:
                _x.append(y.unsqueeze(0))
            else:
                _x.append(y)
        if isinstance(y, TTensor):
            if y.size == 1 and y.ndim == 0:
                _x.append(y.unsqueeze(0))
            else:
                _x.append(y)

    if isinstance(_x[0], np.ndarray):
        return np.concatenate(_x, axis=0)
    if isinstance(_x[0], PTensor):
        return paddle.concat(_x, axis=0)
    if isinstance(_x[0], TTensor):
        return torch.cat(_x, dim=0)


def _safe_divide(num: Tensor, denom: Tensor):
    """
    Safe division, by preventing division by zero.
    """
    denom[denom == 0] = 1
    return num / denom


def _binary_clf_torch(preds: TTensor, target: TTensor, pos_label: int = 1):
    """
    Calculates the tps and false positives for all unique thresholds in the preds for torch.
    """
    # remove class dimension if necessary
    if preds.ndim > target.ndim:
        preds = preds[:, 0]
    desc_score_indices = torch.argsort(preds, descending=True)

    preds = preds[desc_score_indices]
    target = target[desc_score_indices]

    distinct_value_indices = torch.where(preds[1:] - preds[:-1])[0]
    threshold_idxs = torch.nn.functional.pad(distinct_value_indices, [0, 1], value=target.size(0) - 1)
    target = (target == pos_label).to(torch.long)
    tps = torch.cumsum(target, dim=0)[threshold_idxs]

    fps = 1 + threshold_idxs - tps

    return fps, tps, preds[threshold_idxs]


def _binary_compute_torch(tps: TTensor, fps: TTensor, thresholds_c: TTensor, decimals: int = 4):
    """
    Calculates the precision and recall.
    """
    precision = _safe_divide(tps, tps + fps)
    recall = tps / tps[-1]

    last_ind = torch.where(tps == tps[-1])[0][0]
    sl = slice(0, int(last_ind) + 1)

    precision_c = torch.cat(
        [precision[sl].flip(0), torch.ones(1, dtype=precision.dtype)])
    recall_c = torch.cat([recall[sl].flip(0), torch.zeros(1, dtype=recall.dtype)])
    thresholds_c = thresholds_c[sl].flip(0)

    precision_c = torch_round2list(value=precision_c, decimals=decimals)
    recall_c = torch_round2list(value=recall_c, decimals=decimals)
    thresholds_c = torch_round2list(value=thresholds_c, decimals=decimals)

    return precision_c, recall_c, thresholds_c


def _binary_clf_paddle(preds: PTensor, target: PTensor, pos_label: int = 1):
    """
    Calculates the tps and false positives for all unique thresholds in the preds for paddlepaddle.
    """
    if preds.ndim > target.ndim:
        preds = preds[:, 0]
    desc_score_indices = paddle.argsort(preds, descending=True)

    preds = preds[desc_score_indices]
    target = target[desc_score_indices]

    distinct_value_indices = paddle.where(preds[1:] - preds[:-1])[0]
    distinct_value_indices = distinct_value_indices.unsqueeze(axis=0)
    threshold_idxs = paddle.nn.functional.pad(distinct_value_indices, [0, 1], value=target.size - 1, data_format='NLC')
    threshold_idxs = threshold_idxs.squeeze(axis=0).squeeze(axis=0)

    target = target == pos_label
    tps = paddle.cumsum(target.cast(paddle.int32), axis=0)[threshold_idxs]

    fps = 1 + threshold_idxs - tps
    thresholds_c = preds[threshold_idxs]

    if tps.ndim == 2:
        tps = tps.squeeze(axis=1)
    if fps.ndim == 2:
        fps = fps.squeeze(axis=1)
    if thresholds_c.ndim == 2:
        thresholds_c = thresholds_c.squeeze(axis=1)

    return fps, tps, thresholds_c


def _binary_compute_paddle(tps: PTensor, fps: PTensor, thresholds_c: PTensor, decimals: int = 4):
    """
    Calculates the precision and recall.
    """
    precision = _safe_divide(tps, tps + fps)
    recall = tps / tps[-1]

    last_ind = paddle.where(tps == tps[-1])[0][0]
    sl = slice(0, int(last_ind) + 1)

    precision_c = paddle.concat([precision[sl].flip(0), paddle.ones([1], dtype=precision.dtype)])
    recall_c = paddle.concat([recall[sl].flip(0), paddle.zeros([1], dtype=recall.dtype)])
    thresholds_c = thresholds_c[sl].flip(0)

    precision_c = paddle_round2list(value=precision_c, decimals=decimals)
    recall_c = paddle_round2list(value=recall_c, decimals=decimals)
    thresholds_c = paddle_round2list(value=thresholds_c, decimals=decimals)

    return precision_c, recall_c, thresholds_c


def _binary_clf_numpy(preds: np.ndarray, target: np.ndarray, pos_label: int = 1):
    """
    Calculates the tps and false positives for all unique thresholds in the preds for numpy.
    """
    if preds.ndim > target.ndim:
        preds = preds[:, 0]
    # 降序排列
    desc_score_indices = np.argsort(preds)[::-1]

    preds = preds[desc_score_indices]
    target = target[desc_score_indices]

    distinct_value_indices = np.where(preds[1:] - preds[:-1])[0]
    threshold_idxs = np.pad(distinct_value_indices, [0, 1], 'constant', constant_values=(0, target.size - 1))
    target = target == pos_label
    tps = np.cumsum(target, axis=0)[threshold_idxs]

    fps = 1 + threshold_idxs - tps

    return fps, tps, preds[threshold_idxs]


def _binary_compute_numpy(tps: np.ndarray, fps: np.ndarray, thresholds_c: np.ndarray, decimals: int = 4):
    """
    Calculates the precision and recall.
    """
    precision = _safe_divide(tps, tps + fps)
    recall = tps / tps[-1]

    last_ind = np.where(tps == tps[-1])[0][0]
    sl = slice(0, int(last_ind) + 1)

    precision_c = np.concatenate([np.flip(precision[sl], axis=0), np.ones(1, dtype=precision.dtype)])
    recall_c = np.concatenate([np.flip(recall[sl], axis=0), np.zeros(1, dtype=recall.dtype)])
    thresholds_c = np.flip(thresholds_c[sl], axis=0)

    precision_c = numpy_round2list(value=precision_c, decimals=decimals)
    recall_c = numpy_round2list(value=recall_c, decimals=decimals)
    thresholds_c = numpy_round2list(value=thresholds_c, decimals=decimals)

    return precision_c, recall_c, thresholds_c


@METRIC.register_module('precision_recall_curve')
class PrecisionRecallCurve(MetricOperator):
    """
    The Precision-Recall Curve metric.
    """
    metric_name = 'average_precision_curve'

    def __init__(self, thresholds: Optional[Union[int, List[float], Tensor]] = None, **kwargs):
        super(PrecisionRecallCurve, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.thresholds = thresholds
        if self.name in kwargs:
            self.thresholds = eval((kwargs[self.name]['thresholds']))

        if isinstance(self.thresholds, int):
            self.thresholds = np.linspace(0, 1, self.thresholds)
        if isinstance(self.thresholds, List):
            self.thresholds = np.array(self.thresholds)

        if self.thresholds is None:
            self.add_state("preds", default=[])
            self.add_state("target", default=[])
        else:
            self.add_state("confmat", default=0)

    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Computes and returns the middle states, such as precision, recall, etc.
        """
        check_input_type(predictions=predictions, references=references)

        predictions = list2ndarray(predictions)
        references = list2ndarray(references)

        average_precision_check_input_dim(predictions=predictions, num_classes=self.num_classes)

        if isinstance(predictions, np.ndarray):
            if self.thresholds is None:
                self.preds.append(predictions)
                self.target.append(references)
            else:
                len_t = len(self.thresholds)
                if self.num_classes == 2:
                    # num_samples x num_thresholds
                    preds_t = np.expand_dims(predictions, axis=-1) >= np.expand_dims(self.thresholds, axis=0)
                    unique_mapping = preds_t + 2 * np.expand_dims(references, axis=-1) + 4 * np.arange(len_t)
                    bins = np.bincount(unique_mapping.flatten(), minlength=4 * len_t)
                    state = bins.reshape((len_t, 2, 2))
                else:
                    # num_samples x num_classes x num_thresholds
                    preds_t = np.expand_dims(predictions, axis=-1) >= \
                              np.expand_dims(np.expand_dims(self.thresholds, axis=0), axis=0)
                    target_t = np.eye(self.num_classes, dtype=np.int32)[references]
                    unique_mapping = preds_t + 2 * np.expand_dims(target_t, axis=-1)
                    unique_mapping += 4 * np.expand_dims(np.expand_dims(np.arange(self.num_classes), axis=0), axis=-1)
                    unique_mapping += 4 * self.num_classes * np.arange(len_t)
                    bins = np.bincount(unique_mapping.flatten(), minlength=4 * self.num_classes * len_t)
                    state = bins.reshape((len_t, self.num_classes, 2, 2))

                self.confmat += state

        if isinstance(predictions, PTensor):
            if self.thresholds is None:
                self.preds.append(predictions)
                self.target.append(references)
            else:
                self.thresholds = paddle.to_tensor(self.thresholds)
                len_t = len(self.thresholds)
                if self.num_classes == 2:
                    # num_samples x num_thresholds
                    preds_t = predictions.unsqueeze(-1) >= self.thresholds.unsqueeze(0)

                    unique_mapping = preds_t.cast(paddle.int32) + \
                                     2 * references.unsqueeze(-1) + \
                                     4 * paddle.arange(len_t)
                    # paddle.bincount gpu计算不符合预期
                    # bins = paddle.bincount(unique_mapping.flatten(), minlength=4 * len_t)
                    bins = np.bincount(unique_mapping.flatten().numpy(), minlength=4 * len_t)
                    bins = paddle.to_tensor(bins)

                    state = bins.reshape((len_t, 2, 2))
                else:
                    preds_t = predictions.unsqueeze(-1) >= self.thresholds.unsqueeze(0).unsqueeze(0)
                    target_t = paddle.nn.functional.one_hot(references, num_classes=self.num_classes)
                    unique_mapping = preds_t.cast(paddle.int32) + 2 * target_t.unsqueeze(-1)
                    unique_mapping += 4 * paddle.arange(self.num_classes).unsqueeze(0).unsqueeze(-1)
                    unique_mapping += 4 * self.num_classes * paddle.arange(len_t)
                    # bins = paddle.bincount(unique_mapping.flatten(), minlength=4 * self.num_classes * len_t)
                    bins = np.bincount(unique_mapping.flatten().numpy(), minlength=4 * self.num_classes * len_t)
                    bins = paddle.to_tensor(bins)

                    state = bins.reshape((len_t, self.num_classes, 2, 2))

                self.confmat += state
        if isinstance(predictions, TTensor):
            if self.thresholds is None:
                self.preds.append(predictions)
                self.target.append(references)
            else:
                self.thresholds = torch.from_numpy(self.thresholds)
                len_t = len(self.thresholds)
                if self.num_classes == 2:
                    # num_samples x num_thresholds
                    preds_t = predictions.unsqueeze(-1) >= self.thresholds.unsqueeze(0)
                    unique_mapping = preds_t + 2 * references.unsqueeze(-1) + 4 * torch.arange(len_t)
                    bins = torch.bincount(unique_mapping.flatten(), minlength=4 * len_t)
                    state = bins.reshape((len_t, 2, 2))
                else:
                    preds_t = predictions.unsqueeze(-1) >= self.thresholds.unsqueeze(0).unsqueeze(0)
                    target_t = torch.nn.functional.one_hot(references, num_classes=self.num_classes)
                    unique_mapping = preds_t + 2 * target_t.unsqueeze(-1)
                    unique_mapping += 4 * torch.arange(self.num_classes).unsqueeze(0).unsqueeze(-1)
                    unique_mapping += 4 * self.num_classes * torch.arange(len_t)
                    bins = torch.bincount(unique_mapping.flatten(), minlength=4 * self.num_classes * len_t)
                    state = bins.reshape((len_t, self.num_classes, 2, 2))

                self.confmat += state

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        if self.thresholds is None:
            state = [_dim_zero_cat(self.preds), _dim_zero_cat(self.target)]
        else:
            state = self.confmat

        if isinstance(state, PTensor):
            tps = state[..., 1, 1]
            fps = state[..., 0, 1]
            fns = state[..., 1, 0]

            precision = _safe_divide(tps, tps + fps)
            recall = _safe_divide(tps, tps + fns)

            if self.num_classes == 2:
                size = (1,)
            else:
                size = (1, self.num_classes)

            precision = paddle.concat([precision, paddle.ones(size, dtype=precision.dtype)])
            recall = paddle.concat([recall, paddle.zeros(size, dtype=recall.dtype)])

            precision = paddle_round2list(value=precision.T, decimals=self.decimals)
            recall = paddle_round2list(value=recall.T, decimals=self.decimals)
            thresholds = paddle_round2list(value=self.thresholds, decimals=self.decimals)

        elif isinstance(state, TTensor):
            tps = state[:, :, 1, 1]
            fps = state[:, :, 0, 1]
            fns = state[:, :, 1, 0]

            precision = _safe_divide(tps, tps + fps)
            recall = _safe_divide(tps, tps + fns)

            if self.num_classes == 2:
                size = 1
            else:
                size = (1, self.num_classes)

            precision = torch.cat([precision, torch.ones(size, dtype=precision.dtype)])
            recall = torch.cat([recall, torch.zeros(size, dtype=recall.dtype, device=recall.device)])

            precision = torch_round2list(value=precision.T, decimals=self.decimals)
            recall = torch_round2list(value=recall.T, decimals=self.decimals)
            thresholds = torch_round2list(value=self.thresholds, decimals=self.decimals)

        elif isinstance(state, np.ndarray):
            tps = state[..., 1, 1]
            fps = state[..., 0, 1]
            fns = state[..., 1, 0]

            precision = _safe_divide(tps, tps + fps)
            recall = _safe_divide(tps, tps + fns)

            if self.num_classes == 2:
                size = 1
            else:
                size = (1, self.num_classes)
            precision = np.concatenate([precision, np.ones(size, dtype=precision.dtype)])
            recall = np.concatenate([recall, np.zeros(size, dtype=recall.dtype)])

            precision = numpy_round2list(value=precision.T, decimals=self.decimals)
            recall = numpy_round2list(value=recall.T, decimals=self.decimals)
            thresholds = numpy_round2list(value=self.thresholds, decimals=self.decimals)
        else:
            if self.num_classes == 2:
                if isinstance(state[0], TTensor):
                    fps, tps, thresholds_c = _binary_clf_torch(state[0], state[1], pos_label=1)

                    precision, recall, thresholds = _binary_compute_torch(fps=fps,
                                                                          tps=tps,
                                                                          thresholds_c=thresholds_c,
                                                                          decimals=self.decimals)

                if isinstance(state[0], PTensor):
                    fps, tps, thresholds_c = _binary_clf_paddle(state[0], state[1], pos_label=1)

                    precision, recall, thresholds = _binary_compute_paddle(fps=fps,
                                                                           tps=tps,
                                                                           thresholds_c=thresholds_c,
                                                                           decimals=self.decimals)

                if isinstance(state[0], np.ndarray):
                    fps, tps, thresholds_c = _binary_clf_numpy(state[0], state[1], pos_label=1)

                    precision, recall, thresholds = _binary_compute_numpy(fps=fps,
                                                                          tps=tps,
                                                                          thresholds_c=thresholds_c,
                                                                          decimals=self.decimals)
            else:
                precision, recall, thresholds = [], [], []
                precision_c, recall_c, thresholds_c = 0, 0, 0
                for i in range(self.num_classes):
                    if isinstance(state[0], TTensor):
                        fps, tps, thresholds_c = _binary_clf_torch(state[0][:, i], state[1], pos_label=i)

                        precision_c, recall_c, thresholds_c = _binary_compute_torch(fps=fps,
                                                                                    tps=tps,
                                                                                    thresholds_c=thresholds_c,
                                                                                    decimals=self.decimals)

                    if isinstance(state[0], PTensor):
                        fps, tps, thresholds_c = _binary_clf_paddle(state[0][:, i], state[1], pos_label=i)

                        precision_c, recall_c, thresholds_c = _binary_compute_paddle(fps=fps,
                                                                                     tps=tps,
                                                                                     thresholds_c=thresholds_c,
                                                                                     decimals=self.decimals)

                    if isinstance(state[0], np.ndarray):
                        fps, tps, thresholds_c = _binary_clf_numpy(state[0][:, i], state[1], pos_label=i)

                        precision_c, recall_c, thresholds_c = _binary_compute_numpy(fps=fps,
                                                                                    tps=tps,
                                                                                    thresholds_c=thresholds_c,
                                                                                    decimals=self.decimals)

                    precision.append(precision_c)
                    recall.append(recall_c)
                    thresholds.append(thresholds_c)

        return precision, recall, thresholds
