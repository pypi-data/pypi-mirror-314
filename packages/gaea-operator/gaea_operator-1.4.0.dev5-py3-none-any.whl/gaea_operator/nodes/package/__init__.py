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

from ..base_node import BaseNode, set_node_parameters
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Package(BaseNode):
    """
    Transform
    """
    NAME = "package"
    DISPLAY_NAME = "模型组装"

    def __init__(self,
                 package_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        transform_model_name = f"{self.name()}.transform_model_name"
        ensemble_model_name = f"{self.name()}.ensemble_model_name"

        properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: ["training"],
                                    Accelerator.KUNLUN: ["training"],
                                    Accelerator.ASCEND: ["training"],
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: "c4m16",
                                    Accelerator.KUNLUN: "c4m16",
                                    Accelerator.ASCEND: "c4m16",
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {transform_model_name: ["TensorRT"],
                                                         ensemble_model_name: ["Python", "TensorRT"]},
                                    Accelerator.KUNLUN: {transform_model_name: ["PaddleLite"],
                                                         ensemble_model_name: ["Python", "PaddleLite"]},
                                    Accelerator.ASCEND: {transform_model_name: ["Other"],
                                                         ensemble_model_name: ["Python", "Other"]},
                                })

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="transform.output_model_uri")
            ]
        outputs: List[Variable] = \
            [
                Variable(type="model",
                         name="output_model_uri",
                         displayName="模型组装后的模型",
                         key=f"{self.name()}.ensemble_model_name",
                         value="package.output_model_uri")
            ]

        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.package_skip = package_skip
        self.algorithm = algorithm
        self.pre_nodes = pre_nodes

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 transform_model_name: str = "",
                 ensemble_model_name: str = "",
                 sub_extra_models: str = "",
                 ensemble_model_display_name: str = ""):
        package_params = {"skip": self.package_skip,
                          "accelerator": self.properties.accelerator,
                          "transform_model_name": transform_model_name,
                          "ensemble_model_name": ensemble_model_name,
                          "sub_extra_models": sub_extra_models,
                          "ensemble_model_display_name": ensemble_model_display_name}
        package_env = {"ACCELERATOR": "{{accelerator}}",
                       "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                       "ENSEMBLE_MODEL_NAME": "{{ensemble_model_name}}",
                       "SUB_EXTRA_MODELS": "{{sub_extra_models}}",
                       "ENSEMBLE_MODEL_DISPLAY_NAME": "{{ensemble_model_display_name}}"}
        package_params.update(base_params)
        package_env.update(base_env)

        package = ContainerStep(name=Package.name(),
                                docker_env=self.suggest_image(),
                                env=package_env,
                                parameters=package_params,
                                outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                command=f'cd /root && '
                                        f'python3 -m gaea_operator.nodes.package.package '
                                        f'--algorithm={self.algorithm} '
                                        f'--input-model-uri={{{{input_model_uri}}}} '
                                        f'--output-uri={{{{output_uri}}}} '
                                        f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.package_skip, step=package, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return package
