#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import List

from ..base_node import BaseNode
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator


class Train(BaseNode):
    """
    Train
    """
    NAME = "train"
    DISPLAY_NAME = "模型训练"

    def __init__(self, 
                 train_skip: int = -1,
                 accelerator: str = Accelerator.T4):
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

        outputs: List[Variable] = \
            [
                Variable(type="model",
                         name="output_model_uri",
                         displayName="模型训练后的模型",
                         key=f"{self.name()}.model_name",
                         value="train.output_model_uri")
            ]

        super().__init__(outputs=outputs, properties=properties)
        self.train_skip = train_skip

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def __call__(self, *args, **kwargs):
        pass