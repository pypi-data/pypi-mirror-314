#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/19
# @Author  : liyinggang
# @File    : convnext_config.py
"""
import os
import json
from typing import Dict

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize
from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, read_yaml_file, write_yaml_file
from ..config import Config
from ..modify_package_files import ModifyPackageFiles
from .template.modify_train_parameter import generate_train_config, KEY_EVAL_WIDTH, KEY_EVAL_HEIGHT, \
    set_multi_key_value


class ConvNextConfig(Config):
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
        new_advanced_parameters['nb_classes'] = str(num_classes)

        # 2. set dataset
        # train.txt 和 val.txt 是在源码中写定的 不是在配置文件中
        new_advanced_parameters['data_path'] = dataset_uri
        new_advanced_parameters['eval_data_path'] = dataset_uri

        # 2. set pretrain model
        new_advanced_parameters['pretrained'] = pretrain_model_uri

        # output
        new_advanced_parameters['output_dir'] = model_uri

        # 2. generate train config file
        if not os.path.exists(model_uri):
            os.makedirs(model_uri, exist_ok=True)
        self._update_train_metadata(advanced_parameters=new_advanced_parameters)

        generate_train_config(new_advanced_parameters,
                              self.metadata,
                              os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME))

    def write_eval_config(self, dataset_uri: str, model_uri: str, ):
        """
        Config write for eval of ppyoloe_plus_m model.
        """
        parameters = {}
        parameters['eval_data_path'] = dataset_uri
        config_data = read_yaml_file(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)
        for key, val in parameters.items():
            set_multi_key_value(config_data, key, val)

        write_yaml_file(config_data, model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)

    def _update_train_metadata(self, advanced_parameters: Dict):
        super()._update_train_metadata(advanced_parameters=advanced_parameters)

        input_size = InputSize(width=int(advanced_parameters[KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[KEY_EVAL_HEIGHT]))
        model_meta_data = ModelMetadata(labels=self.labels,
                                        algorithmParameters={'evalWidth': int(advanced_parameters[KEY_EVAL_WIDTH]),
                                                             'evalHeight': int(advanced_parameters[KEY_EVAL_HEIGHT])},
                                        inputSize=input_size)
        self._metadata.update(model_meta_data.dict())