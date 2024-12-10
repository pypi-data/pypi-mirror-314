#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/17
# @Author  : yanxiaodong
# @File    : imagenet_dataset.py
"""
import os
import yaml
from typing import List, Any, Dict

import bcelogger
from windmillclient.client.windmill_client import WindmillClient

from .dataset import Dataset
from gaea_operator.utils import get_filepaths_in_archive


class MultiAttributeDataset(Dataset):
    """
    ImageNet Dataset
    """
    usages = [("train.txt", "annotation.txt"), ("val.txt", "annotation.txt")]

    def __init__(self, windmill_client: WindmillClient, work_dir: str, extra_work_dir: str = None):
        super().__init__(windmill_client=windmill_client, work_dir=work_dir, extra_work_dir=extra_work_dir)

        self.image_prefix_path = "images"
        self.label_list = []
        self.data_yamls = ["label_description.yaml", "config_for_sdk_encapsulation.yaml"]

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

            for idx in range(len(raw_data)):
                img_file, label = raw_data[idx].strip("\"").split(" ", 1)
                img_file = self._file_name_cvt_abs(img_file, file, base_uri, 2, work_dir)
                raw_data[idx] = img_file + " " + label

            if os.path.exists(os.path.join(os.path.dirname(file), "label_description.yaml")):
                bcelogger.info(f"Find the label_description.yaml file in {os.path.dirname(file)}")
                with open(os.path.join(os.path.dirname(file), "label_description.yaml"), "r") as f:
                    label_data = yaml.load(f, Loader=yaml.FullLoader)
                    self.label_list.append(label_data)
            else:
                raise FileNotFoundError(f"Can't find the label_description.yaml in {os.path.dirname(file)}")

            raw_data_list.append(raw_data)
        return raw_data_list

    def _concat_annotation(self, raw_data_list: List):
        raw_data_imagenet = None
        if len(raw_data_list) >= 1:
            self._label_valid(self.label_list)
            raw_data_imagenet = self._multi_attribute_data_raw_concat(raw_data_list)
        else:
            raise ValueError(f"The number of annotation file is empty, please check dataset name")

        return raw_data_imagenet

    def _multi_attribute_data_raw_concat(self, raw_data: List[List]):
        raw_data_imagenet = []
        for data in raw_data:
            for item in data:
                raw_data_imagenet.append(item)
        return raw_data_imagenet

    def _filter_not_exist_image(self, raw_data: Any):
        bcelogger.info(f"The image num is {len(raw_data)}")
        new_raw_data = []

        not_exist_num = 0
        for item in raw_data:
            img_file, label = item.strip("\"").split(" ", 1)
            if os.path.exists(img_file):
                new_raw_data.append(img_file + " " + str(label))
            else:
                not_exist_num += 1

        assert len(new_raw_data) > 0, "All images are not exist"
        bcelogger.info(f"The image num is {len(raw_data)}, not exist num is {not_exist_num}")

        return new_raw_data

    def _label_valid(self, label_list: List[Dict]):
        assert len(label_list) > 0, "The label list is empty"

        info_list = []
        for label in label_list:
            info_task = []
            for task_index, task_label in enumerate(label.get('tasks', [])):
                anno_key = task_label['anno_key']
                # 任务名
                task_name = task_label.get('task_name', 'unknown_{}'.format(task_index))
                info_task.append([task_name, anno_key])
            info_list.append(info_task)
        # check label task name and anno key
        for index, info in enumerate(info_list):
            for task_index, task in enumerate(info):
                if info_list[0][task_index][0] != task[0]:
                    raise ValueError(f"The multi data set label task name is not equal, please check {info_list}")
                if info_list[0][task_index][1] != task[1]:
                    raise ValueError(f"The multi data set label task anno key is not equal, please check {info_list}")
        # 解析 labels      
        self.labels = self._get_label_data(label_list[0])
        return True

    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        if raw_data is None:
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as fp:
            for item in raw_data:
                fp.write(item + "\n")

    def _get_label_data(self, config_for_sdk: dict):
        """从 config_for_sdk 解析 label 数据"""

        label_data = []
        # 转化为 labels.json 的格式 
        for task_index, task_label in enumerate(config_for_sdk.get('tasks', [])):

            # 类型检测
            task_type = task_label.get('task_type', 'unknown')
            assert task_type in ['image_classification'], f"task_type {task_type} is not supported now in imagenet."

            # 该任务的标签位于标签文件的第几列
            anno_key = task_label['anno_key']

            # 保存任务名
            task_name = task_label.get('task_name', 'unknown_{}'.format(task_index))
            label_data.append({'id': anno_key - 1, 'name': task_name})

            # 保存该任务的所有类别名
            task_categories = task_label.get('categories', [])
            for label_id, label_name in task_categories.items():
                label_data.append({'id': int(label_id), 'name': label_name, 'parentID': anno_key - 1})

        return label_data
