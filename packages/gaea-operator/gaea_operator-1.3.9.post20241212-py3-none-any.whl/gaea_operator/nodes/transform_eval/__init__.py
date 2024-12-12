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
from gaea_operator.utils import get_accelerator, Accelerator


class TransformEval(BaseNode):
    """
    Transform
    """
    NAME = "transform-eval"
    DISPLAY_NAME = "模型转换评估"

    def __init__(self,
                 transform_eval_skip: int = -1,
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
                                    Accelerator.NVIDIA: {f"{self.name()}.model_name": ["TensorRT"]},
                                    Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddleLite"]},
                                    Accelerator.ASCEND: {f"{self.name()}.model_name": ["Other"]},
                                })

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="transform.output_model_uri"),
                Variable(type="dataset", name="input_dataset_uri", value="eval.output_dataset_uri")
            ]
        outputs: List[Variable] = \
            [
                Variable(type="dataset",
                         name="output_dataset_uri",
                         displayName="模型转换评估的数据",
                         key=f"{self.name()}.model_name",
                         value="transform-eval.output_dataset_uri")
            ]

        super().__init__(inputs=inputs, outputs=outputs, properties=properties)

        self.transform_eval_skip = transform_eval_skip
        self.algorithm = algorithm
        self.pre_nodes = pre_nodes

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 dataset_name: str = "",
                 transform_model_name: str = ""):
        transform_eval_params = {"skip": self.transform_eval_skip,
                                 "accelerator": self.properties.accelerator,
                                 "dataset_name": dataset_name,
                                 "model_name": transform_model_name,
                                 "advanced_parameters": '{"conf_threshold":"0.5",'
                                                        '"iou_threshold":"0.5"}'}
        transform_eval_env = {"ACCELERATOR": "{{accelerator}}",
                              "DATASET_NAME": "{{dataset_name}}",
                              "MODEL_NAME": "{{model_name}}",
                              "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_eval_params.update(base_params)
        transform_eval_env.update(base_env)
        accelerator = get_accelerator(name=self.properties.accelerator)
        transform_eval_env.update(accelerator.suggest_env())

        transform_eval = ContainerStep(name=TransformEval.name(),
                                       docker_env=self.suggest_image(),
                                       env=transform_eval_env,
                                       parameters=transform_eval_params,
                                       outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                                       command=f'cd /root && '
                                               f'python3 -m gaea_operator.nodes.transform_eval.transform_eval '
                                               f'--algorithm={self.algorithm} '
                                               f'--input-model-uri={{{{input_model_uri}}}} '
                                               f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                               f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                               f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.transform_eval_skip,
                            step=transform_eval,
                            inputs=self.inputs,
                            pre_nodes=self.pre_nodes)

        return transform_eval
