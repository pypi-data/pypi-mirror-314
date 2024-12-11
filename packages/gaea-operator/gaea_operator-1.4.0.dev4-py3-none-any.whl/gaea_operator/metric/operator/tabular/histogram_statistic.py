#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/23
# @Author  : yanxiaodong
# @File    : histogram_statistics.py
"""
from typing import List, Union, Any, Tuple, Sequence, Dict, Optional
import numpy as np
from collections import defaultdict

from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from gaea_operator.utils import list2ndarray


def _parse_histogram_result(hist, bin_edges):
    """
    Parse the histogram result.
    """
    result = []
    for idx in range(len(hist)):
        result.append((hist[idx], bin_edges[idx], bin_edges[idx + 1]))

    return result


@METRIC.register_module('histogram_statistic')
class HistogramStatistic(MetricOperator):
    """
    Histogram Statistics.
    """
    metric_name = 'histogram_statistic'

    def __init__(self, labels: Optional[List], bins: Union[int, Sequence] = 10, range: Tuple = None, **kwargs):
        super(HistogramStatistic, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.bins = bins
        self.range = range
        self.labels = labels
        self.label_name2id = {label["name"]: label["id"] for idx, label in enumerate(self.labels)}

        self.add_state("anno", default={name: [] for name in self.label_name2id})

    def update(self, annotations: Dict) -> None:
        """
        Computes and returns the middle states.
        """
        for name, annotation in annotations.items():
            assert name in self.label_name2id, f"The prediction label name {name} must be in {self.label_name2id}."

            annotation = list2ndarray(annotation)

            if len(self.anno[name]) == 0:
                self.anno[name] = annotation
            else:
                self.anno[name] = np.concatenate([self.anno[name], annotation])

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        anno_result = defaultdict(list)
        for name, data in self.anno.items():
            if len(data) == 0:
                continue
            hist, bin_edges = np.histogram(data, bins=self.bins, range=self.range)
            result = _parse_histogram_result(hist, bin_edges)
            anno_result[name] = result

        return anno_result
