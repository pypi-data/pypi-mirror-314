#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/20
# @Author  : yanxiaodong
# @File    : base_node.py
"""
from typing import List, Dict
from abc import ABCMeta, abstractmethod
from paddleflow.pipeline import ContainerStep

from .types import Properties
from gaea_operator.artifacts import Variable
from gaea_operator.utils import get_accelerator


class BaseNode(metaclass=ABCMeta):
    """
    BaseNode
    """
    NAME = ""
    DISPLAY_NAME = ""

    def __init__(self,
                 inputs: List[Variable] = None,
                 outputs: List[Variable] = None,
                 properties: Properties = None,
                 **kwargs):
        self._inputs = inputs
        self._outputs = outputs
        self._properties = properties

    @classmethod
    def name(cls):
        """
        name
        """
        return cls.NAME

    @classmethod
    def display_name(cls):
        """
        display_name
        """
        return cls.DISPLAY_NAME

    @property
    def inputs(self) -> List[Variable]:
        """
        input
        """
        return self._inputs

    @inputs.setter
    def inputs(self, values: List[Variable]):
        if values is not None:
            self._inputs = values

    @property
    def outputs(self) -> List[Variable]:
        """
        output
        """
        return self._outputs

    @outputs.setter
    def outputs(self, values: List[Variable]):
        if values is not None:
            self._outputs = values

    @property
    def properties(self) -> Properties:
        """
        properties
        """
        return self._properties

    @properties.setter
    def properties(self, values: Properties):
        if self._properties is None:
            self._properties = values
        else:
            properties_dict = self._properties.dict()
            for key, value in values.dict().items():
                default_value = Properties.__fields__[key].default
                if value != default_value:
                    properties_dict[key] = value
            self._properties = Properties(**properties_dict)

    def suggest_image(self):
        """
        suggest image
        """
        for image in self.properties.images:
            if image.kind == get_accelerator(self.properties.accelerator).get_kind:
                return image.name
        return ""

    def suggest_compute_tips(self):
        """
        suggest compute tips
        """
        return self.properties.computeTips[get_accelerator(self.properties.accelerator).get_kind] + \
            [f"tags.accelerator={self.properties.accelerator}"]

    def suggest_model_formats(self, key: str):
        """
        suggest model formats
        """
        return self.properties.modelFormats[get_accelerator(self.properties.accelerator).get_kind][key]

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def set_node_parameters(skip: int, step: ContainerStep, inputs: List[Variable], pre_nodes: Dict[str, ContainerStep]):
    """
    set node parameters
    """
    if skip > 0:
        skip_parameter = "skip"
        step.condition = f"{step.parameters[skip_parameter]} < 0"

    for variable in inputs:
        if variable.value != "" and skip < 0:
            name, value = variable.value.split(".")
            step.inputs[variable.name] = getattr(pre_nodes[name], "outputs")[value]
        else:
            step.parameters[variable.name] = ""