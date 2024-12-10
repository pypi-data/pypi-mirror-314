#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/7
# @Author  : yanxiaodong
# @File    : model.py
"""
import bcelogger
from windmillclient.client.windmill_client import WindmillClient
from pyserver.naming.naming import truncate_local_name

from gaea_operator.metric.metric import get_score_from_file


class Model:
    """
    Model class.
    """
    def __init__(self, windmill_client: WindmillClient):
        self.windmill_client = windmill_client

    def get_best_model_score(self, model_name: str, metric_name: str):
        """
        Get the best score of model.
        """
        try:
            best_alias = "best"
            response = self.windmill_client.get_artifact(object_name=model_name, version=best_alias)
            bcelogger.info(f"Get artifact {model_name} response: {response}")

            self.windmill_client.download_artifact(object_name=model_name, version=best_alias, output_uri="./")
            best_score = get_score_from_file("./metric.json", metric_name=metric_name)
            assert best_score is not None, f"Can not get score from metric, please check metric name {metric_name}."
            version = response.version
        except Exception as e:
            bcelogger.error(f"Get artifact {model_name} error: {e}")
            best_score = 0
            version = None

        return best_score, version


def format_name(name: str, category: str):
    """
    Merge model name.
    """
    return truncate_local_name(f"{name}-{category}")


def format_display_name(name: str, category: str):
    """
    Merge model name.
    """
    return f"{name}-{category}"[-80:]
