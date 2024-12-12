#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/17
# @Author  : yanxiaodong
# @File    : imagenet_dataset.py
"""
import os
from typing import List, Any

import bcelogger
from windmillclient.client.windmill_client import WindmillClient

from .dataset import Dataset
from gaea_operator.utils import get_filepaths_in_archive


class ImageNetDataset(Dataset):
    """
    ImageNet Dataset
    """
    usages = [("train.txt", "annotation.txt"), ("val.txt", "annotation.txt")]

    def __init__(self, windmill_client: WindmillClient, work_dir: str, extra_work_dir: str = None):
        super().__init__(windmill_client=windmill_client, work_dir=work_dir, extra_work_dir=extra_work_dir)

        self.image_prefix_path = ""
        self.label_list = []

    def reset(self):
        """
        Reset attribute variable.
        """
        self.label_list = []

    def _get_annotation(self, paths: List, base_uri: str, usage: str, work_dir: str):
        annotation_file_list = []
        for path in paths:
            path = os.path.join(work_dir, path)
            annotation_file_list = get_filepaths_in_archive(path, self.decompress_output_uri, usage)

        bcelogger.info(f"Annotation file list is: {annotation_file_list}")

        raw_data_list = []
        for file in annotation_file_list:
            text_data = open(file, "r").read()
            raw_data = text_data.strip("\n").split("\n")

            bcelogger.info(f"Parse annotation file {file}, image num is {len(raw_data)}")

            if os.path.exists(os.path.join(os.path.dirname(file), "labels.txt")):
                for idx in range(len(raw_data)):
                    img_file, label = raw_data[idx].strip("\"").rsplit(" ", 1)
                    img_file = self._file_name_cvt_abs(img_file, file, base_uri, 1, work_dir)
                    raw_data[idx] = img_file + " " + label

                raw_data_list.append(raw_data)
                
                bcelogger.info(f"Find the labels.txt file in {os.path.dirname(file)}")
                label_data = open(os.path.join(os.path.dirname(file), "labels.txt"), "r").read().strip("\n").split("\n")
            else:
                raise FileNotFoundError(f"Can't find the labels.txt in {os.path.dirname(file)}")

            self.label_list.append(label_data)

        return raw_data_list

    def _concat_annotation(self, raw_data_list: List):
        raw_data_imagenet = None
        if len(raw_data_list) >= 1:
            raw_data_imagenet = self._imagenet_data_raw_concat(raw_data_list, self.label_list)
        else:
            raise ValueError(f"The number of annotation file is empty, please check dataset name")

        return raw_data_imagenet

    def _filter_not_exist_image(self, raw_data: Any):
        bcelogger.info(f"The image num is {len(raw_data)}")
        new_raw_data = []

        not_exist_num = 0
        for item in raw_data:
            img_file, label = item.strip("\"").rsplit(" ", 1)
            if os.path.exists(img_file):
                new_raw_data.append(img_file + " " + str(label))
            else:
                not_exist_num += 1

        assert len(new_raw_data) > 0, "All images are not exist"
        bcelogger.info(f"The image num is {len(raw_data)}, not exist num is {not_exist_num}")

        return new_raw_data

    def _imagenet_data_raw_concat(self, raw_data: List[List], label_list: List[List]):
        label_name2id = self._category_valid(label_list)

        raw_data_imagenet = []

        for idx, data in enumerate(raw_data):
            old2new_cat_id = {}
            for inner_idx, label in enumerate(label_list[idx]):
                label_name, label_id = label.strip().split(" ")[0], label.strip().split(" ")[1]
                if label_id != label_name2id[label_name]:
                    old2new_cat_id[label_id] = label_name2id[label_name]
            for item in data:
                img_file, label_id = item.strip("\"").rsplit(" ", 1)
                label_id = int(label_id)
                if label_id in old2new_cat_id:
                    label_id = old2new_cat_id[label_id]
                raw_data_imagenet.append(img_file + " " + str(label_id))

        return raw_data_imagenet

    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        if raw_data is None:
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as fp:
            for item in raw_data:
                fp.write(item + "\n")

    def _category_valid(self, label_list: List[List]):
        lengths = [len(label) for label in label_list]

        if len(set(lengths)) == 1:
            for idx in range(1, len(lengths)):
                for inner_idx, label in enumerate(label_list[idx]):
                    if label != label_list[0][inner_idx]:
                        raise ValueError(f"The labels name is not equal, please check {label_list}")
            self.labels = [{"id": int(name.split(" ")[1]),
                            "name": name.split(" ")[0],
                            "displayName": name.split(" ")[0]} for name in label_list[0]]
            bcelogger.info(f"The labels is {self.labels}")
            return {name.split(" ")[0]: name.split(" ")[1] for name in label_list[0]}
        else:
            raise ValueError(f"The number of labels is not equal, please check {label_list}")