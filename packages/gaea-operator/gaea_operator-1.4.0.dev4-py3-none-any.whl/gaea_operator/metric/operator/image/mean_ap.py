#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : object_detection.py
@Author        : yanxiaodong
@Date          : 2023/6/30
@Description   :
"""
from typing import List, Union, Optional, Sequence, Any, Dict
from collections import defaultdict
import copy
import numpy as np
import sys
import itertools
from pycocotools.cocoeval import COCOeval
from pycocotools import mask as mask_utils

from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import is_list_of
from gaea_operator.utils import list_round
import bcelogger

def create_nd_list(shape: tuple):
    """创建n维列表

    Args:
        shape (tuple): 形状

    Returns:
        list: 多维列表
    """
    item = []
    for s in reversed(shape):
        container = [copy.deepcopy(item) for i in range(s)]
        item = container
    return container


def ann_to_rle(ann):
    """
    Convert annotation which can be polygons, uncompressed RLE to RLE.
    :return: binary mask (numpy 2D array)
    """
    h, w = ann['height'], ann['width']
    segm = ann['segmentation']
    if type(segm) == list:
        # polygon -- a single object might consist of multiple parts
        # we merge all parts into one mask rle code
        rles = mask_utils.frPyObjects(segm, h, w)
        rle = mask_utils.merge(rles)
    elif type(segm['counts']) == list:
        # uncompressed RLE
        rle = mask_utils.frPyObjects(segm, h, w)
    else:
        # rle
        rle = ann['segmentation']
    return rle


COCO_SIGMAS = (
        np.array(
            [
                0.26,
                0.25,
                0.25,
                0.35,
                0.35,
                0.79,
                0.79,
                0.72,
                0.72,
                0.62,
                0.62,
                1.07,
                1.07,
                0.87,
                0.87,
                0.89,
                0.89,
            ]
        )
        / 10.0
)
CROWD_SIGMAS = (
        np.array(
            [
                0.79,
                0.79,
                0.72,
                0.72,
                0.62,
                0.62,
                1.07,
                1.07,
                0.87,
                0.87,
                0.89,
                0.89,
                0.79,
                0.79,
            ]
        )
        / 10.0
)


class DistCocoEval(COCOeval):
    """_summary_

    Args:
        COCOeval (_type_): _description_
    """

    def __init__(self,
                 cocoGt=None,
                 cocoDt=None,
                 iouThrs=None,
                 areaRng=None,
                 maxDets=None,
                 iouType='segm',
                 categories=[]):
        super().__init__(cocoGt, cocoDt, iouType=iouType)
        self.iouType = iouType
        if maxDets is not None:
            self.params.maxDets = maxDets
        if areaRng is not None:
            self.params.areaRng = areaRng
        if iouThrs is not None:
            self.params.iouThrs = iouThrs
        if len(categories) > 0 and isinstance(categories[0], dict):
            self.cat_ids = [cate['id'] for cate in categories]
        else:
            self.cat_ids = categories
        self.prepare()
        self.reset()

    def prepare(self):
        """
        Prepare some variables for evaluation
        """
        p = self.params
        print("Evaluate annotation type *{}*".format(p.iouType))
        if p.useCats:
            p.catIds = list(np.unique(self.cat_ids))
        p.maxDets = sorted(p.maxDets)
        if p.iouType == "segm" or p.iouType == "bbox":
            self.compute_iou = self.computeIoU
        elif p.iouType == "keypoints":
            self.compute_iou = self.computeOks
        self.params = p

    def reset(self):
        """
        重置eval_imgs_all
        """
        K = len(self.cat_ids)
        A = len(self.params.areaRng)
        self.eval_imgs_all = create_nd_list((K, A))
        self.eval = {}
        self.cur_dtid = 0

    def _parse_dt_gt(self, predictions, groundths):
        """解析当前batch产出的预测结果

        Args:
            predictions (list): _description_

        Returns:
            tuple(set, dict): 当前batch对应的image_ids和对应image_id、category_id的预测结果
        """
        img_ids = set()
        self._dts = defaultdict(list)
        self._gts = defaultdict(list)

        gts = copy.deepcopy(groundths)
        if len(gts) <= 0:
            bcelogger.warning('gt is empty')
        
        for gt in gts:
            if gt["image_id"] not in img_ids:
                img_ids.add(gt["image_id"])

            if self.params.iouType == "segm":
                # all segmentation change to rle
                if 'segmentation' in gt:
                    rles = mask_utils.frPyObjects(gt['segmentation'], gt['height'], gt['width'])
                    rle = mask_utils.merge(rles)
                    gt['segmentation'] = rle
                    gt["area"] = mask_utils.area(gt['segmentation'])
                    self._gts[(gt['image_id'], gt['category_id'])].append(gt)
                else:
                    bcelogger.warning('gt format is invalid. need segmentation {}'.format(gt))

            if self.params.iouType == "bbox":
                if 'bbox' in gt:
                    gt["area"] = gt['bbox'][2] * gt['bbox'][3] if len(gt['bbox']) > 0 else 0
                    self._gts[(gt['image_id'], gt['category_id'])].append(gt)

        for pred in predictions:
            if pred["image_id"] not in img_ids:
                img_ids.add(pred["image_id"])

            if self.params.iouType == "segm":
                if 'segmentation' in pred:
                    if len(pred['segmentation'][0]) > 0:
                        if len(pred['segmentation'][0]) < 5:
                            # pending
                            for _ in range(5 - len(pred['segmentation'][0])):
                                pred['segmentation'][0].append(pred['segmentation'][0][-1])
                        rles = mask_utils.frPyObjects(pred['segmentation'], pred['height'], pred['width'])
                        rle = mask_utils.merge(rles)
                        pred['segmentation'] = rle
                        pred["area"] = mask_utils.area(rle)
                    else:
                        bcelogger.warning('pred mask is empty')
                        pred["area"] = 0
                else:
                    bcelogger.warning('no segmentation key-word in prediction when iouType==segm')
                    pred['area'] = 0
            if self.params.iouType == "bbox":
                if 'bbox' in pred:
                    pred["area"] = pred['bbox'][2] * pred['bbox'][3] if len(pred['bbox']) > 0 else 0

            pred['id'] = self.cur_dtid
            self.cur_dtid += 1
            self._dts[(pred["image_id"], pred["category_id"])].append(pred)

        return img_ids

    def evaluate_batch(self, dts: List[Dict], gts: List[Dict]):
        """获得当前batch的评估结果

        Args:
            img_ids (List[int]): _description_
            dts (List[Dict]): _description_
            gts (List[Dict]): _description_
        Returns:
            Dict[List]: _description_
        """
        img_ids = self._parse_dt_gt(dts, gts)
        p = self.params
        # loop through images, area range, max detection number
        cat_ids = self.cat_ids

        self.ious = {
            (img_id, cat_id): self.compute_iou(img_id, cat_id)
            for img_id in img_ids
            for cat_id in cat_ids
        }

        max_det = p.maxDets[-1]
        for k, cat_id in enumerate(cat_ids):
            for a, area_rng in enumerate(p.areaRng):
                eval_imgs = [
                    self.evaluateImg(img_id, cat_id, area_rng, max_det)
                    for img_id in img_ids
                ]
                self.eval_imgs_all[k][a].extend(eval_imgs)

    def accumulate_rank(self):
        """
        Accumulate per image evaluation results and store the result in self.eval
        :return: None
        """
        print("Accumulating evaluation results...")
        # allows input customized parameters
        p = self.params
        p.catIds = p.catIds if p.useCats == 1 else [-1]
        T = len(p.iouThrs)
        R = len(p.recThrs)
        K = len(p.catIds) if p.useCats else 1
        A = len(p.areaRng)
        M = len(p.maxDets)
        # -1 for the precision of absent categories
        precision = -np.ones(
            (T, R, K, A, M)
        )
        recall = -np.ones((T, K, A, M))
        scores = -np.ones((T, R, K, A, M))

        # create dictionary for future indexing
        _pe = self.params
        catIds = _pe.catIds if _pe.useCats else [-1]
        setK = set(catIds)
        setA = set(map(tuple, _pe.areaRng))
        setM = set(_pe.maxDets)
        # get inds to evaluate
        k_list = [n for n, k in enumerate(p.catIds) if k in setK]
        k_list2catId = {n: k for n, k in enumerate(p.catIds) if k in setK}
        m_list = [m for n, m in enumerate(p.maxDets) if m in setM]
        a_list = [
            n for n, a in enumerate(map(lambda x: tuple(x), p.areaRng)) if a in setA
        ]
        # retrieve E at each category, area range, and max number of detections
        for k in range(len(k_list)):
            for a in range(len(a_list)):
                for m, max_det in enumerate(m_list):
                    res = self.get_tp_fp(self.eval_imgs_all[k][a], max_det)
                    if res is None:
                        continue
                    npig = res["npig"]
                    tps = res["tps"]
                    fps = res["fps"]
                    dt_score_sorted = res["dt_scores"]

                    tp_sum = np.cumsum(tps, axis=1).astype(dtype=np.float32)
                    fp_sum = np.cumsum(fps, axis=1).astype(dtype=np.float32)
                    for t, (tp, fp) in enumerate(zip(tp_sum, fp_sum)):
                        tp = np.array(tp)
                        fp = np.array(fp)
                        nd = len(tp)
                        rc = tp / npig
                        pr = tp / (fp + tp + np.spacing(1))
                        q = np.zeros((R,))
                        ss = np.zeros((R,))

                        if nd:
                            recall[t, k, a, m] = rc[-1]
                        else:
                            recall[t, k, a, m] = 0

                        # numpy is slow without cython optimization for accessing elements
                        # use python array gets significant speed improvement
                        pr = pr.tolist()
                        q = q.tolist()

                        for i in range(nd - 1, 0, -1):
                            if pr[i] > pr[i - 1]:
                                pr[i - 1] = pr[i]

                        inds = np.searchsorted(rc, p.recThrs, side="left")
                        try:
                            for ri, pi in enumerate(inds):
                                q[ri] = pr[pi]
                                ss[ri] = dt_score_sorted[pi]
                        except Exception as e:
                            pass
                        precision[t, :, k, a, m] = np.array(q)
                        scores[t, :, k, a, m] = np.array(ss)

        self.eval = {
            "precision": precision,
            "recall": recall,
            "scores": scores,
        }
        return self.eval

    def get_tp_fp(self, eval_imgs: List[Dict], max_det: int):
        """_summary_

        Args:
            eval_imgs (list): 一个list里边都是包含匹配关系的dict
            max_det (int): 最大检出数
        """
        E = eval_imgs
        E = [e for e in E if not e is None]
        if len(E) == 0:
            return None
        dtScores = np.concatenate([e["dtScores"][0:max_det] for e in E])

        # different sorting method generates slightly different results.
        # mergesort is used to be consistent as Matlab implementation.
        inds = np.argsort(-dtScores, kind="mergesort")
        dt_score_sorted = dtScores[inds]

        dtm = np.concatenate([e["dtMatches"][:, 0:max_det]
                              for e in E], axis=1)[:, inds]
        dtIg = np.concatenate([e["dtIgnore"][:, 0:max_det]
                               for e in E], axis=1)[:, inds]
        gtIg = np.concatenate([e["gtIgnore"] for e in E])
        npig = np.count_nonzero(gtIg == 0)
        if npig == 0:
            return None
        tps = np.logical_and(dtm, np.logical_not(dtIg))
        fps = np.logical_and(np.logical_not(dtm), np.logical_not(dtIg))
        return {"tps": tps, "fps": fps, "npig": npig, "dt_scores": dt_score_sorted}


@METRIC.register_module('mean_ap')
class MeanAveragePrecision(MetricOperator):
    """
    Computes the `Mean-Average-Precision (mAP) and Mean-Average-Recall (mAR)` for object detection predictions.
    Optionally, the mAP and mAR values can be calculated per class.
    """
    metric_name = 'mean_ap'

    def __init__(self,
                 iou_threshold: Optional[float] = None,
                 iou_thrs: Union[float, Sequence[float], None] = None,
                 area_rng: Union[float, Sequence[float], None] = None,
                 max_dets: Union[float, Sequence[float], None] = None,
                 classwise: Optional[bool] = False,
                 proposal_nums: Sequence[int] = (100, 300, 1000),
                 labels: Optional[List] = [],
                 **kwargs):
        super(MeanAveragePrecision, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.classwise = classwise
        self.proposal_nums = list(proposal_nums)
        if iou_threshold is not None:
            iou_thrs = iou_threshold

        if iou_thrs is None:
            iou_thrs = np.linspace(
                0.5, 0.95, int(np.round((0.95 - 0.5) / 0.05)) + 1, endpoint=True
            )
        elif isinstance(iou_thrs, float):
            iou_thrs = np.array([iou_thrs])
        elif is_list_of(iou_thrs, float):
            iou_thrs = np.array(iou_thrs)
        else:
            raise TypeError(
                "`iou_thrs` should be None, float, or a list of float")

        self.iou_thrs = iou_thrs
        self.iou_threshold = iou_threshold

        self.coco_eval_bbox = DistCocoEval(
            iouThrs=iou_thrs, areaRng=area_rng, maxDets=max_dets, iouType='bbox', categories=labels)
        self.coco_eval_segm = DistCocoEval(
            iouThrs=iou_thrs, areaRng=area_rng, maxDets=max_dets, iouType='segm', categories=labels)

        self.cur_dtid = 0
        self.categories = labels
        self.segm = False

        self.add_state("bbox_instance", default=self.coco_eval_bbox)
        self.add_state("segm_instance", default=self.coco_eval_segm)

    def reset(self) -> None:
        """
        Resets the metric to it's initial state.
        """
        super().reset()
        self.coco_eval_bbox.reset()
        self.coco_eval_segm.reset()

    def update(self, predictions: Dict[str, List[Dict]], references: Dict[str, List[Dict]]) -> None:
        """
        Computes and returns the middle states, such as.
        """
        dts, gts = predictions, references
        if 'bbox' in dts:
            self.coco_eval_bbox.evaluate_batch(dts['bbox'], gts['bbox'])

        if 'mask' in dts:
            if not self.segm:
                self.segm = True
            self.coco_eval_segm.evaluate_batch(dts['mask'], gts['mask'])

    def _compute_ap_pr(self, precisions, cate_names, style):
        """
        Compute per-category AP and PR curve
        """
        try:
            from terminaltables import AsciiTable
        except Exception as err:
            raise err

        # precision: (iou, recall, cls, area range, max dets)
        assert len(cate_names) == precisions.shape[2]
        results_per_category = []
        for idx, nm in enumerate(cate_names):
            # area range index 0: all area ranges
            # max dets index -1: typically 100 per image
            precision = precisions[:, :, idx, 0, -1]
            precision = precision[precision > -1]
            if precision.size:
                ap = np.mean(precision)
            else:
                ap = float("nan")
            results_per_category.append(
                (str(nm), "{:0.3f}".format(float(ap))))

        num_columns = min(6, len(results_per_category) * 2)
        results_flatten = list(itertools.chain(*results_per_category))
        headers = ["category", "AP"] * (num_columns // 2)
        results_2d = itertools.zip_longest(
            *[results_flatten[i::num_columns] for i in range(num_columns)]
        )
        table_data = [headers]
        table_data += [result for result in results_2d]
        table = AsciiTable(table_data)
        print("Per-category of {} AP: \n{}".format(style, table.table))

    def _compute_per_cat_metrics(self, params, precisions, recalls, area_range='all', max_dets=100):
        """
        返回指定iou, area_range, max_dets的分类别评估结果
        """
        p = params

        aind = [i for i, aRng in enumerate(p.areaRngLbl) if aRng == area_range]
        mind = [i for i, mDet in enumerate(p.maxDets) if mDet == max_dets]

        if self.iou_threshold is not None:
            t = np.where(self.iou_threshold == p.iouThrs)[0]
            precisions = precisions[t]
            recalls = recalls[t]

        # precision: (iou, recall, cls, area range, max dets)
        assert len(self.categories) == precisions.shape[2]

        if len(self.categories) > 0 and not isinstance(self.categories[0], dict):
            self.categories = [{"id": idx, "name": idx} for idx in self.categories]
        cat_ids = [cate['id'] for cate in self.categories]
        cat_id2name = {cate['id']: cate["name"] for cate in self.categories}

        results_per_category = []
        for idx, catId in enumerate(cat_ids):
            # area range index 0: all area ranges
            # max dets index -1: typically 100 per image
            cate_name = cat_id2name[catId]

            precision = precisions[:, :, idx, aind, mind]
            precision = precision[precision > -1]
            if precision.size > 0:
                ap = np.mean(precision)
            else:
                ap = -1

            recall = recalls[:, idx, aind, mind]
            recall = recall[recall > -1]
            if recall.size > 0:
                ar = np.mean(recall)
            else:
                ar = -1

            results_per_category.append(dict(labelName=cate_name, averagePrecision=round(ap, self.decimals),
                                             averageRecall=round(ar, self.decimals)))

        return results_per_category

    def _compute_pr_curve(self, params, precisions):
        """
        Compute the PR curve.
        """
        if self.iou_threshold is None:
            self.iou_threshold = 0.5

        p = params
        iou_index = np.where(self.iou_threshold == p.iouThrs)[0]
        cat_ids = [cate['id'] for cate in self.categories]
        cat_id2name = {cate['id']: cate["name"] for cate in self.categories}
        metric = []

        for idx, catId in enumerate(cat_ids):
            # area range index 0: all area ranges
            # max dets index -1: typically 100 per image
            name = cat_id2name[catId]
            precision_iou = precisions[iou_index, :, idx, 0, -1]
            if precision_iou.size:
                ap = np.mean(precision_iou)

            else:
                ap = -1.0  # float('nan')

            metric.append([name,
                           round(float(ap), 4),
                           np.reshape(precision_iou, -1).tolist(),
                           [round(i * 0.01, 2) for i in range(101)],
                           self.iou_threshold])

        return metric

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        _results = {}
        _results['bbox'] = self.coco_eval_bbox.eval_imgs_all
        _results['segm'] = self.coco_eval_segm.eval_imgs_all

        eval_results = {'bbox': [],
                        'segm': [],
                        'bbox_results_per_label': [],
                        'segm_results_per_label': [],
                        'pr_curve': []}

        if 'bbox' in _results:
            self.coco_eval_bbox.eval_imgs_all = _results['bbox']
            self.coco_eval_bbox.accumulate_rank()
            self.coco_eval_bbox.summarize()

        if self.segm:
            self.coco_eval_segm.eval_imgs_all = _results['segm']
            self.coco_eval_segm.accumulate_rank()
            self.coco_eval_segm.summarize()

        if self.classwise:
            if len(self.categories) > 0 and isinstance(self.categories[0], dict):
                cate_names = [cate['name'] for cate in self.categories]
            else:
                cate_names = self.categories
            if 'bbox' in _results:
                self._compute_ap_pr(
                    self.coco_eval_bbox.eval['precision'], cate_names, 'bbox')
                results_per_category = self._compute_per_cat_metrics(self.coco_eval_bbox.params,
                                                                     self.coco_eval_bbox.eval["precision"],
                                                                     self.coco_eval_bbox.eval["recall"])
                eval_results['bbox_results_per_label'] = results_per_category
                eval_results['pr_curve'] = self._compute_pr_curve(self.coco_eval_bbox.params,
                                                                  self.coco_eval_bbox.eval["precision"])

            if self.segm:
                self._compute_ap_pr(
                    self.coco_eval_segm.eval['precision'], cate_names, 'segm')
                results_per_category = self._compute_per_cat_metrics(self.coco_eval_segm.params,
                                                                     self.coco_eval_segm.eval["precision"],
                                                                     self.coco_eval_segm.eval["recall"])
                eval_results['segm_results_per_label'] = results_per_category
                eval_results['mask_pr_curve'] = self._compute_pr_curve(self.coco_eval_segm.params,
                                                                  self.coco_eval_segm.eval["precision"])

        sys.stdout.flush()

        if 'bbox' in _results:
            stats = self.coco_eval_bbox.stats.tolist()
            eval_results['bbox'] = list_round(stats, decimals=self.decimals)
        if self.segm:
            stats = self.coco_eval_segm.stats.tolist()
            eval_results['segm'] = list_round(stats, decimals=self.decimals)

        return eval_results
