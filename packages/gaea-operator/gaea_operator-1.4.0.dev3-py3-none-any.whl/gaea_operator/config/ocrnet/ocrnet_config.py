#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/19
# @Author  : wanggaofei
# @File    : ocrnet.py
"""
import os
import json
from typing import Dict
from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize
from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, read_yaml_file, \
    write_yaml_file, DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME, DEFAULT_TRANSFORM_CONFIG_FILE_NAME, \
    DEFAULT_META_FILE_NAME
from .. import Config, generate_transform_config
from ..modify_package_files import ModifyPackageFiles
from .template.modify_train_parameter import generate_train_config, set_multi_key_value, \
    KEY_EVAL_WIDTH, KEY_EVAL_HEIGHT


class OCRNetConfig(Config):
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
        Config write for train of ocrnet model.
        """
        # 1. get model number
        tran_json_name = os.path.join(dataset_uri, 'labels.json')
        self.labels = json.load(open(tran_json_name, "r"))
        num_classes = len(self.labels)
        new_advanced_parameters = advanced_parameters.copy()
        new_advanced_parameters['model.num_classes'] = str(num_classes + 1)
        new_advanced_parameters['train_dataset.num_classes'] = str(num_classes + 1)
        new_advanced_parameters['val_dataset.num_classes'] = str(num_classes + 1)

        # 2. set dataset
        new_advanced_parameters['train_dataset.dataset_root'] = dataset_uri
        new_advanced_parameters['train_dataset.train_path'] = os.path.join(dataset_uri, 'train.txt')
        new_advanced_parameters['val_dataset.dataset_root'] = dataset_uri
        new_advanced_parameters['val_dataset.val_path'] = os.path.join(dataset_uri, 'val.txt')

        # 2. set pretrain model
        new_advanced_parameters['model.backbone.pretrained'] = pretrain_model_uri

        # 2. generate train config file
        if not os.path.exists(model_uri):
            os.makedirs(model_uri, exist_ok=True)

        generate_train_config(new_advanced_parameters, os.path.join(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME))

        self._update_train_metadata(advanced_parameters=new_advanced_parameters)

    def write_eval_config(self, dataset_uri: str, model_uri: str, ):
        """
        Config write for eval of ocrnet model.
        """
        parameters = {}
        parameters['train_dataset.dataset_root'] = dataset_uri
        parameters['train_dataset.train_path'] = os.path.join(dataset_uri, 'val.txt')  # use validation dataset
        parameters['val_dataset.dataset_root'] = dataset_uri
        parameters['val_dataset.val_path'] = os.path.join(dataset_uri, 'val.txt')

        # 2. set pretrain model
        parameters['model.backbone.pretrained'] = os.path.join(model_uri, DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME)

        config_data = read_yaml_file(model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)
        for key, val in parameters.items():
            set_multi_key_value(config_data, key, val)

        write_yaml_file(config_data, model_uri, DEFAULT_TRAIN_CONFIG_FILE_NAME)

    def _update_train_metadata(self, advanced_parameters: Dict):
        super()._update_train_metadata(advanced_parameters=advanced_parameters)
        model_meta = ModelMetadata(**self._metadata)

        input_size = InputSize(width=int(advanced_parameters[KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[KEY_EVAL_HEIGHT]))
        model_meta.inputSize = input_size
        model_meta.labels = self.labels

        model_meta.algorithmParameters.update({"mean": advanced_parameters["mean"],
                                               "std": advanced_parameters["std"]})

        self._metadata = model_meta.dict()
