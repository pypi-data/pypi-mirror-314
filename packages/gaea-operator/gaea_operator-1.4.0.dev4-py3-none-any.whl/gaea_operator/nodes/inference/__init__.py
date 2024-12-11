#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import Dict, List
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

import bcelogger

from ..base_node import BaseNode, set_node_parameters, calculate_template_ensemble_time
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator, ModelTemplate


class Inference(BaseNode):
    """
    Transform
    """
    NAME = "inference"
    DISPLAY_NAME = "模型包评估"

    def __init__(self,
                 inference_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        nvidia_accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        kunlun_accelerator = get_accelerator(kind=Accelerator.KUNLUN)
        ascend_accelerator = get_accelerator(kind=Accelerator.ASCEND)

        properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: ["training"] + nvidia_accelerator.suggest_resource_tips(),
                                    Accelerator.KUNLUN: ["training"] + kunlun_accelerator.suggest_resource_tips(),
                                    Accelerator.ASCEND: ["training"] + ascend_accelerator.suggest_resource_tips(),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: nvidia_accelerator.suggest_flavour_tips(),
                                    Accelerator.KUNLUN: kunlun_accelerator.suggest_flavour_tips(),
                                    Accelerator.ASCEND: ascend_accelerator.suggest_flavour_tips(),
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {f"{self.name()}.model_name": ["Python", "TensorRT"]},
                                    Accelerator.KUNLUN: {f"{self.name()}.model_name": ["Python", "PaddleLite"]},
                                    Accelerator.ASCEND: {f"{self.name()}.model_name": ["Python", "Other"]},
                                })

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="package.output_model_uri"),
                Variable(type="dataset", name="input_dataset_uri", value="eval.output_dataset_uri")
            ]

        super().__init__(inputs=inputs, properties=properties)

        self.inference_skip = inference_skip
        self.algorithm = algorithm
        self.pre_nodes = pre_nodes

    def suggest_time_profiler(self):
        """
        suggest time profiler
        """
        if self.properties.timeProfilerParams.qps is None:
            bcelogger.warning("Inference use template ensemble model")
            model_template = ModelTemplate(accelerator=self.properties.accelerator)
            time_profiler_params = model_template.suggest_time_profiler(
                key=self.properties.timeProfilerParams.networkArchitecture, node_name=self.name())

            time_count = calculate_template_ensemble_time(benchmark=time_profiler_params,
                                                          image_count=self.properties.timeProfilerParams.evalImageCount,
                                                          width=self.properties.timeProfilerParams.width,
                                                          height=self.properties.timeProfilerParams.height,
                                                          eval_size=self.properties.timeProfilerParams.evalSize,
                                                          precision=self.properties.timeProfilerParams.precision)
            bcelogger.info(f"Inference time count: {time_count}")

            return time_count

        time_count = 1 / self.properties.timeProfilerParams.qps * self.properties.timeProfilerParams.evalImageCount
        bcelogger.info(f"Inference time count: {time_count}")

        return time_count

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 ensemble_model_name: str = "",
                 dataset_name: str = ""):
        inference_params = {"skip": self.inference_skip,
                            "accelerator": self.properties.accelerator,
                            "model_name": ensemble_model_name,
                            "dataset_name": dataset_name,
                            "advanced_parameters": '{"conf_threshold":"0.5"}'}
        inference_env = {"ACCELERATOR": "{{accelerator}}",
                         "MODEL_NAME": "{{model_name}}",
                         "DATASET_NAME": "{{dataset_name}}",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        inference_params.update(base_params)
        inference_env.update(base_env)
        accelerator = get_accelerator(name=self.properties.accelerator)
        inference_env.update(accelerator.suggest_env())

        inference = ContainerStep(name=Inference.name(),
                                  docker_env=self.suggest_image(),
                                  env=inference_env,
                                  parameters=inference_params,
                                  outputs={"output_uri": Artifact()},
                                  command=f'cd /root && '
                                          f'python3 -m gaea_operator.nodes.inference.inference '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.inference_skip, step=inference, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return inference
