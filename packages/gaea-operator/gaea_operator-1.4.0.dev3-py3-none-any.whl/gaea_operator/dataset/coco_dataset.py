#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/29
# @Author  : yanxiaodong
# @File    : coco_dataset.py
"""
import json
import os
from typing import Any, Dict, List, Union, Tuple
import copy
import math

import bcelogger
import numpy as np
from windmillclient.client.windmill_client import WindmillClient

from .dataset import Dataset
from gaea_operator.utils import get_filepaths_in_archive


class CocoDataset(Dataset):
    """
    A Coco dataset for data processing.
    """
    usages = [("train.json", "annotation.json"), ("val.json", "annotation.json")]

    def __init__(self, windmill_client: WindmillClient, work_dir: str, extra_work_dir: str = None):
        super().__init__(windmill_client=windmill_client, work_dir=work_dir, extra_work_dir=extra_work_dir)
        self.image_prefix_path = "images"

    @classmethod
    def coco_annotation_from_vistudio_v1(cls, annotations: List[Dict]):
        """
        Convert the annotation from Vistudio v1 to Coco format.
        """
        anno_id = 1
        new_annotations = []
        for item in annotations:
            im_id = item["image_id"]
            if item.get("annotations") is None:
                anno = {"id": anno_id, "image_id": im_id}
                anno_id += 1
                new_annotations.append(anno)
                continue

            for anno in item["annotations"]:
                if "bbox" not in anno or len(anno["bbox"]) == 0 or sum(anno["bbox"]) == 0:
                    continue

                anno["image_id"] = im_id
                anno['ignore'] = anno['ignore'] if 'ignore' in anno else 0
                anno['iscrowd'] = "iscrowd" in anno and anno["iscrowd"]
                for idx in range(len(anno["labels"])):
                    new_anno = copy.deepcopy(anno)
                    new_anno["id"] = anno_id

                    label = new_anno["labels"][idx]

                    if label.get("parent_id") == "" or label.get("parent_id") is None:
                        label.pop("parent_id", None)

                    if isinstance(label["id"], str):
                        label["id"] = int(label["id"])
                    if label["id"] is None or math.isnan(label["id"]):
                        continue
                    new_anno['category_id'] = int(label["id"])
                    new_anno['score'] = label.get("confidence", 1)
                    new_anno['confidence'] = label.get("confidence", 1)
                    new_annotations.append(new_anno)
                    anno_id += 1

        return new_annotations
    
    @classmethod
    def coco_seg_annotation_from_vistudio_v1(cls, annotations: List[Dict]):
        """
        Convert the annotation from Vistudio v1 to Coco format.
        """
        anno_id = 1
        new_annotations = []
        for item in annotations:
            im_id = item["image_id"]
            if item.get("annotations") is None:
                anno = {"id": anno_id, "image_id": im_id}
                anno_id += 1
                new_annotations.append(anno)
                continue
            for anno in item["annotations"]:
                if 'segmentation' not in anno or len(anno['segmentation']) == 0:
                    anno = {"id": anno_id, "image_id": im_id}
                    anno_id += 1
                    new_annotations.append(anno)
                    continue

                anno["image_id"] = im_id
                anno['ignore'] = anno['ignore'] if 'ignore' in anno else 0
                anno['iscrowd'] = "iscrowd" in anno and anno["iscrowd"]
                for idx in range(len(anno["labels"])):
                    new_anno = copy.deepcopy(anno)
                    new_anno["id"] = anno_id
                    if isinstance(new_anno["labels"][idx]["id"], str):
                        new_anno["labels"][idx]["id"] = int(new_anno["labels"][idx]["id"])
                    if new_anno["labels"][idx]["id"] is None or math.isnan(new_anno["labels"][idx]["id"]):
                        continue
                    new_anno['category_id'] = int(new_anno["labels"][idx]["id"])
                    new_anno['score'] = new_anno["labels"][idx].get("confidence", 1)
                    new_anno['confidence'] = new_anno["labels"][idx].get("confidence", 1)
                    new_annotations.append(new_anno)
                    anno_id += 1

        return new_annotations

    def _get_annotation(self, paths: List, base_uri: str, usage: Union[str, Tuple], work_dir: str) -> List:
        annotation_file_list = []
        for idx, path in enumerate(paths):
            path = os.path.join(work_dir, path)
            annotation_file_list = get_filepaths_in_archive(path, self.decompress_output_uri, usage)

        bcelogger.info(f"Annotation file list is: {annotation_file_list}")

        raw_data_list = []
        for file in annotation_file_list:
            json_data = json.load(open(file, "r"))
            images = json_data["images"]

            bcelogger.info(f"Parse annotation file {file}, image num is {len(images)}")
            
            for img in images:
                img["file_name"] = self._file_name_cvt_abs(img["file_name"], file, base_uri, 2, work_dir)
                self.image_set.add(img["file_name"])

            raw_data_list.append(json_data)

        return raw_data_list

    def _concat_annotation(self, raw_data_list: List):
        if len(raw_data_list) >= 1:
            raw_data_coco = self._coco_data_raw_concat(raw_data_list)
        else:
            raise ValueError(f"The number of annotation file is empty, please check dataset name")

        return raw_data_coco

    def _filter_not_exist_image(self, raw_data: Any):
        return raw_data

    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        if raw_data is None:
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as fp:
            json.dump(raw_data, fp, separators=(",", ":"))

    def _coco_data_raw_concat(self, raw_data: List[Dict]):
        cat_name2id = self._category_valid(raw_data)

        raw_data_coco = {"images": [], "annotations": [], "categories": []}
        max_ann_id = -1
        new_im_id = 1

        categories = []
        for cat in raw_data[0]["categories"]:
            cat["id"] = int(cat["id"])
            categories.append(cat)
        raw_data_coco["categories"] = categories

        for data in raw_data:
            old2new_im_id = {}
            old2new_cat_id = {}
            for img in data["images"]:
                old2new_im_id[img["id"]] = new_im_id
                img["id"] = new_im_id
                raw_data_coco["images"].append(img)
                new_im_id += 1

            for cat in data["categories"]:
                if cat_name2id[cat["name"]] != int(cat["id"]):
                    old2new_cat_id[cat["id"]] = cat_name2id[cat["name"]]
                    cat["id"] = cat_name2id[cat["name"]]

            for ann in data["annotations"]:
                max_ann_id = self._get_max_id(int(ann["id"]), max_ann_id)
                if ann["image_id"] in old2new_im_id:
                    ann["image_id"] = old2new_im_id[ann["image_id"]]
                else:
                    ann["image_id"] = int(ann["image_id"])
                if ann["category_id"] in old2new_cat_id:
                    ann["category_id"] = old2new_cat_id[ann["category_id"]]
                else:
                    ann["category_id"] = int(ann["category_id"])
                ann["id"] = max_ann_id
                max_ann_id += 1
                raw_data_coco["annotations"].append(ann)

        return raw_data_coco

    def _get_max_id(self, im_id: int, max_im_id: int):
        if im_id > max_im_id:
            max_im_id = im_id

        return max_im_id

    def _category_valid(self, raw_data: List[Dict]):
        categories_list = [data["categories"] for data in raw_data]
        lengths = [len(categories) for categories in categories_list]

        if len(set(lengths)) == 1:
            cat_name2id = {cat["name"]: int(cat["id"]) for cat in categories_list[0]}
            for idx in range(1, len(lengths)):
                for cat in categories_list[idx]:
                    if cat["name"] not in cat_name2id:
                        raise ValueError(f"The categories name is not equal, please check {categories_list}")
            self.labels = [{"id": int(cat["id"]), "name": cat["name"], "displayName": cat["name"]}
                           for cat in categories_list[0]]
            bcelogger.info(f"The labels is {self.labels}")
            return cat_name2id
        else:
            raise ValueError(f"The number of categories is not equal, please check {categories_list}")