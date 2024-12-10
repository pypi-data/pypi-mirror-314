#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/7
# @Author  : yanxiaodong
# @File    : metric.py
"""
import os
from typing import Dict, List, Union, Optional

import bcelogger
from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmilltrainingv1.client.training_api_project import parse_project_name

from gaea_operator.utils import read_file, format_time, write_file, DEFAULT_METRIC_FILE_NAME
from .types.metric import BaseMetric
from gaea_operator.metric.analysis import EvalMetricAnalysis
from gaea_operator.metric.analysis import InferenceMetricAnalysis, InferenceMetricAnalysisV2
from gaea_operator.metric.analysis import LabelStatisticMetricAnalysis


class Metric(object):
    """
    Metric class.
    """

    def __init__(self,
                 metric: List[Union[
                     EvalMetricAnalysis,
                     InferenceMetricAnalysis,
                     InferenceMetricAnalysisV2,
                     LabelStatisticMetricAnalysis]],
                 dataset_name: str = None,
                 annotation_set_name: str = None):
        self.dataset_name = dataset_name
        self.annotation_set_name = annotation_set_name
        self.metric = metric

    def save(self, metric_result: Dict, output_uri: str):
        """
        Save metric.
        """
        if os.path.splitext(output_uri)[1] == "":
            output_dir = output_uri
            file_name = "metric.json"
        else:
            output_dir = os.path.dirname(output_uri)
            file_name = os.path.basename(output_uri)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        write_file(obj=metric_result, output_dir=output_dir, file_name=file_name)

    def set_images(self, images: List[Dict]):
        """
        Set images.
        """
        for m in self.metric:
            if hasattr(m, "set_images"):
                m.set_images(images)

    def set_labels(self, labels: List):
        """
        Set labels.
        """
        for m in self.metric:
            if hasattr(m, "set_labels"):
                m.set_labels(labels)

    def update(self, predictions: List[Dict], references: List[Dict], task_kind: str = None):
        """
        Update metric.
        """
        for m in self.metric:
            m.reset()
            m.update(predictions=predictions, references=references, task_kind=task_kind)

    def compute(self, artifact_name: Optional[str] = None, task_kind: str = None,):
        """
        Compute metric.
        """
        metric_result = {"labels": [], "metrics": []}
        for m in self.metric:
            res = m.compute()
            if "labels" in res:
                metric_result["labels"] = res["labels"]
            if "metrics" in res:
                metric_result["metrics"].extend(res["metrics"])

        base_metric = BaseMetric(artifactName=artifact_name,
                                 datasetName=self.dataset_name,
                                 annotationSetName=self.annotation_set_name,
                                 taskKind=task_kind,
                                 createdAt=format_time())
        metric_result.update(base_metric.dict(by_alias=True, exclude_none=True))

        return metric_result

    def __call__(self, references: List[Dict] = None,
                 predictions: List[Dict] = None,
                 output_uri: str = "./",
                 task_kind: str = None,
                 artifact_name: Optional[str] = None):
        self.update(predictions=predictions, references=references, task_kind=task_kind)

        metric_result = self.compute(artifact_name=artifact_name, task_kind=task_kind)

        self.save(metric_result=metric_result, output_uri=output_uri)

        bcelogger.info(f"Metric result save path: {output_uri}")


def update_metric_file(windmill_client: WindmillClient,
                       tracker_client: ExperimentTracker,
                       dataset_name: str,
                       model_object_name: str,
                       model_artifact_name: str):
    """
    Update metric file.
    """
    bcelogger.info(f"Model artifact name is {model_artifact_name}")
    base_metric = BaseMetric(artifactName=model_artifact_name,
                             datasetName=dataset_name,
                             updatedAt=format_time(),
                             baselineJobName=tracker_client.job_name)

    try:
        response = windmill_client.get_artifact(object_name=model_object_name, version="best")
        bcelogger.info(f"Get best artifact name {model_object_name} response {response}")
        if response.name != model_artifact_name:
            bcelogger.info(f"Get baseline model name {response.name}")
            baseline_model_name = response.name
            tags = [{"artifactName": baseline_model_name}, {"datasetName": dataset_name}]
            project_name = parse_project_name(tracker_client.project_name)
            response = windmill_client.list_job(workspace_id=project_name.workspace_id,
                                                project_name=project_name.local_name,
                                                tags=tags)
            if len(response.result) > 0:
                base_metric.baselineJobName = response.result[0]["name"]
            bcelogger.info(f"Base metric dict is {base_metric.dict()}")
    except Exception as e:
        bcelogger.error(f"Get best artifact name {model_object_name} error {e}")

    metric_dir = tracker_client.job_work_dir
    metric_data = read_file(input_dir=metric_dir, file_name=DEFAULT_METRIC_FILE_NAME)
    metric_data.update(base_metric.dict())
    write_file(obj=metric_data, output_dir=metric_dir, file_name=DEFAULT_METRIC_FILE_NAME)


def update_metric_file_with_dataset(dataset_name: str, input_dir: str, file_name: str):
    """
    Update metric file with dataset.
    """
    base_metric = BaseMetric(datasetName=dataset_name, updatedAt=format_time())
    metric_data = read_file(input_dir=input_dir, file_name=file_name)
    metric_data.update(base_metric.dict())
    write_file(obj=metric_data, output_dir=input_dir, file_name=file_name)


def get_score_from_file(filepath: str, metric_name: str):
    """
    Get metric name score from file.
    """
    metric_data = read_file(input_dir=os.path.dirname(filepath), file_name=os.path.basename(filepath))
    return get_score_from_metric_raw(metric_data=metric_data, metric_name=metric_name)


def get_score_from_metric_raw(metric_data: Dict, metric_name: str):
    """
    Get metric name score from raw.
    """
    for metric in metric_data["metrics"]:
        if metric["name"] == metric_name:
            if isinstance(metric["result"], Dict):
                return list(metric["result"].values())[0]
            return metric["result"]
