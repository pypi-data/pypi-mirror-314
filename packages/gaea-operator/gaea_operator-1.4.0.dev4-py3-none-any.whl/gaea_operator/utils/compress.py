#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/6
# @Author  : yanxiaodong
# @File    : compress.py
"""
import os
from typing import List, Union, Tuple
import shutil

import bcelogger


def is_compressed_file(file: str):
    """
    Check if the file is compressed.
    """
    compressed_extensions = ['.zip', '.tar', '.tar.gz', '.tar.bz2', '.tar.xz', '.gz', '.bz2', '.xz']
    file_extension = os.path.splitext(file)[1]
    return file_extension in compressed_extensions


def decompress(filepath: str, ext: str, output_uri: str = "./"):
    """
    Extract the compressed file.
    """
    file_list = []
    if filepath.startswith("/"):
        target_path = os.path.join(output_uri, filepath[1:])
    else:
        target_path = os.path.join(output_uri, filepath)
    shutil.unpack_archive(filepath, target_path)
    bcelogger.info(f"Decompress {filepath} to {target_path}")
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(ext):
                absolute_file = os.path.join(root, file)
                file_list.append(absolute_file)

    return file_list


def is_match_file(file: str, target: Union[str, Tuple]):
    """
    Check if the file matches the target.
    """
    def __is_match(file: str, target: str):
        # 目前匹配是后缀匹配，标注文件可能是train.txt 或者 000000_000000_annotation.txt
        # 需要兼容训练集文档里的trainxxx.txt/valxxx.txt格式
        if file.endswith(target):
            return True
        else:
            parts = target.split(".")
            if len(parts) != 2:
                return False
            if file.startswith(parts[0]) and file.endswith(parts[1]):
                return True
        return False
    if isinstance(target, str):
        if __is_match(file, target):
            return True
    else:
        for t in target:
            if __is_match(file, t):
                return True
    return False


def get_filepaths_in_archive(path: str, output_uri: str, target: Union[str, Tuple], max_depth: int = 1) -> List[str]:
    """
    Traverse the file directory recursively.
    """
    file_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            if root.count(os.sep) - path.count(os.sep) > max_depth:
                break
            for file in files:
                absolute_file = os.path.join(root, file)
                if is_compressed_file(absolute_file):
                    if isinstance(target, str):
                        file_list.extend(decompress(absolute_file, target, output_uri))
                    else:
                        for t in target:
                            file_list.extend(decompress(absolute_file, t, output_uri))
                else:
                    if is_match_file(file, target):
                        file_list.append(absolute_file)
    elif os.path.isfile(path):
        if is_compressed_file(path):
            file_list.extend(decompress(path, target, output_uri))
        else:
            if is_match_file(path, target):
                file_list.append(path)
    else:
        raise ValueError(f"Path {path} is not a file or directory")

    bcelogger.info(f"Found {len(file_list)} target file is {file_list}")

    return file_list