#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/22
# @Author  : yanxiaodong
# @File    : transform_eval.py
"""
import os
import shutil
from argparse import ArgumentParser
from typing import Dict
import json
import base64

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
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillartifactv1.client.artifact_api_artifact import get_name, parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from tritonv2.evaluator import evaluate

from ..download_artifact import download_artifact
from gaea_operator.config import Config
from gaea_operator.dataset import CocoDataset, ImageNetDataset, MultiAttributeDataset, CityscapesDataset, PPOCRDataset
from gaea_operator.metric import EvalMetricAnalysis, Metric
from gaea_operator.utils import find_dir, \
    read_file, \
    is_base64, \
    get_accelerator, \
    ModelTemplate, \
    DEFAULT_TRITON_CONFIG_FILE_NAME, \
    rle_to_polygon
import gaea_operator.config.std_algorithm.encapsulation_config as encapsulation_config


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
    parser.add_argument("--scene", type=str, default=os.environ.get("SCENE"))
    parser.add_argument("--public-model-store",
                        type=str,
                        default=os.environ.get("PUBLIC_MODEL_STORE", "workspaces/public/modelstores/default"))
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--accelerator", type=str, default=os.environ.get("ACCELERATOR", "t4"))
    parser.add_argument("--algorithm", type=str, default=os.environ.get("ALGORITHM", ""))
    parser.add_argument("--dataset-name", type=str, default=os.environ.get("DATASET_NAME", ""))
    parser.add_argument("--model-name", type=str, default=os.environ.get("MODEL_NAME", ""))
    parser.add_argument("--advanced-parameters",
                        type=str,
                        default=os.environ.get("ADVANCED_PARAMETERS", "{}"))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--input-dataset-uri", type=str, default=os.environ.get("INPUT_DATASET_URI"))
    parser.add_argument("--output-dataset-uri", type=str, default=os.environ.get("OUTPUT_DATASET_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def package_model_by_template(windmill_client: WindmillClient,
                              tracker_client: ExperimentTracker,
                              metadata: Dict,
                              input_model_uri: str,
                              output_model_uri: str,
                              ensemble_name: str,
                              sub_models: Dict,
                              model_name: str):
    """
    Package model by template.
    """
    sub_models = {model: "" for model, _ in sub_models.items()}
    config = Config(windmill_client=windmill_client, tracker_client=tracker_client, metadata=metadata)
    sub_models, _ = config.write_relate_config(model_repo=output_model_uri,
                                               sub_models=sub_models,
                                               extra_models={},
                                               model_name=model_name,
                                               template_model_name=model_name,
                                               model_display_name="",
                                               template_ensemble_name=ensemble_name,
                                               ensemble_name=ensemble_name,
                                               template_ensemble_version="")
    bcelogger.info('modify sub model: {}'.format(sub_models))

    model_uri = os.path.join(output_model_uri, model_name)
    shutil.rmtree(find_dir(model_uri))
    if os.path.exists(os.path.join(model_uri, str(1))):
        shutil.rmtree(os.path.join(model_uri, str(1)))
    shutil.copytree(src=input_model_uri, dst=os.path.join(model_uri, str(1)))
    shutil.copyfile(src=os.path.join(find_dir(model_uri), DEFAULT_TRITON_CONFIG_FILE_NAME),
                    dst=os.path.join(model_uri, DEFAULT_TRITON_CONFIG_FILE_NAME))


def transform_eval(args):
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

    # 1. 下载模型
    transform_model_uri, model_name = download_artifact(windmill_client=windmill_client,
                                                        input_uri=args.input_model_uri,
                                                        artifact_name=args.model_name,
                                                        output_uri="/home/windmill/tmp/transform",
                                                        is_copy=True)

    # 2. 获取模型信息
    response = windmill_client.get_artifact(name=model_name)
    metadata = response.metadata

    # 增加参数解析
    config_for_sdk_file = os.path.join(transform_model_uri, "config_for_sdk_encapsulation.yaml")
    if os.path.exists(config_for_sdk_file):
        encap_config = encapsulation_config.EncapsulationConfig(config_for_sdk_file)
        encap_config.parse()
        metadata['encapsulation_config'] = {}
        for key, value in encap_config.advanced_parameters().items():
            metadata['encapsulation_config'][key] = value
            bcelogger.info(f"Advanced parameters use \
                config_for_sdk_encapsulation.yaml update key: {key}, value: {value}")

    else:
        bcelogger.info(f"config_for_sdk_encapsulation.yaml not exist")

    # 3. 下载ensemble template 模型
    ensemble_model_uri = "/home/windmill/tmp/model"
    model_template = ModelTemplate(windmill_client=windmill_client,
                                   accelerator=args.accelerator,
                                   model_store_name=args.public_model_store,
                                   algorithm=args.algorithm)
    ensemble = model_template.suggest_template_ensemble()
    ensemble_artifact_name = get_name(object_name=ensemble, version="latest")
    bcelogger.info(f"Dumping model {ensemble_artifact_name} to {ensemble_model_uri}")
    windmill_client.dump_models(artifact_name=ensemble_artifact_name,
                                location_style="Triton",
                                rename="ensemble",
                                output_uri=ensemble_model_uri)

    # 4. 基于模板文件组装转换后模型包
    response = windmill_client.get_artifact(name=ensemble_artifact_name)
    model = parse_model_name(model_template.suggest_template_model()).local_name
    package_model_by_template(windmill_client=windmill_client,
                              tracker_client=tracker_client,
                              metadata=metadata,
                              input_model_uri=transform_model_uri,
                              output_model_uri=ensemble_model_uri,
                              ensemble_name="ensemble",
                              sub_models=response.metadata["subModels"],
                              model_name=model)

    # 5.评估数据集
    if args.input_dataset_uri is not None and len(args.input_dataset_uri) > 0:
        bcelogger.info(f"Dataset artifact input uri is {args.input_dataset_uri}")
        response = read_file(input_dir=args.input_dataset_uri)
        args.dataset_name = response["name"]
    else:
        bcelogger.info(f"Dataset artifact name is {args.dataset_name}")
        assert args.dataset_name is not None and len(args.dataset_name) > 0, "Dataset artifact name is None"
    bcelogger.info(f"Dataset artifact name is {args.dataset_name}")

    # 3.1 获取数据集信息
    artifact_name = parse_artifact_name(name=args.dataset_name)
    object_name = artifact_name.object_name
    dataset = parse_dataset_name(name=object_name)
    response = windmill_client.get_dataset(workspace_id=dataset.workspace_id,
                                           project_name=dataset.project_name,
                                           local_name=dataset.local_name)

    # 3.2 下载数据集
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
        raise ValueError(f'Unsupported annotation format {response.annotationFormat}.')
    bcelogger.info(f"Download dataset {args.dataset_name} to {args.output_dataset_uri}")
    dataset = dataset_class(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
    dataset.concat_dataset(dataset_name=args.dataset_name,
                           output_dir=args.output_dataset_uri,
                           usage=dataset_class.usages[1],
                           save_label=True)
    
    if response.category['category'] in ("Image/InstanceSegmentation", ):
        rle_to_polygon(args.output_dataset_uri + '/val.json')

    triton_server_extra_args = get_accelerator(name=args.accelerator).suggest_args()
    if is_base64(args.advanced_parameters):
        advanced_parameters = json.loads(base64.b64decode(args.advanced_parameters))
    else:
        advanced_parameters = json.loads(args.advanced_parameters)
    conf_threshold = advanced_parameters["conf_threshold"]
    iou_threshold = advanced_parameters["iou_threshold"]
    eval_metric_analysis = EvalMetricAnalysis(category=response.category["category"],
                                              conf_threshold=conf_threshold,
                                              iou_threshold=iou_threshold)
    metric = Metric([eval_metric_analysis], dataset_name=response.artifact["name"])

    # 6.开始评估
    bcelogger.info(f'eval output uri: {tracker_client.job_work_dir}')
    evaluate(model_path=ensemble_model_uri,
             dataset_path=args.output_dataset_uri,
             annotation_format=response.annotationFormat,
             output_uri=tracker_client.job_work_dir,
             metric=metric,
             triton_server_extra_args=triton_server_extra_args)


if __name__ == "__main__":
    args = parse_args()
    transform_eval(args=args)
