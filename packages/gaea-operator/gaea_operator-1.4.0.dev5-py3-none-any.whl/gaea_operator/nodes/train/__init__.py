#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/12
# @Author  : yanxiaodong
# @File    : __init__.py.py
"""
from typing import List

import bcelogger

from ..base_node import BaseNode, calculate_train_time
from ..types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import Accelerator, get_accelerator, ModelTemplate


class Train(BaseNode):
    """
    Train
    """
    NAME = "train"
    DISPLAY_NAME = "模型训练"

    def __init__(self,
                 train_skip: int = -1,
                 algorithm: str = "",
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
        self.algorithm = algorithm

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind]

    def suggest_time_profiler(self):
        """
        suggest time profiler
        """
        model_template = ModelTemplate(accelerator=self.properties.accelerator)
        time_profiler_params = model_template.suggest_time_profiler(
            key=self.properties.timeProfilerParams.networkArchitecture, kind="train", node_name=self.name())

        train_time_count = calculate_train_time(benchmark=time_profiler_params,
                                                epoch=self.properties.timeProfilerParams.epoch,
                                                image_count=self.properties.timeProfilerParams.trainImageCount,
                                                batch_size=self.properties.timeProfilerParams.batchSize,
                                                width=self.properties.timeProfilerParams.width,
                                                height=self.properties.timeProfilerParams.height,
                                                eval_size=self.properties.timeProfilerParams.evalSize,
                                                gpu_num=self.properties.timeProfilerParams.gpuNum,
                                                worker_num=self.properties.timeProfilerParams.workerNum)
        bcelogger.info(f"Train time count: {train_time_count}")

        time_profiler_params = model_template.suggest_time_profiler(
            key=self.properties.timeProfilerParams.networkArchitecture, kind="val", node_name=self.name())
        val_time_count = calculate_train_time(benchmark=time_profiler_params,
                                              epoch=1,
                                              image_count=self.properties.timeProfilerParams.valImageCount,
                                              batch_size=self.properties.timeProfilerParams.batchSize,
                                              width=self.properties.timeProfilerParams.width,
                                              height=self.properties.timeProfilerParams.height,
                                              eval_size=self.properties.timeProfilerParams.evalSize,
                                              gpu_num=self.properties.timeProfilerParams.gpuNum,
                                              worker_num=self.properties.timeProfilerParams.workerNum)
        bcelogger.info(f"Val time count: {val_time_count}")

        return train_time_count + val_time_count

    def __call__(self, *args, **kwargs):
        pass
