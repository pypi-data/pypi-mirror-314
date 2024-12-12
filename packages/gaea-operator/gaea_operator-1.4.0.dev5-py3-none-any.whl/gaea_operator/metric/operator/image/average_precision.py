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
import warnings

from .precision_recall_curve import PrecisionRecallCurve
from gaea_operator.utils import Tensor
from gaea_operator.utils import METRIC
from gaea_operator.utils import numpy_round2list


@METRIC.register_module('average_precision')
class AveragePrecision(PrecisionRecallCurve):
    """
    The Area Under Precision-Recall Curve metric.
    """
    average_options = ['macro', 'none']
    metric_name = 'average_precision'

    def __init__(self,
                 average: Optional[str] = 'macro',
                 thresholds: Optional[Union[int, List[float], Tensor]] = None,
                 **kwargs):
        super(AveragePrecision, self).__init__(num_classes=kwargs.get('num_classes', 2), thresholds=thresholds)

        self.average = average
        if self.average in kwargs:
            self.average = kwargs[self.name]['average']

        assert self.average in self.average_options, f'Invalid `average` argument: {self.average}, ' \
                                                     f'please specify from {self.average_options}.'

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        precision, recall, _ = super(AveragePrecision, self).compute()
        precision = np.array(precision)
        recall = np.array(recall)
        if self.num_classes == 2:
            return round(-np.sum((recall[1:] - recall[:-1]) * precision[:-1]), self.decimals)
        else:
            res = []
            if isinstance(precision[0], np.ndarray):
                res = -np.sum((recall[:, 1:] - recall[:, :-1]) * precision[:, :-1], axis=1)
            else:
                for p, r in zip(precision, recall):
                    p = np.array(p)
                    r = np.array(r)
                    res.append(-np.sum((r[1:] - r[:-1]) * p[:-1]))
                res = np.array(res)

            if self.average is None or self.average == self.average_options[1]:
                return numpy_round2list(res, decimals=self.decimals)
            else:
                if np.isnan(res).any():
                    warnings.warn(f"Average precision score {res} for one or more classes was `nan`. "
                                  f"Ignoring these classes.")
                idx = ~ np.isnan(res)
                return round(np.mean(res[idx]), self.decimals)