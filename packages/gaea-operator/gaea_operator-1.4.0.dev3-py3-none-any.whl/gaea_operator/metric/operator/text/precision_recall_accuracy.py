# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/7/25 15:15
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : precision_recall_accuracy.py
# @Software: PyCharm
"""
from typing import List, Union, Optional, Any

from ..metric import MetricOperator
from ..check import check_input_type
from gaea_operator.utils import Tensor
from gaea_operator.utils import METRIC


@METRIC.register_module('precision_recall_accuracy')
class PrecisionRecallAccuracy(MetricOperator):
    """
    PrecisionRecallAccuracy is a operator transform character to confusion matrix.
    """
    metric_name = 'precision_recall_accuracy'

    def __init__(self,
                 labels: Optional[List],
                 **kwargs):
        super(PrecisionRecallAccuracy, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.labels = labels
        self.add_state("tp_sum", default=0)
        self.add_state("tn_sum", default=0)
        self.add_state("fp_sum", default=0)
        self.add_state("fn_sum", default=0)

    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Accumulates the references and predictions.
        """
        check_input_type(predictions=predictions, references=references)
        for ref, pred in zip(references, predictions):
            # 判断是否是负样本（没有任何标注）
            is_negative_sample = ref == ""  # 假设 ref 为空字符串或 None 代表负样本

            if not is_negative_sample and ref == pred:
                self.tp_sum += 1

            if not is_negative_sample and ref != pred:
                self.fn_sum += 1

            if is_negative_sample and ref != pred:
                self.fp_sum += 1

            if is_negative_sample and ref == pred:
                self.tn_sum += 1

    def compute(self) -> Any:
        """
        Computes Precision, Recall, and Accuracy.
        """
        precision = self.tp_sum / (self.tp_sum + self.fp_sum) if (self.tp_sum + self.fp_sum) != 0 else -1.0
        # 计算 Recall
        recall = self.tp_sum / (self.tp_sum + self.fn_sum) if (self.tp_sum + self.fn_sum) != 0 else -1.0
        # 计算 Accuracy
        accuracy = (self.tp_sum + self.tn_sum) / (self.tp_sum + self.tn_sum + self.fp_sum + self.fn_sum) \
            if (self.tp_sum + self.tn_sum + self.fp_sum + self.fn_sum) != 0 else -1.0

        return precision, recall, accuracy
