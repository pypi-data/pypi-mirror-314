# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify model config.pbtxt/parse.yaml in package step
Authors: wanggaofei(wanggaofei03@baidu.com)
Date:    2023-02-29
"""
import os
import bcelogger
import copy

from tritonv2.dag_builder import PkgDAGBuilder, ADV_PARAM_WIDTH, ADV_PARAM_HEIGHT, ADV_PARAM_CHANNEL, \
    ADV_PARAM_BATCH_SIZE, ADV_PARAM_MODEL_TYPE, ADV_PARAM_MAX_BBOX_COUNT, ADV_PARAM_MODEL_NAME_PAIR
from tritonv2.update_pbtxt import PBTXT_NAME, ModelConfig, KEY_MAX_BATCH_SIZE

from .update_parse import ParseYamlConfig, KEY_PARSE_NAME
from .generate_transform_config import KEY_EVAL_SIZE


def get_version_sub_verson(version_name):
    """
        get version & sub_version
    """
    version = None
    sub_version = None
    if '-' in version_name:
        v = version_name.split('-')
        version = int(v[0])
        sub_version = int(v[1])
    else:
        version = int(version_name)
        sub_version = 0
    return version, sub_version


def find_version_folder(path: str):
    """
    find version folder from the path
    """
    max_version = None
    max_sub_version = None
    version_folder = ''
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            version, sub_version = get_version_sub_verson(d)
            if max_version is None or max_version < version \
                    or (max_version == version and max_sub_version < sub_version):
                max_version = version
                max_sub_version = sub_version
                version_folder = d

    return version_folder


class ModifyPackageFiles(object):
    """
    解析修改模型包 parse.yaml
    """

    def __init__(self,
                 sub_models: dict = {},
                 extra_models: dict = {},
                 metadata: dict = {},
                 transform_model_uri: str = '',
                 model_repo: str = '',
                 template_ensemble_name: str = '',
                 template_ensemble_version: str = ''):
        # 1. read parameter of modify
        algo_param_dict = self.get_algorithm_parameters(metadata)
        algo_param_dict['inferenceMaxBatchSize'] = algo_param_dict['maxBatchSize'] \
            if 'maxBatchSize' in algo_param_dict else algo_param_dict.get("inferenceMaxBatchSize")

        self.eval_width = 0
        self.eval_height = 0
        if 'inputSize' in metadata:
            self.eval_width = int(metadata['inputSize']['width']) if 'width' in metadata['inputSize'] else 0
            self.eval_height = int(metadata['inputSize']['height']) if 'height' in metadata['inputSize'] else 0
        self.max_batch_size = int(algo_param_dict['inferenceMaxBatchSize'])
        self.max_box_count = int(metadata['maxBoxNum']) if 'maxBoxNum' in metadata else None
        self.channel = 3
        if self.max_batch_size is None:
            self.max_batch_size = 1
        self.labels = self.get_yaml_categories(metadata)
        if 'channel' in metadata:
            self.channel = int(metadata['channel'])
        if 'encapsulation_config' in metadata:
            if KEY_EVAL_SIZE in metadata['encapsulation_config']:
                self.eval_width, self.eval_height = metadata['encapsulation_config'].pop(KEY_EVAL_SIZE).split('*')
                bcelogger.info(f"ModifyPackageFiles encapsulation_config \
                                eval_width = {self.eval_width}, eval_height = {self.eval_height}")
            if 'tasks' in metadata['encapsulation_config']:
                self.labels = metadata['encapsulation_config']['tasks']
        bcelogger.info(f"ModifyPackageFiles labels = {self.labels}")
        self.advanced_parameters = {ADV_PARAM_WIDTH: self.eval_width,
                                    ADV_PARAM_HEIGHT: self.eval_height,
                                    ADV_PARAM_BATCH_SIZE: self.max_batch_size,
                                    ADV_PARAM_CHANNEL: self.channel}
        if self.max_box_count is not None:
            self.advanced_parameters[ADV_PARAM_MAX_BBOX_COUNT] = self.max_box_count
        bcelogger.info("advanced_parameters: {}".format(self.advanced_parameters))

        self.transform_model_uri = transform_model_uri
        self.model_repo = model_repo
        self.sub_models = sub_models
        self.extra_models = extra_models
        self.ensemble_name = template_ensemble_name
        self.ensemble_version = template_ensemble_version

        bcelogger.info(f"ModifyPackageFiles  max_batch_size = {self.max_batch_size}, \
            max_box_count = {self.max_box_count}")

    def modify_model_config(self, network_architecture: str, contain_preprocess: str = "true"):
        """
        modify transform model config.pbtxt
        """
        width = int(self.eval_width) if self.eval_width is not None else None
        height = int(self.eval_height) if self.eval_height is not None else None
        channel = int(self.channel) if self.channel is not None else None
        batch_size = int(self.max_batch_size) if self.max_batch_size is not None else None
        max_bbox_count = int(self.max_box_count) if self.max_box_count is not None else None

        pbtxt_path = os.path.join(self.transform_model_uri, PBTXT_NAME)
        pbtxt = ModelConfig._create_from_file(pbtxt_path)
        input_names = pbtxt.get_input_names()

        if width is not None and height is not None and channel is not None:
            for v in input_names:
                if len(pbtxt.get_shape_by_name(v)) == 4:
                    # 2.1 input/warmup shape
                    if 'change-ocrnet' in network_architecture:
                        channel = 6
                    pbtxt.set_model_input_warmup_shape(v, width, height, channel, batch_size, contain_preprocess)

        pbtxt.set_field(KEY_MAX_BATCH_SIZE, batch_size)
        pbtxt.modify_dynamic_batching(batch_size)

        # modify model output shape (segmentation only)
        if 'ocrnet' in network_architecture and width is not None and height is not None:
            pbtxt.set_segment_width_height(width, height)

        # modify model output number (dbnet only)
        if network_architecture == "dbnet_student":
            pbtxt.delete_output(name="sigmoid_11.tmp_0")

        # modify model output max bbox shape (ppyoloe plus only)
        if 'ppyoloe' in network_architecture:
            if max_bbox_count is None:
                raise ValueError('Max box is None. need set')
            pbtxt.modify_output_dim_value(['det_boxes', 'det_scores', 'det_classes'], max_bbox_count)

        # modify model output shape (resnet only)
        if 'resnet' in network_architecture and 'cvresnet' not in network_architecture:
            category_num_list = [len(label['categories']) if 'categories' in label else -1 for label in self.labels]
            category_num = max(category_num_list)
            pbtxt.set_output_dims(None, 0, dims=[category_num])

        if 'yoloseg' in network_architecture:
            pbtxt.set_output_dims('masks', -2, dims=[height, width])

        if 'cvresnet' in network_architecture:
            category_num_list = [len(label['categories']) if 'categories' in label else -1 for label in self.labels]
            category_num = max(category_num_list)
            pbtxt.set_output_dims(None, 0, dims=[len(self.labels), category_num])

        pbtxt.write_config_to_file(pbtxt_path)

    def write_relate_config(self,
                            ensemble_name: str,
                            model_name: str,
                            template_model_name: str,
                            model_display_name: str,
                            network_architecture: str,
                            is_update_labels: bool = True):
        """
        modify model-package dag by model name
        """
        builder = PkgDAGBuilder(model_repo=self.model_repo,
                                ensemble_name=self.ensemble_name,
                                ensemble_version=self.ensemble_version,
                                sub_models=self.sub_models,
                                extra_models=self.extra_models)
        self.advanced_parameters.update({ADV_PARAM_MODEL_TYPE: network_architecture})
        modify_sub_models, modify_extra_models = builder.modify_connect_model(
            model_name=template_model_name,
            advanced_parameters=self.advanced_parameters)
        bcelogger.info(f"modify connect sub models {modify_sub_models} extra models {modify_extra_models}")
        models = copy.deepcopy(modify_sub_models)
        models.update(modify_extra_models)
        for name in models:
            if name in self.sub_models:
                modify_sub_models[name] = self.sub_models[name]
            if name in self.extra_models:
                modify_extra_models[name] = self.extra_models[name]

        parse_model_name = self._modify_parse_yaml(model_name=model_name,
                                                   ensemble_name=ensemble_name,
                                                   template_model_name=template_model_name,
                                                   model_display_name=model_display_name,
                                                   is_update_labels=is_update_labels)
        assert parse_model_name is not None, 'parse post process error'
        bcelogger.info(f"modify parse model name is {parse_model_name}")
        if parse_model_name not in modify_sub_models:
            modify_sub_models[parse_model_name] = self.sub_models[parse_model_name]

        return modify_sub_models, modify_extra_models

    def modify_ensemble_config(self, model_name_pairs: dict = {}):
        """
        modify model-package dag by model name
        """
        builder = PkgDAGBuilder(model_repo=self.model_repo,
                                ensemble_name=self.ensemble_name,
                                ensemble_version=self.ensemble_version,
                                sub_models=self.sub_models,
                                extra_models=self.extra_models)
        bcelogger.info(f"modify ensemble model pairs is {model_name_pairs}")
        builder.modify_ensemble(model_name_pairs=model_name_pairs)

    def get_algorithm_parameters(self, metadata: dict):
        """
        get algorithm parameter dict from meta.yaml
        """
        yaml_data = metadata

        if 'algorithmParameters' in yaml_data:
            alg_param = yaml_data['algorithmParameters']
            return alg_param.copy()
        return {}

    def get_yaml_categories(self, metadata: dict):
        """
            获取YAML中的类别列表，返回一个列表。
        每个元素都是一个字符串，代表一个类别名称。
        
        Returns:
            list (str) - 类别列表，每个元素为一个字符串，代表一个类别名称。
        """
        if metadata.get("labels") is None:
            return [{}]
        
        task = {}
        task['categories'] = metadata['labels']
        task['task_source'] = 'single_task'
        return [task]

    def _modify_parse_yaml(self,
                           ensemble_name: str,
                           model_name: str,
                           template_model_name: str,
                           model_display_name: str,
                           is_update_labels: bool = True):
        """
            search & modify parse.yaml information
        """
        # 1. search parse.yaml
        for model, version in self.sub_models.items():
            parse_name = os.path.join(self.model_repo, model, version, KEY_PARSE_NAME)
            if os.path.exists(parse_name):
                bcelogger.info(f"modify parse_yaml: {parse_name}, ensemble_name: {ensemble_name}, \
                model_name: {model_name}, template_model_name: {template_model_name}, \
                is update labels: {is_update_labels}")
                cfg = ParseYamlConfig(parse_name)
                # 1. set ensemble name
                cfg.modify_ensemble_name(ensemble_name)

                # 2. set categories
                if is_update_labels and self.labels is not None:
                    cfg.modify_labels(self.labels,
                                      modify_model_name=model_name,
                                      template_model_name=template_model_name)

                # 3. set model name
                cfg.modify_model_name(modify_model_name=model_name,
                                      template_model_name=template_model_name,
                                      modify_model_display_name=model_display_name)

                # 4. save
                cfg.save_yaml(parse_name)

                return model
        return None


if __name__ == '__main__':
    pass
