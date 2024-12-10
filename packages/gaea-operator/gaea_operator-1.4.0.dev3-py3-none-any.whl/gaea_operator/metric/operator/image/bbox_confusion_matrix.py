#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : confusion_matrix.py    
@Author        : yanxiaodong
@Date          : 2023/5/25
@Description   :
"""
from typing import List, Dict, Any
from collections import defaultdict
import copy

import numpy as np
from pycocotools import mask as mask_utils

from gaea_operator.utils import METRIC
from gaea_operator.utils import list_round
from ..metric import MetricOperator


@METRIC.register_module('bbox_confusion_matrix')
class BboxConfusionMatrix(MetricOperator):
    """
    Confusion matrix of the evaluation.
    """
    metric_name = 'bbox_confusion_matrix'

    def __init__(self, labels, conf_threshold: float = 0, iou_threshold: float = 0.5, **kwargs):
        super(BboxConfusionMatrix, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.labels = labels
        self.label_id2index = {label["id"]: idx for idx, label in enumerate(self.labels)}
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

        self.add_state("confmat", default=0)

    def _parse_dt_gt(self, predictions, groundths):
        img_ids = set()
        self._dts = defaultdict(list)
        self._gts = defaultdict(list)

        gts = copy.deepcopy(groundths)
        for gt in gts:
            if gt["image_id"] not in img_ids:
                img_ids.add(gt["image_id"])
            if 'bbox' in gt:
                self._gts[(gt['image_id'])].append(gt)

        for pred in predictions:
            if pred["image_id"] not in img_ids:
                img_ids.add(pred["image_id"])
            self._dts[(pred["image_id"])].append(pred)

        return img_ids

    def update(self, predictions: Dict[str, List[Dict]], references: Dict[str, List[Dict]]) -> None:
        """
        Computes and returns the middle states, such as TP, etc.
        """
        dts, gts = predictions, references
        img_ids = self._parse_dt_gt(dts['bbox'], gts['bbox'])
        confusion_matrix = np.zeros(shape=(self.num_classes + 1, self.num_classes + 1), dtype=np.int64)
        for img_id in img_ids:
            gt = self._gts[img_id]
            dt = self._dts[img_id]
            dt = [d for d in dt if d['score'] > self.conf_threshold]

            if len(gt) == 0 and len(dt) == 0:
                confusion_matrix[self.num_classes, self.num_classes] += 1
            elif len(gt) == 0 and len(dt) > 0:
                for d in dt:
                    confusion_matrix[self.num_classes, self.label_id2index[d['category_id']]] += 1
            elif len(gt) > 0 and len(dt) == 0:
                for g in gt:
                    confusion_matrix[self.label_id2index[g['category_id']], self.num_classes] += 1
            else:
                gtind = np.argsort([g['ignore'] if 'ignore' in g else 0 for g in gt], kind='mergesort')
                gt = [gt[i] for i in gtind]
                dtind = np.argsort([-d['score'] for d in dt], kind='mergesort')
                dt = [dt[i] for i in dtind]
                iscrowd = [int(o['iscrowd']) if 'iscrowd' in o else 0 for o in gt]

                gt_box = [g['bbox'] for g in gt]
                dt_box = [d['bbox'] for d in dt]
                ious = mask_utils.iou(dt_box, gt_box, iscrowd)

                iscrowd = [int(o['iscrowd']) if 'iscrowd' in o else 0 for o in gt]
                gtIg = np.array([g['ignore'] if 'ignore' in g else 0 for g in gt])
                gt_matched_index = np.ones(len(gt)) * -1

                for dind, d in enumerate(dt):
                    m = -1
                    label_m = -1
                    iou = self.iou_threshold
                    for gind, g in enumerate(gt):
                        # 如果gt已经匹配，则跳过
                        if gt_matched_index[gind] >= 0 and not iscrowd[gind]:
                            continue
                        # 如果dt匹配到gt并且no ignore, stop
                        if m > -1 and gtIg[m] == 0 and gtIg[gind] == 1 and label_m > -1:
                            break
                        # 如果iou小于阈值，则跳过
                        if ious[dind, gind] < self.iou_threshold:
                            continue
                        # 如果已有匹配当前dt和gt的类别不相同，则跳过
                        if m > -1 and label_m > -1 and d["category_id"] != g["category_id"]:
                            continue
                        # 如果iou小于已经匹配的iou，但是类别没有匹配，计算类别匹配，否则跳过
                        if ious[dind, gind] < iou:
                            if label_m == -1 and d["category_id"] == g["category_id"]:
                                iou = ious[dind, gind]
                                label_m = gind
                                m = gind
                            continue
                        else:
                            iou = ious[dind, gind]
                            m = gind
                            if d["category_id"] == g["category_id"]:
                                label_m = gind

                    if label_m > -1:
                        gt_matched_index[label_m] = label_m
                        index = self.label_id2index[gt[label_m]["category_id"]]
                        confusion_matrix[index, index] += 1
                    elif m > -1:
                        gt_matched_index[m] = m
                        g_index = self.label_id2index[gt[m]["category_id"]]
                        d_index = self.label_id2index[d["category_id"]]
                        confusion_matrix[g_index, d_index] += 1
                    else:
                        d_index = self.label_id2index[d["category_id"]]
                        confusion_matrix[self.num_classes, d_index] += 1

                gt_matched_index = set(np.asarray(gt_matched_index, dtype=np.int32))
                for gind, g in enumerate(gt):
                    if gind not in gt_matched_index:
                        g_index = self.label_id2index[g["category_id"]]
                        confusion_matrix[g_index, self.num_classes] += 1

        self.confmat += confusion_matrix

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        return self.confmat.tolist()


def precision_recall_f1_from_confusion_matrix(confusion_matrix: np.ndarray):
    """
    Computes the precision, recall and f1 score from the confusion matrix.
    """
    tps = np.diagonal(confusion_matrix)
    fps = np.sum(confusion_matrix, axis=0) - tps
    fns = np.sum(confusion_matrix, axis=1) - tps

    eps = 1e-16
    recall = [tp / (tp + fns[idx]) if (tp + fns[idx]) > 0 else -1 for idx, tp in enumerate(tps)]
    precision = [tp / (tp + fps[idx] + eps) if recall[idx] != -1 else -1 for idx, tp in enumerate(tps)]
    f1 = [(2 * precision[idx] * recall[idx]) / (precision[idx] + recall[idx] + eps) if precision[idx] != -1 else -1
          for idx, _ in enumerate(precision)]
    return list_round(precision[:-1], MetricOperator.decimals), \
        list_round(recall[:-1], MetricOperator.decimals), \
        list_round(f1[:-1], MetricOperator.decimals)

