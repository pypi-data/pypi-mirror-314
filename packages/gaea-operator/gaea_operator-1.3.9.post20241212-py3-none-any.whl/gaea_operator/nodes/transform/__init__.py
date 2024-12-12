#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import Dict, List
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

from ..base_node import BaseNode, set_node_parameters
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Transform(BaseNode):
    """
    Transform
    """
    NAME = "transform"
    DISPLAY_NAME = "模型转换"

    def __init__(self,
                 transform_skip: int = -1,
                 algorithm: str = "",
                 category: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        nvidia_accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        ascend_accelerator = get_accelerator(kind=Accelerator.ASCEND)

        properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: ["training"] + nvidia_accelerator.suggest_resource_tips(),
                                    Accelerator.KUNLUN: ["training"],
                                    Accelerator.ASCEND: ["training"] + ascend_accelerator.suggest_resource_tips(),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: nvidia_accelerator.suggest_flavour_tips(),
                                    Accelerator.KUNLUN: "c4m16",
                                    Accelerator.ASCEND: ascend_accelerator.suggest_flavour_tips(),
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {f"{self.name()}.train_model_name": ["PaddlePaddle", "PyTorch"],
                                                         f"{self.name()}.transform_model_name": ["TensorRT"]},
                                    Accelerator.KUNLUN: {f"{self.name()}.train_model_name": ["PaddlePaddle", "PyTorch"],
                                                         f"{self.name()}.transform_model_name": ["PaddleLite"]},
                                    Accelerator.ASCEND: {f"{self.name()}.train_model_name": ["PaddlePaddle", "PyTorch"],
                                                         f"{self.name()}.transform_model_name": ["Other"]},
                                })

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="train.output_model_uri")
            ]
        outputs: List[Variable] = \
            [
                Variable(type="model",
                         name="output_model_uri",
                         displayName="模型转换后的模型",
                         key=f"{self.name()}.transform_model_name",
                         value="transform.output_model_uri")
            ]

        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.transform_skip = transform_skip
        self.algorithm = algorithm
        self.category = category
        self.pre_nodes = pre_nodes

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        if get_accelerator(self.properties.accelerator).get_kind == Accelerator.NVIDIA:
            return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind] + \
                [f"tags.accelerator={self.properties.accelerator}"]
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 train_model_name: str = "",
                 transform_model_name: str = "",
                 transform_model_display_name: str = "",
                 advanced_parameters: str = ""):
        """
        call
        """
        transform_params = {"skip": self.transform_skip,
                            "train_model_name": train_model_name,
                            "transform_model_name": transform_model_name,
                            "transform_model_display_name": transform_model_display_name,
                            "accelerator": self.properties.accelerator,
                            "advanced_parameters": advanced_parameters}
        transform_env = {"TRAIN_MODEL_NAME": "{{train_model_name}}",
                         "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                         "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                         "ACCELERATOR": "{{accelerator}}",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_env.update(base_env)
        transform_params.update(base_params)

        transform = ContainerStep(name=Transform.name(),
                                  docker_env=self.suggest_image(),
                                  env=transform_env,
                                  parameters=transform_params,
                                  outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                  command=f'cd /root && '
                                          f'python3 -m gaea_operator.nodes.transform.transform '
                                          f'--algorithm={self.algorithm} '
                                          f'--category={self.category} '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}} '
                                          f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.transform_skip, step=transform, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return transform
