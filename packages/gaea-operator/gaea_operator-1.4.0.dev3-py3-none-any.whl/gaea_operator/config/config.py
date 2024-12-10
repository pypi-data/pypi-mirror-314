#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/26
# @Author  : yanxiaodong
# @File    : config.py
"""
from typing import Dict
import copy
import os
from abc import ABCMeta
import bcelogger

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize

from gaea_operator.utils import DEFAULT_TRANSFORM_CONFIG_FILE_NAME, Accelerator
from .generate_transform_config import generate_transform_config, KEY_CONTAIN_PREPROCESS
from .modify_package_files import ModifyPackageFiles
from .generate_transform_config import KEY_EVAL_SIZE, \
    KEY_EVAL_WIDTH, \
    KEY_EVAL_HEIGHT, \
    KEY_MAX_BATCH_SIZE, \
    KEY_MAX_BOX_NUM, \
    KEY_IOU_THRESHOLD, \
    KEY_CONF_THRESHOLD, \
    KEY_PRECISION

KEY_NETWORK_ARCHITECTURE = 'networkArchitecture'
KEY_WORKER_NUM_STANDARD = 'workerNum'
KEY_BATCH_SIZE_STANDARD = 'batchSize'
KEY_EVAL_HEIGHT_STANDARD = 'evalHeight'
KEY_EVAL_WIDTH_STANDARD = 'evalWidth'


class Config(metaclass=ABCMeta):
    """
    Config write for train, transform and package.
    """
    accelerator2model_format = {Accelerator.T4: "TensorRT",
                                Accelerator.A100: "TensorRT",
                                Accelerator.V100: "TensorRT",
                                Accelerator.A10: "TensorRT",
                                Accelerator.A800: "TensorRT",
                                Accelerator.R200: "PaddleLite",
                                Accelerator.Atlas310: "Other"}

    def __init__(self, windmill_client: WindmillClient, tracker_client: ExperimentTracker, metadata: Dict = {}):
        self.windmill_client = windmill_client
        self.tracker_client = tracker_client
        self._metadata = metadata

    @property
    def metadata(self):
        """
        Get metadata.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value: dict):
        """
        Set metadata.
        """
        self._metadata = ModelMetadata(**value).dict()

    def write_train_config(self,
                           dataset_uri: str,
                           model_uri: str,
                           advanced_parameters: dict,
                           pretrain_model_uri: str):
        """
        Config write for train.
        """
        pass

    def write_eval_config(self, dataset_uri: str, model_uri: str, ):
        """
        Config write for eval.
        """
        pass

    def write_transform_config(self, model_uri: str, advanced_parameters: dict):
        """
        Config write for transform.
        """
        if KEY_EVAL_HEIGHT_STANDARD in advanced_parameters:
            advanced_parameters[KEY_EVAL_HEIGHT] = advanced_parameters.pop(KEY_EVAL_HEIGHT_STANDARD)
        if KEY_EVAL_WIDTH_STANDARD in advanced_parameters:
            advanced_parameters[KEY_EVAL_WIDTH] = advanced_parameters.pop(KEY_EVAL_WIDTH_STANDARD)

        cfg_path = os.path.join(model_uri, DEFAULT_TRANSFORM_CONFIG_FILE_NAME)
        self._update_transform_metadata(advanced_parameters)

        generate_transform_config(advanced_parameters, cfg_path, self.metadata)

    def write_model_config(self, transform_model_uri: str, advanced_parameters: dict):
        """
        Config write for transform model.
        """
        network_architecture = self.metadata["algorithmParameters"].get(KEY_NETWORK_ARCHITECTURE, "")
        bcelogger.info('network architecture: {}'.format(network_architecture))
        contain_preprocess = advanced_parameters.get(KEY_CONTAIN_PREPROCESS, "true")
        cfg = ModifyPackageFiles(metadata=self.metadata, transform_model_uri=transform_model_uri)
        cfg.modify_model_config(network_architecture=network_architecture, contain_preprocess=contain_preprocess)

    def write_relate_config(self,
                            model_repo: str,
                            model_display_name: str,
                            template_ensemble_name: str,
                            template_ensemble_version: str,
                            ensemble_name: str,
                            sub_models: dict,
                            model_name: str,
                            template_model_name: str,
                            is_new_ensemble_model: bool = True,
                            extra_models: dict = None,
                            is_update_labels: bool = True):
        """
        Config write for connect model.
        """
        network_architecture = self.metadata["algorithmParameters"].get(KEY_NETWORK_ARCHITECTURE, "")
        bcelogger.info('network architecture: {}'.format(network_architecture))
        cfg = ModifyPackageFiles(sub_models=sub_models,
                                 extra_models=extra_models,
                                 metadata=self.metadata,
                                 model_repo=model_repo,
                                 template_ensemble_name=template_ensemble_name,
                                 template_ensemble_version=template_ensemble_version)
        modify_sub_models, modify_extra_models = cfg.write_relate_config(model_name=model_name,
                                                                         ensemble_name=ensemble_name,
                                                                         template_model_name=template_model_name,
                                                                         model_display_name=model_display_name,
                                                                         network_architecture=network_architecture,
                                                                         is_update_labels=is_update_labels)

        # 如果转换模型是BLS节点，修改与之关联的节点
        if extra_models is not None and len(extra_models) > 0 and template_model_name in extra_models:
            cfg.modify_ensemble_config({template_model_name: (model_name, -1)})

        new_sub_models = copy.deepcopy(sub_models)
        new_extra_models = copy.deepcopy(extra_models)
        if is_new_ensemble_model:
            new_sub_models.update(new_extra_models)
            for name, version in new_sub_models.items():
                if name == template_model_name:
                    continue
                if name in sub_models:
                    modify_sub_models[name] = version
                if name in extra_models:
                    modify_extra_models[name] = version

        return modify_sub_models, modify_extra_models

    def write_ensemble_config(self,
                              model_repo: str,
                              sub_models: dict,
                              model_name_pairs: dict,
                              ensemble_name: str,
                              ensemble_version: str,
                              extra_models: dict = None):
        """
        Config write for ensemble.
        """
        cfg = ModifyPackageFiles(sub_models=sub_models,
                                 extra_models=extra_models,
                                 metadata=self.metadata,
                                 model_repo=model_repo,
                                 template_ensemble_name=ensemble_name,
                                 template_ensemble_version=ensemble_version)
        return cfg.modify_ensemble_config(model_name_pairs=model_name_pairs)

    def _update_train_metadata(self, advanced_parameters: Dict):
        meta_data = ModelMetadata(experimentName=self.tracker_client.experiment_name,
                                  jobName=self.tracker_client.job_name,
                                  jobDisplayName=self.tracker_client.job_display_name,
                                  algorithmParameters={KEY_NETWORK_ARCHITECTURE:
                                                           str(advanced_parameters[KEY_NETWORK_ARCHITECTURE])},
                                  experimentRunID=self.tracker_client.run_id)
        self._metadata = meta_data.dict()

    def _update_transform_metadata(self, advanced_parameters: Dict):
        """
            更新模型的转换元数据，包括输入尺寸、实验名称、作业名称、运行ID和最大框数等。
        如果在参数中提供了评估尺寸，则将其分解为宽度和高度并存储在单独的字段中。
        然后，创建一个InputSize对象，并将其添加到ModelMetadata对象中。
        最后，更新算法参数，包括最大批处理大小、网络架构、IoU阈值、置信度阈值和精度。
        
        Args:
            advanced_parameters (Dict): 包含转换参数的字典，包括评估尺寸、最大框数、最大批处理大小、网络架构、IoU阈值、置信度阈值和精度等。
                KEY_EVAL_SIZE (str)：评估尺寸，格式为"宽度*高度"。
                KEY_MAX_BOX_NUM (str)：最大框数，默认为1。
                KEY_MAX_BATCH_SIZE (str)：最大批处理大小，默认为-1。
                KEY_NETWORK_ARCHITECTURE (str)：网络架构。
                KEY_IOU_THRESHOLD (str)：IoU阈值，默认为-1。
                KEY_CONF_THRESHOLD (str)：置信度阈值，默认为-1。
                KEY_PRECISION (str)：精度，默认为"fp16"。
        
        Returns:
            None.
        """
        if self._metadata is None:
            self._metadata = {}

        encapsulation_config = None
        if 'encapsulation_config' in self._metadata.keys():
            if KEY_EVAL_SIZE in self._metadata['encapsulation_config'].keys():
                encapsulation_config = self._metadata['encapsulation_config']
                advanced_parameters[KEY_EVAL_SIZE] = encapsulation_config[KEY_EVAL_SIZE]
                bcelogger.info(f"_update_transform_metadata use encapsulation_config update eval_size: \
                                {advanced_parameters[KEY_EVAL_SIZE]}")

        if KEY_EVAL_SIZE in advanced_parameters:
            width, height = advanced_parameters.pop(KEY_EVAL_SIZE).split('*')
            advanced_parameters[KEY_EVAL_WIDTH] = width
            advanced_parameters[KEY_EVAL_HEIGHT] = height

        input_size = InputSize(width=int(advanced_parameters[KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[KEY_EVAL_HEIGHT]))

        meta_data = ModelMetadata(**self._metadata)

        meta_data.inputSize = input_size
        meta_data.experimentName = self.tracker_client.experiment_name
        meta_data.jobName = self.tracker_client.job_name
        meta_data.experimentRunID = self.tracker_client.run_id
        max_box_num = int(advanced_parameters[KEY_MAX_BOX_NUM]) \
            if KEY_MAX_BOX_NUM in advanced_parameters else 1
        meta_data.maxBoxNum = max_box_num

        advanced_parameters = {
            'maxBatchSize': str(advanced_parameters.get(KEY_MAX_BATCH_SIZE, -1)),
            KEY_NETWORK_ARCHITECTURE: str(advanced_parameters[KEY_NETWORK_ARCHITECTURE]),
            'iouThreshold': str(advanced_parameters.get(KEY_IOU_THRESHOLD, -1)),
            'confThreshold': str(advanced_parameters.get(KEY_CONF_THRESHOLD, -1)),
            'precision': advanced_parameters.get(KEY_PRECISION, "fp16")
        }

        if meta_data.algorithmParameters is None:
            meta_data.algorithmParameters = advanced_parameters
        else:
            meta_data.algorithmParameters.update(advanced_parameters)

        self._metadata = meta_data.dict()
        if encapsulation_config is not None:
            self._metadata['encapsulation_config'] = encapsulation_config


def get_pretrained_model_path(pretrained_model_path, extension: str = ".pdparams"):
    """
        get pretrained model absolute path
    """
    paths = []
    for filepath in os.listdir(pretrained_model_path):
        if filepath.endswith(extension):
            bcelogger.info('find pth file: {}'.format(filepath))
            paths.append(os.path.join(pretrained_model_path, filepath))
    return paths


def convert_value_type(val):
    """
    convert string to real data type
    """
    if val is None:
        return val
    if val.isdigit():
        return int(val)
    elif val.replace('.', '', 1).isdigit():
        return float(val)
    else:
        return val


def set_multi_key_value(config_dict, multi_key, val):
    """
    set all do not care parameter
    """
    keys = multi_key.split('.')
    for idx, key in enumerate(keys):
        if isinstance(config_dict, dict) and key in config_dict:
            if idx + 1 == len(keys):
                config_dict[key] = [convert_value_type(v) for v in val] if isinstance(val, list) \
                    else convert_value_type(val)
                bcelogger.info(f"set key: {multi_key} value: {config_dict[key]}")
            else:
                config_dict = config_dict[key]
        elif isinstance(config_dict, list):
            for op in config_dict:
                set_multi_key_value(op, ".".join(keys[idx:]), val)
        else:
            break
