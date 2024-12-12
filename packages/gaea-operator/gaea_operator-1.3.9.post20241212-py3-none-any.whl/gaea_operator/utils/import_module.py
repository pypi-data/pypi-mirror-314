#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File          : plugin.py    
@Author        : yanxiaodong
@Date          : 2023/6/20
@Description   :
"""
from typing import TYPE_CHECKING, TypeVar, Optional, Dict
from types import ModuleType
import importlib
import numpy as np
import warnings


def try_import(name: str) -> Optional[ModuleType]:
    """
    Try to import a module.
    """
    try:
        return importlib.import_module(name)
    except ImportError:
        warnings.warn("'{}' library import error, please check install correctly".format(name))
        return None


def try_import_class(module: ModuleType, target: str):
    """
    Try to import a class.
    """
    if module is None:
        return CustomObject

    strs = target.rsplit('.', maxsplit=1)
    if len(strs) == 2:
        module = module.__name__ + '.' + strs[0]
        module = importlib.import_module(module)
        target = strs[-1]
    return getattr(module, target)


class CustomObject(Dict):
    """
    Inheritance object.
    """
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass


if TYPE_CHECKING:
    import paddle
    from paddle import Tensor as PTensor
else:
    paddle = try_import('paddle')
    PTensor = try_import_class(paddle, 'Tensor')


if TYPE_CHECKING:
    import torch
    from torch import Tensor as TTensor
else:
    torch = try_import('torch')
    TTensor = try_import_class(torch, 'Tensor')


Tensor = TypeVar('Tensor', PTensor, TTensor, np.ndarray)