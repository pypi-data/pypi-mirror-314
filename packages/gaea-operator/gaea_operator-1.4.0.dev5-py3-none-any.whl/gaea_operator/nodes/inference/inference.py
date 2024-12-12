#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/22
# @Author  : yanxiaodong
# @File    : inference.py
"""
import os
from argparse import ArgumentParser
import json
import base64
import shutil

from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
import bcelogger
from windmilltrainingv1.client.training_api_dataset import \
    parse_dataset_name, \
    ANNOTATION_FORMAT_COCO, \
    ANNOTATION_FORMAT_IMAGENET, \
    ANNOTATION_FORMAT_CITYSCAPES, \
    ANNOTATION_FORMAT_PADDLECLAS, \
    ANNOTATION_FORMAT_PADDLEOCR, \
    ANNOTATION_FORMAT_PADDLESEG
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillcomputev1.filesystem import upload_by_filesystem
from windmillclient.client.windmill_client import WindmillClient
from tritonv2.evaluator import evaluate

from gaea_operator.metric import InferenceMetricAnalysisV2 as InferenceMetricAnalysis
from gaea_operator.metric import Metric
from gaea_operator.dataset import CocoDataset, ImageNetDataset, MultiAttributeDataset, CityscapesDataset, PPOCRDataset
from gaea_operator.utils import get_accelerator, read_file, is_base64, rle_to_polygon


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--windmill-ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill-sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--org-id", type=str, default=os.environ.get("ORG_ID"))
    parser.add_argument("--user-id", type=str, default=os.environ.get("USER_ID"))
    parser.add_argument("--windmill-endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--project-name", type=str, default=os.environ.get("PROJECT_NAME"))
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--accelerator", type=str, default=os.environ.get("ACCELERATOR", "t4"))
    parser.add_argument("--advanced-parameters",
                        type=str,
                        default=os.environ.get("ADVANCED_PARAMETERS", "{}"))
    parser.add_argument("--model-name", type=str, default=os.environ.get("MODEL_NAME"))
    parser.add_argument("--dataset-name", type=str, default=os.environ.get("DATASET_NAME", ""))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--input-dataset-uri", type=str, default=os.environ.get("INPUT_DATASET_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def inference(args):
    """
    Package component for ppyoloe_plus model.
    """
    windmill_client = WindmillClient(ak=args.windmill_ak,
                                     sk=args.windmill_sk,
                                     endpoint=args.windmill_endpoint,
                                     context={"OrgID": args.org_id, "UserID": args.user_id})
    tracker_client = ExperimentTracker(windmill_client=windmill_client,
                                       tracking_uri=args.tracking_uri,
                                       experiment_name=args.experiment_name,
                                       experiment_kind=args.experiment_kind,
                                       project_name=args.project_name)
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))

    if args.input_model_uri is not None and len(args.input_model_uri) > 0:
        bcelogger.info(f"Model artifact input uri is {args.input_model_uri}")
        response = read_file(input_dir=args.input_model_uri)
        args.model_name = response["name"]
    else:
        bcelogger.info(f"Model artifact name is {args.model_name}")
        assert args.model_name is not None and len(args.model_name) > 0, "Model artifact name is None"
    bcelogger.info(f"Model artifact name is {args.model_name}")

    output_model_uri = "/home/windmill/tmp/model"
    # 1. 下载ensemble template 模型
    bcelogger.info(f"Downloading ensemble from {args.model_name}")
    windmill_client.dump_models(artifact_name=args.model_name,
                                location_style="Triton",
                                rename="ensemble",
                                output_uri=output_model_uri)

    # 2.评估数据集
    is_download_dataset = False
    if args.input_dataset_uri is not None and len(args.input_dataset_uri) > 0:
        bcelogger.info(f"Dataset artifact input uri is {args.input_dataset_uri}")
        response = read_file(input_dir=args.input_dataset_uri)
        args.dataset_name = response["name"]
    else:
        args.input_dataset_uri = "/home/windmill/tmp/dataset"
        bcelogger.info(f"Dataset artifact name is {args.dataset_name}")
        assert args.dataset_name is not None and len(args.dataset_name) > 0, "Dataset artifact name is None"
        is_download_dataset = True
    bcelogger.info(f"Dataset artifact name is {args.dataset_name}")

    artifact_name = parse_artifact_name(name=args.dataset_name)
    object_name = artifact_name.object_name
    dataset = parse_dataset_name(name=object_name)
    response = windmill_client.get_dataset(workspace_id=dataset.workspace_id,
                                           project_name=dataset.project_name,
                                           local_name=dataset.local_name)
    bcelogger.info(f"Get dataset {args.dataset_name} response is {response}")
    if is_download_dataset:
        if response.annotationFormat == ANNOTATION_FORMAT_COCO:
            dataset_class = CocoDataset
        elif response.annotationFormat in [ANNOTATION_FORMAT_IMAGENET, ANNOTATION_FORMAT_PADDLECLAS]:
            dataset_class = ImageNetDataset
        elif response.annotationFormat in [ANNOTATION_FORMAT_CITYSCAPES, ANNOTATION_FORMAT_PADDLESEG]:
            dataset_class = CityscapesDataset
        elif response.annotationFormat == ANNOTATION_FORMAT_PADDLEOCR:
            dataset_class = PPOCRDataset
        elif response.annotationFormat == "MultiAttributeDataset":
            dataset_class = MultiAttributeDataset
        else:
            raise ValueError(f'Unsupported annoation format{response.annotationFormat}.')
        bcelogger.info(f"Download dataset {args.dataset_name}")
        dataset = dataset_class(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
        dataset.concat_dataset(dataset_name=args.dataset_name,
                               output_dir=args.input_dataset_uri,
                               usage=dataset_class.usages[1],
                               save_label=True)

    triton_server_extra_args = get_accelerator(name=args.accelerator).suggest_args()
    if is_base64(args.advanced_parameters):
        advanced_parameters = json.loads(base64.b64decode(args.advanced_parameters))
    else:
        advanced_parameters = json.loads(args.advanced_parameters)
    conf_threshold = float(advanced_parameters["conf_threshold"])
    eval_metric_analysis = InferenceMetricAnalysis(conf_threshold=conf_threshold)
    metric = Metric([eval_metric_analysis], dataset_name=response.artifact["name"])

    if response.annotationFormat == ANNOTATION_FORMAT_COCO:
        rle_to_polygon(args.input_dataset_uri + '/val.json')

    # 3.开始评估
    evaluate(model_path=output_model_uri,
             dataset_path=args.input_dataset_uri,
             annotation_format=response.annotationFormat,
             output_uri=tracker_client.job_work_dir,
             metric=metric,
             triton_server_extra_args=triton_server_extra_args)

    # 4.更新model metric 和 metadata
    bcelogger.info(f"Update model {args.model_name} metric and metadata")
    response = windmill_client.get_artifact(name=args.model_name)
    bcelogger.info(f"Get artifact {args.model_name} response is {response}")
    filesystem = windmill_client.suggest_first_filesystem(workspace_id=response.workspaceID,
                                                          guest_name=response.parentName)
    upload_by_filesystem(filesystem=filesystem,
                         file_path=os.path.join(tracker_client.job_work_dir, "metric.json"),
                         dest_path=os.path.join(response.uri, "metric.json"))
    metadata = response.metadata
    metadata["jobName"] = tracker_client.job_name
    metadata["jobDisplayName"] = tracker_client.job_display_name
    bcelogger.info(f"Update artifact {args.model_name} metadata is {metadata}")
    windmill_client.update_artifact(object_name=response.objectName, version=str(response.version), metadata=metadata)


if __name__ == "__main__":
    args = parse_args()
    inference(args=args)
