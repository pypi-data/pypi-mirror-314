# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/7/25 15:15
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : precision_recall_accuracy.py
# @Software: PyCharm
"""
import numpy as np
from shapely.geometry import Polygon
from collections import defaultdict

from ..metric import MetricOperator
from gaea_operator.utils import METRIC


@METRIC.register_module('precision_recall_hmean')
class PrecisionRecallHmean(MetricOperator):
    """
    PrecisionRecallHmean is an operator to calculate precision, recall, and hmean metrics.
    """
    metric_name = 'precision_recall_hmean'

    def __init__(self, conf_threshold: float = 0, iou_threshold: float = 0.5, **kwargs):
        super(PrecisionRecallHmean, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.add_state("tp_sum", default=0)
        self.add_state("pred_sum", default=0)
        self.add_state("gt_sum", default=0)
        self._dts = defaultdict(list)
        self._gts = defaultdict(list)

    def get_union(self, pD, pG):
        """
        Calculates the union area between two polygons.
        """
        return Polygon(pD).union(Polygon(pG)).area

    def get_intersection(self, pD, pG):
        """
        Calculates the intersection area between two polygons.
        """
        return Polygon(pD).intersection(Polygon(pG)).area

    def get_intersection_over_union(self, pD, pG):
        """
        Calculates the intersection over union (IoU) between two polygons.
        """
        union_area = self.get_union(pD, pG)
        if union_area == 0:  # Avoid division by zero
            return -1
        intersection_area = self.get_intersection(pD, pG)
        return intersection_area / union_area

    def _parse_dt_gt(self, predictions, groundtruths):
        img_ids = set()
        for gt in groundtruths:
            img_ids.add(gt["image_id"])
            self._gts[gt['image_id']].append(gt)
        for pred in predictions:
            img_ids.add(pred["image_id"])
            self._dts[pred["image_id"]].append(pred)
        return img_ids

    def _convert_to_polygon(self, coordinates):
        """
        Converts a list of coordinates representing a quadrangle into a polygon.
        """
        # Assuming `coordinates` is a flat list of coordinates like [x1, y1, x2, y2, x3, y3, x4, y4]
        # Convert this directly to a polygon format
        if len(coordinates) != 8:
            raise ValueError("Coordinates must contain exactly 8 values (for 4 points).")

        # Create polygon format (assumed here as a list of tuples)
        return [
            (coordinates[i], coordinates[i + 1])
            for i in range(0, len(coordinates), 2)
        ]

    def update(self, predictions, references):
        """
        Update the state with the given predictions and references.
        """
        img_ids = self._parse_dt_gt(predictions, references)

        for img_id in img_ids:
            img_predictions = self._dts.get(img_id, [])
            img_references = self._gts.get(img_id, [])

            img_predictions = [p for p in img_predictions if p["confidence"] > self.conf_threshold]

            if len(img_references) == 0 and len(img_predictions) == 0:
                continue
            elif len(img_references) == 0:
                self.pred_sum += len(img_predictions)
                continue
            elif len(img_predictions) == 0:
                self.gt_sum += len(img_references)
                continue

            pred_polygons = [self._convert_to_polygon(p["quadrangle"]) for p in img_predictions]
            gt_polygons = [self._convert_to_polygon(g["quadrangle"]) for g in img_references]

            ious = np.zeros((len(pred_polygons), len(gt_polygons)))

            for i, pred_polygon in enumerate(pred_polygons):
                for j, gt_polygon in enumerate(gt_polygons):
                    ious[i, j] = self.get_intersection_over_union(pred_polygon, gt_polygon)

            gt_matched = np.full(len(gt_polygons), -1, dtype=int)

            for dind, d in enumerate(pred_polygons):
                best_iou = -1
                best_gind = -1
                for gind, g in enumerate(gt_polygons):
                    if gt_matched[gind] >= 0:
                        continue
                    if ious[dind, gind] < self.iou_threshold:
                        continue
                    if ious[dind, gind] > best_iou:
                        best_iou = ious[dind, gind]
                        best_gind = gind

                if best_gind >= 0:
                    gt_matched[best_gind] = dind
                    self.tp_sum += 1

            self.pred_sum += len(pred_polygons)
            self.gt_sum += len(gt_polygons)

    def compute(self):
        """
        Compute the precision, recall, and hmean metrics.
        """
        precision = -1
        recall = -1
        hmean = -1
        if self.pred_sum > 0:
            precision = self.tp_sum / self.pred_sum
        if self.gt_sum > 0:
            recall = self.tp_sum / self.gt_sum
        if precision + recall > 0:
            hmean = 2 * (precision * recall) / (precision + recall)
        return precision, recall, hmean
