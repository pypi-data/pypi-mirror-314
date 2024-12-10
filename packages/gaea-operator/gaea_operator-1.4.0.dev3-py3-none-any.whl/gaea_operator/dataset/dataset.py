#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/21
# @Author  : yanxiaodong
# @File    : dataset_concat.py
"""
import json
import os
from abc import ABCMeta, abstractmethod
from typing import Any, List, Union, Tuple, Dict
import pycocotools.mask as mask_utils
import math
import numpy as np

import bcelogger
from windmillclient.client.windmill_client import WindmillClient

from gaea_operator.utils import find_upper_level_folder, write_file


class Dataset(metaclass=ABCMeta):
    """
    A dataset for data processing.
    """
    decompress_output_uri = "/root/dataset"
    usages = ["", ""]

    def __init__(self, windmill_client: WindmillClient, work_dir: str, extra_work_dir: str = None):
        self.windmill_client = windmill_client
        self.work_dir = work_dir
        self.extra_work_dir = extra_work_dir
        self.labels = []
        self.image_set = set()
        self.image_prefix_path = ""
        self.label_file_path = "labels.json"
        assert len(self.usages) == 2, "Dataset mode keys length must equal 2"

    def reset(self):
        """
        Reset attribute variable.
        """
        pass

    def concat_dataset(self,
                       dataset_name: str,
                       output_dir: str,
                       usage: Union[str, Tuple],
                       base_dataset_name: str = None,
                       save_label: bool = False):
        """
        Concat dataset from artifact.
        """
        self.reset()
        # 处理base dataset name
        base_raw_data_list = []
        if base_dataset_name is not None and len(base_dataset_name) > 0:
            bcelogger.info(f"Concat base dataset from dataset name {base_dataset_name}")
            response = self.windmill_client.get_artifact(name=base_dataset_name)
            filesystem = self.windmill_client.suggest_first_filesystem(workspace_id=response.workspaceID,
                                                                       guest_name=response.parentName)
            bcelogger.info(f"Filesystem is {filesystem}")
            paths = []
            base_uri = ""
            for _path in response.metadata["paths"]:
                relative_path = self.windmill_client.get_path(filesystem, _path)
                bcelogger.info(f"Path is {_path}, relative path is {relative_path}")
                base_uri = _path[:_path.index(relative_path)].rstrip('/')
                paths.append(relative_path)

            bcelogger.info(f"Concat base dataset from path {paths} and base uri {base_uri}")
            base_raw_data_list = self._get_annotation(paths=paths,
                                                      base_uri=base_uri,
                                                      usage=usage,
                                                      work_dir=self.extra_work_dir)

        bcelogger.info(f"Concat dataset from dataset name {dataset_name}")
        response = self.windmill_client.get_artifact(name=dataset_name)
        write_file(json.loads(response.raw_data), output_dir=output_dir)
        filesystem = self.windmill_client.suggest_first_filesystem(workspace_id=response.workspaceID,
                                                                   guest_name=response.parentName)

        paths = []
        base_uri = ""
        for _path in response.metadata["paths"]:
            relative_path = self.windmill_client.get_path(filesystem, _path)
            base_uri = _path[:_path.index(relative_path)].rstrip('/')
            paths.append(relative_path)

        bcelogger.info(f"Concat dataset from path {paths} and base uri {base_uri}")

        raw_data_list = self._get_annotation(paths=paths, base_uri=base_uri, usage=usage, work_dir=self.work_dir)

        raw_data_list += base_raw_data_list
        raw_data = self._concat_annotation(raw_data_list=raw_data_list)

        self._warmup_image_meta()

        raw_data = self._filter_not_exist_image(raw_data=raw_data)

        self._write_annotation(output_dir=output_dir,
                               file_name=usage if isinstance(usage, str) else usage[0],
                               raw_data=raw_data)

        if usage == self.usages[0] or save_label:
            self._write_category(output_dir=output_dir)

    @classmethod
    def mask_from_vistudio_v1(cls, annotations: List[Dict], images: List[Dict], labels: List[Dict]):
        """
        Convert annotations from Vistudio to Mask.
        """
        label_id2index = {int(label["id"]): idx for idx, label in enumerate(labels)}
        image_dict = {item["image_id"]: item for item in images}
        new_annotations = []
        for item in annotations:
            im_id = item["image_id"]
            img = image_dict[im_id]
            width = img["width"]
            height = img["height"]

            label_raw = np.zeros((height, width), dtype=np.uint8)
            new_anno = {"mask": label_raw, "image_id": im_id, "width": width, "height": height}
            if item.get("annotations") is None:
                new_annotations.append(new_anno)
                continue
            for anno in item["annotations"]:
                for idx in range(len(anno["labels"])):
                    if isinstance(anno["labels"][idx]["id"], str):
                        anno["labels"][idx]["id"] = int(anno["labels"][idx]["id"])
                    if anno["labels"][idx]["id"] is None or math.isnan(anno["labels"][idx]["id"]):
                        continue
                    # 如果标注标签id不在label,则跳过（修改了标签但是标注没有同步修改）
                    if anno["labels"][idx]["id"] not in label_id2index:
                        continue
                    if "rle" in anno and len(anno["rle"]) > 0:
                        if isinstance(anno["rle"]["counts"], list):
                            rle = mask_utils.frPyObjects(anno["rle"], height, width)
                            mask = mask_utils.decode(rle)
                        else:
                            mask = mask_utils.decode(anno["rle"])
                    else:
                        polygon = anno["segmentation"]
                        if len(polygon) > 0 and not isinstance(polygon[0], list):
                            polygon = [polygon]
                        if len(polygon[0]) < 6:
                            continue
                        rle = mask_utils.frPyObjects(polygon, height, width)
                        mask = mask_utils.decode(mask_utils.merge(rle))
                    index = mask == 1
                    label_raw[index] = label_id2index[anno["labels"][idx]["id"]]

            new_annotations.append(new_anno)

        return new_annotations

    @abstractmethod
    def _get_annotation(self, paths: List, base_uri: List, usage: str, work_dir: str) -> List:
        pass

    @abstractmethod
    def _concat_annotation(self, raw_data_list: List):
        pass

    @abstractmethod
    def _write_annotation(self, output_dir: str, file_name: str, raw_data: Any):
        pass

    @abstractmethod
    def _filter_not_exist_image(self, raw_data: Any):
        pass

    def _write_category(self, output_dir: str):
        if self.labels is None:
            bcelogger.warning("No labels found, skip write category file.")
            return
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, self.label_file_path)
        with open(file_path, "w") as fp:
            json.dump(self.labels, fp)

    def _file_name_cvt_abs(self, image_file: str, path: str, fs_prefix: str, level: int, work_dir: str):
        if image_file.startswith(fs_prefix):
            file = image_file.replace(fs_prefix, work_dir)
            return file
        if os.path.isabs(image_file):
            return image_file
        else:
            return os.path.join(find_upper_level_folder(path, level), self.image_prefix_path, image_file)

    def _warmup_image_meta(self):
        dirs = [os.path.dirname(filepath) for filepath in self.image_set]
        dirs = set(dirs)
        for dir in dirs:
            os.listdir(dir)
