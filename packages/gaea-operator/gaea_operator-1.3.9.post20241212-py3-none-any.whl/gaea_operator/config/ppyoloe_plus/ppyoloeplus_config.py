#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/1
# @Author  : yanxiaodong
# @File    : ppyoloeplus_config.py
"""
import os
import json
from typing import Dict

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, read_yaml_file, write_yaml_file
from ..config import Config
from .template.modify_train_parameter import generate_train_config, \
    set_multi_key_value, \
    KEY_EVAL_HEIGHT, \
    KEY_EVAL_WIDTH, \
    KEY_EVAL_SIZE, \
    KEY_EVAL_BATCH_SIZE, \
    KEY_TRAIN_BATCH_SIZE


class PPYOLOEPLUSMConfig(Config):
    """
    Config write for train, transform and package.
    """

    def __init__(self, windmill_client: WindmillClient, tracker_client: ExperimentTracker, metadata: Dict = {}):
        super().__init__(windmill_client=windmill_client, tracker_client=tracker_client, metadata=metadata)
        self.labels = []

    def write_train_config(self,
                           dataset_uri: str,
                           model_uri: str,
                           advanced_parameters: dict,
                           pretrain_model_uri: str):
        """
        Config write for train of ppyoloe_plus_m model.
        """
        # 1. get model number
        tran_json_name = os.path.join(dataset_uri, 'labels.json')
        self.labels = json.load(open(tran_json_name, "r"))
        num_classes = len(self.labels)
        new_advanced_parameters = advanced_parameters.copy()
        new_advanced_parameters['num_classes'] = str(num_classes)

        # 2. set dataset
        new_advanced_parameters['TrainDataset.dataset_dir'] = dataset_uri
        new_advanced_parameters['EvalDataset.dataset_dir'] = dataset_uri

        # 3. set batch size
        if KEY_TRAIN_BATCH_SIZE in new_advanced_parameters:
            new_advanced_parameters[KEY_EVAL_BATCH_SIZE] = advanced_parameters[KEY_TRAIN_BATCH_SIZE]

        # 4. generate train config file
        if not os.path.exists(model_uri):
            os.makedirs(model_uri, exist_ok=True)
        self._update_train_metadata(advanced_parameters=new_advanced_parameters)

        generate_train_config(new_advanced_parameters,
                              pretrain_model_uri,
                              os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME))

    def write_eval_config(self, dataset_uri: str, model_uri: str, ):
        """
        Config write for eval of ppyoloe_plus_m model.
        """
        parameters = {}
        parameters['TrainDataset.dataset_dir'] = dataset_uri
        parameters['EvalDataset.dataset_dir'] = dataset_uri

        config_data = read_yaml_file(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)
        for key, val in parameters.items():
            set_multi_key_value(config_data, key, val)

        write_yaml_file(config_data, model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)

    def _update_train_metadata(self, advanced_parameters: Dict):
        """
            更新训练元数据。

        Args:
            advanced_parameters (Dict): 高级参数字典，包含以下键值对：
                - KEY_EVAL_SIZE (str): 评估图像大小，格式为"<宽度>*<高度>"，例如"256*256"；
                - 'model_type' (str): 模型类型，例如"resnet"。

        Returns:
            None.

        Raises:
            None.
        """
        super()._update_train_metadata(advanced_parameters=advanced_parameters)
        model_meta = ModelMetadata(**self._metadata)

        input_size = InputSize(width=int(advanced_parameters[KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[KEY_EVAL_HEIGHT]))
        model_meta.inputSize = input_size
        model_meta.labels = self.labels

        self._metadata = model_meta.dict()
