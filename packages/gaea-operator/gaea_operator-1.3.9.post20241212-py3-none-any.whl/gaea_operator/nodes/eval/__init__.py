#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import List, Dict
from paddleflow.pipeline import ContainerStep

from ..base_node import BaseNode
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Eval(BaseNode):
    """
    Train
    """
    NAME = "eval"
    DISPLAY_NAME = "模型评估"

    def __init__(self, 
                 eval_skip: int = -1,
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        nvidia_accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        ascend_accelerator = get_accelerator(kind=Accelerator.ASCEND)

        properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA:
                                        ["training", "tags.usage=train"] + nvidia_accelerator.suggest_resource_tips(),
                                    Accelerator.ASCEND:
                                        ["training", "tags.usage=train"] + ascend_accelerator.suggest_resource_tips(),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: nvidia_accelerator.suggest_flavour_tips(),
                                    Accelerator.ASCEND: ascend_accelerator.suggest_flavour_tips(),
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle", "PyTorch"]},
                                    Accelerator.ASCEND: {f"{self.name()}.model_name": ["PaddlePaddle", "PyTorch"]},
                                })

        inputs: List[Variable] = \
            [
                Variable(type="model", name="input_model_uri", value="train.output_model_uri")
            ]
        outputs: List[Variable] = \
            [
                Variable(type="dataset",
                         name="output_dataset_uri",
                         displayName="模型评估的数据集",
                         value="eval.output_dataset_uri"),
                Variable(type="model",
                         name="output_model_uri",
                         displayName="模型评估后的模型",
                         key=f"{self.name()}.model_name",
                         value="eval.output_model_uri")
            ]

        super().__init__(inputs=inputs, outputs=outputs, properties=properties)
        self.eval_skip = eval_skip
        self.pre_nodes = pre_nodes

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def __call__(self, *args, **kwargs):
        pass