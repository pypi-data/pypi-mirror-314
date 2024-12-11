#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/27
# @Author  : yanxiaodong
# @File    : misc.py
"""
import json
import yaml
import os
import fcntl
from typing import Dict


def find_upper_level_folder(path: str, level: int = 2):
    """
    Find the folder `levels` levels up from the given path.
    """
    upper_level = path
    for _ in range(level):
        upper_level = os.path.dirname(upper_level)
    return upper_level


def write_file(obj: Dict, output_dir: str, file_name: str = "response.json"):
    """
    Write to json file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, file_name), "w") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def write_yaml_file(obj: Dict, output_dir: str, file_name: str = "response.yaml"):
    """
    Write to yaml file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, file_name), "w") as f:
        yaml.dump(obj, f, allow_unicode=True, sort_keys=False)


def read_file(input_dir: str, file_name: str = "response.json", is_lock: bool = False):
    """
    Read the response list from a file.
    """
    file_path = os.path.join(input_dir, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    if not is_lock:
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        return data

    with open(file_path, "r", encoding='utf-8') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        data = json.load(f)
        fcntl.flock(f, fcntl.LOCK_UN)
    return data


def read_yaml_file(input_dir: str, file_name: str = "response.yaml"):
    """
    Read the response list from a file.
    """
    with open(os.path.join(input_dir, file_name), "r") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    return data


def find_dir(path: str, level: int = 1):
    """
    Find the folder `levels` levels down from the given path.
    """
    down_level = path
    for _ in range(level):
        for d in os.listdir(down_level):
            d = os.path.join(down_level, d)
            if os.path.isdir(d):
                down_level = d
                break

    return down_level