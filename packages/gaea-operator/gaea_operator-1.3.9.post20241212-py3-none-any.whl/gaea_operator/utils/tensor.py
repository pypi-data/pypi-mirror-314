#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : tensor_operations.py
"""
from typing import List
import numpy as np

from .import_module import PTensor, torch


def list2ndarray(value: List) -> np.ndarray:
    """
    List to np.ndarray.
    """
    if isinstance(value, List):
        value = np.array(value)

    return value


def numpy_round2list(value: np.ndarray, decimals: int):
    """
    Numpy round to list.
    """
    return np.round(value, decimals=decimals).tolist()


def paddle_round2list(value: PTensor, decimals: int):
    """
    Paddle round to list.
    """
    return np.round(value.numpy().astype(float), decimals=decimals).tolist()


def torch_round2list(value: PTensor, decimals: int):
    """
    Torch round to list.
    """
    return torch.round(value, decimals=decimals).tolist()


def list_round(value: List, decimals: int):
    """
    List round.
    """
    return [round(v, decimals) for v in value]
