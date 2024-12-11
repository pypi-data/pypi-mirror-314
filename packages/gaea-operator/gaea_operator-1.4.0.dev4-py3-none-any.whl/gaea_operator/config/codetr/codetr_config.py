#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/04/
# @Author  : liyinggang
# @File    : codetr config
"""
import os
import json
from typing import Dict

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, DEFAULT_DEPLOY_CONFIG_FILE_NAME, write_yaml_file
from ..config import Config
from .template.modify_parameter import generate_train_config, generate_deploy_config, \
    modify_var_value, modify_eval_config, \
    VAR_KEY_EVAL_HEIGHT, \
    VAR_KEY_EVAL_WIDTH, \
    VAR_KEY_NUM_CLASSES, KEY_CLASS_NAMES, VAR_KEY_DATA_ROOT, VAR_KEY_VAL_ANNO, \
    IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD


class CoDETRConfig(Config):
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

        new_advanced_parameters[VAR_KEY_NUM_CLASSES] = str(num_classes)
        #  set dataset
        new_advanced_parameters[VAR_KEY_DATA_ROOT] = dataset_uri
        # set class names
        class_names = [label['name'] for label in self.labels]
        new_advanced_parameters[KEY_CLASS_NAMES] = class_names

        # 2. generate train config file
        if not os.path.exists(model_uri):
            os.makedirs(model_uri, exist_ok=True)

        generate_train_config(new_advanced_parameters,
                              pretrain_model_uri,
                              os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME))

        self._update_train_metadata(advanced_parameters=new_advanced_parameters)

    def write_deploy_config(self, advanced_parameters: dict, model_uri: str):
        """
        Config write for export of ppyoloe_plus_m model.
        """
        generate_deploy_config(advanced_parameters, os.path.join(model_uri, DEFAULT_DEPLOY_CONFIG_FILE_NAME))

    def write_eval_config(self, dataset_uri: str, model_uri: str):
        """
        Config write for eval of ppyoloe_plus_m model.
        """
        var_name_vals = [[VAR_KEY_DATA_ROOT, dataset_uri],
                         [VAR_KEY_VAL_ANNO, os.path.join(dataset_uri, 'val.json')]]
        input_yaml_name = os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)
        config_data = modify_var_value(input_yaml_name, var_name_vals)
        # yaml文件被dump之后不再保持锚点
        modify_eval_config(config_data, var_name_vals)
        write_yaml_file(config_data, model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)

    def _update_train_metadata(self, advanced_parameters: Dict):
        super()._update_train_metadata(advanced_parameters=advanced_parameters)
        model_meta = ModelMetadata(**self._metadata)

        input_size = InputSize(width=int(advanced_parameters[VAR_KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[VAR_KEY_EVAL_HEIGHT]))
        model_meta.inputSize = input_size
        model_meta.labels = self.labels

        model_meta.algorithmParameters.update({"mean": str(IMAGENET_DEFAULT_MEAN),
                                               "std": str(IMAGENET_DEFAULT_STD)})

        self._metadata = model_meta.dict()
