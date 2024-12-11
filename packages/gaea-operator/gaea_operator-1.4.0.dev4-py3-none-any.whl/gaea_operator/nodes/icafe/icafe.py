#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   icafe.py
@Time    :   2024/04/17 11:00:53
@Author  :   lidai@baidu.com 
@License :   (C)Copyright 2021-2024, Baidu
@Desc    :   Sync mlops data to icafe 
'''
from icafeutil.core.icafe_util import IcafeUtil
from argparse import ArgumentParser
import bcelogger

    
def sync_icafe(args):
    """
    将训练过程指标同步到 icafe 对应卡片中
    
    Args:
        args (argparse.Namespace): 命令行参数对象，包含以下属性：
            - stage (str): 目标stage的名称。
            - id (str): 要同步的ICafe卡片的ID。
            - status (str): 要同步的ICafe卡片的状态。
            - stage_description (str): 目标stage的描述信息。
            - operator (str): 操作员名称。
    
    Returns:
        Any: 同步操作的结果，具体类型由ICafeUtil.sync()函数的返回值类型决定。
    
    Raises:
        无
    """
    icafe_util = IcafeUtil()
    stage = get_stage_name(args.stage)
    sync_data = {
        "stage": stage,
        "type": "object",
        "properties": {
            "status": {
            "type": "string",
            "enum": [
                {
                "value": get_stage_status(args.stage),
                "description": args.stage_description
                }
            ]
            }
        }
    }
    try:
        bcelogger.info(f"sync_icafe error: id: {args.id}, "
                        f"status: {args.status} ,data: {sync_data}, operator: {args.operator}")
        ret = icafe_util.sync(card_id=args.id, status=args.status, data=sync_data, operator=args.operator)
    except Exception as e:
        bcelogger.error(f"sync_icafe error: id: {args.id}, "
                        f"status: {args.status} ,data: {sync_data}, operator: {args.operator}")


def get_stage_name(stage):
    """
    根据输入的 stage 名称, 返回 scheme 数据
    
    Args:
    - stage (str): 数据处理的阶段名称，格式为"stage_name.sub_stage_name"。
    
    Returns:
    - str: 数据文件夹名称，格式为"Data/StageName"。
    
    """
    stage_info = stage.split(".")
    if len(stage_info) > 0:
        if stage_info[0] == "aigc":
            return "Data/AIGC"
        if stage_info[0] == "web_spider":
            return "Data/WebSpider"
        if stage_info[0] == "manual_annotation":
            return "Data/ManualAnnotation"
        if stage_info[0] == "model_annotation":
            return "Data/ModelAnnotation"
        if stage_info[0] == "train":
            return "Data/Train"
        if stage_info[0] == "eval":
            return "Data/Eval"
        if stage_info[0] == "transform":
            return "Data/Transform"
        if stage_info[0] == "package":
            return "Data/Package"
    return "Data/Other"

def get_stage_status(stage):
    """
    获取 stage 状态
    
    Args:
        stage (str): 包含stage信息的字符串，格式为"stage.status"。
    
    Returns:
        str: stage的状态，如果stage信息格式不正确，则返回"unknown"。
    
    """
    stage_info = stage.split(".")
    if len(stage_info) > 1:
       return stage_info[1]
    return "unknown"
    
def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, default='')
    parser.add_argument("--status", type=str, default='')
    parser.add_argument("--stage", type=str, default='')
    parser.add_argument("--stage_description", type=str, default='')
    parser.add_argument("--operator", type=str, default='')

    args, _ = parser.parse_known_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    sync_icafe(args=args)