#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : check.py
"""
from typing import List, Union, Any, Type
from collections import abc
import numpy as np

import bcelogger

from gaea_operator.utils import Tensor, PTensor, TTensor


def check_input_dim(predictions: Tensor, num_classes: int) -> None:
    """
    Check input dimension.
    """
    if num_classes == 2:
        assert predictions.ndim == 1, f'The predictions dimension must be one when num_classes=2, ' \
                                      f'but given: {predictions.ndim}'
    if num_classes > 2:
        assert predictions.ndim >= 1, f'The predictions dimension must be greater than one when num_classes>2, ' \
                                      f'but given: {predictions.ndim}'
    if num_classes == 1:
        assert predictions.ndim == 1, 'The predictions dimension must be one when num_classes=1, ' \

    assert len(predictions) > 0, 'Please check your input, it length == 0'


def check_input_value(predictions: Tensor, references: Tensor, filter_value: float = -1) -> (Tensor, Tensor):
    """
    Check input value.
    """
    index = (predictions == filter_value) | (references == filter_value)

    predictions = predictions[~index]
    references = references[~index]

    return predictions, references


def check_input_length(references: Tensor) -> bool:
    """
    Check length.
    """
    if len(references) == 0:
        bcelogger.warning('Please check your input, it length == 0')
        return False
    return True


def average_precision_check_input_dim(predictions: Tensor, num_classes: int) -> None:
    """
    Check input dimension.
    """
    if num_classes == 2:
        assert predictions.ndim == 1, f'The predictions dimension must be one when num_classes=2, ' \
                                      f'but given: {predictions.ndim} '
    if num_classes > 2:
        assert predictions.ndim == 2, f'The predictions dimension must be two when num_classes>2, ' \
                                      f'but given: {predictions.ndim} '


def check_input_type(predictions: Union[List, Tensor], references: Union[List, Tensor]):
    """
    Check input shape and length.
    """
    assert len(predictions) == len(references), f'predictions length must be same as references, ' \
                                                f'but given predictions: {len(predictions)} ' \
                                                f'and references {len(references)}'
    assert isinstance(predictions, (List, np.ndarray, TTensor, PTensor)), \
        f'predictions type should be in `(List、 np.ndarray、 PTensor、 TTensor)`, but given: {type(predictions)}'


def check_input_num_classes(predictions: Tensor, num_classes: int):
    """
    Check input num classes.
    """
    pre_num_classes = predictions.shape[1]

    assert pre_num_classes == num_classes, f'Number of classes does not match between ' \
                                           f'predictions ({pre_num_classes}) and `self` ({num_classes}).'


def is_seq_of(seq: Any,
              expected_type: Union[Type, tuple],
              seq_type: Type = None) -> bool:
    """
    Check whether it is a sequence of some type.

    Args:
        seq: The sequence to be checked.
        expected_type: Expected type of sequence items.
        seq_type: Expected sequence type. Defaults to None.
    """
    if seq_type is None:
        exp_seq_type = abc.Sequence
    else:
        assert isinstance(seq_type, type)
        exp_seq_type = seq_type
    if not isinstance(seq, exp_seq_type):
        return False
    for item in seq:
        if not isinstance(item, expected_type):
            return False
    return True


def is_list_of(seq, expected_type):
    """
    Check whether it is a list of some type.
    """
    return is_seq_of(seq, expected_type, seq_type=list)
