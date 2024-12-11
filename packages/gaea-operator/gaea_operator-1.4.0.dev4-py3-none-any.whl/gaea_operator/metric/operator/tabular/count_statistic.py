#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/23
# @Author  : yanxiaodong
# @File    : statistics.py
"""
from typing import List, Union, Any
import numpy as np

from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import check_input_num_classes
from gaea_operator.utils import list2ndarray


@METRIC.register_module('count_statistic')
class CountStatistic(MetricOperator):
    """
    Count statistics.
    """
    metric_name = 'count_statistic'

    def __init__(self, **kwargs):
        super(CountStatistic, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.add_state("anno", default=np.zeros(self.num_classes))

    def update(self, annotations: Union[List, np.ndarray]) -> None:
        """
        Computes and returns the middle states, such as sum etc.
        """

        annotations = list2ndarray(annotations)

        check_input_num_classes(predictions=annotations, num_classes=self.num_classes)

        sum_state = np.sum(annotations, axis=0)
        self.anno += sum_state

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        return self.anno.tolist()
