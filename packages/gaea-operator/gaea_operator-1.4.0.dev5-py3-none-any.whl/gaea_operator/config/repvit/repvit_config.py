#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/4/23
# @Author  : liyinggang
# @File    : repvit_config.py
"""
from typing import Dict

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from .. import ConvNextConfig


class RepViTConfig(ConvNextConfig):
    """
    Config write for train, transform and package.
    """
    def __init__(self, windmill_client: WindmillClient, tracker_client: ExperimentTracker, metadata: Dict = {}):
        super().__init__(windmill_client=windmill_client, tracker_client=tracker_client, metadata=metadata)