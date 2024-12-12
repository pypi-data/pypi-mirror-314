#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : transform_component.py
"""
import os
import json
from argparse import ArgumentParser
import base64
import shutil

import bcelogger
from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillclient.client.windmill_client import WindmillClient
from gaea_operator.transform import Transform

from ..download_artifact import download_artifact
from gaea_operator.config import Config, KEY_NETWORK_ARCHITECTURE
from gaea_operator.utils import write_file, ModelTemplate, is_base64
from gaea_operator.config.generate_transform_config import KEY_ACCELERATOR
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
    parser.add_argument("--train-model-name",
                        type=str,
                        default=os.environ.get("TRAIN_MODEL_NAME"))
    parser.add_argument("--transform-model-name",
                        type=str,
                        default=os.environ.get("TRANSFORM_MODEL_NAME"))
    parser.add_argument("--transform-model-display-name",
                        type=str,
                        default=os.environ.get("TRANSFORM_MODEL_DISPLAY_NAME"))
    parser.add_argument("--accelerator", type=str, default=os.environ.get("ACCELERATOR", "t4"))
    parser.add_argument("--advanced-parameters",
                        type=str,
                        default=os.environ.get("ADVANCED_PARAMETERS", "{}"))
    parser.add_argument("--category", type=str, default=os.environ.get("CATEGORY", "Image/ObjectDetection"))
    parser.add_argument("--algorithm", type=str, default=os.environ.get("ALGORITHM", ModelTemplate.PPYOLOE_PLUS_NAME))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def transform(args):
    """
    Transform component for model.
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
    model_uri, model_name = download_artifact(windmill_client=windmill_client,
                                              input_uri=args.input_model_uri,
                                              artifact_name=args.train_model_name,
                                              output_uri="/home/windmill/tmp/model")
    response = windmill_client.get_artifact(name=model_name)
    bcelogger.info(f"Model artifact is {response}")
    metadata = response.metadata

    # 2. 下载模板模型
    try:
        model = windmill_client.get_artifact(object_name=args.transform_model_name, version="latest")
        bcelogger.info(f"Get transform model {args.transform_model_name} success")
        model_name = model.objectName
    except Exception:
        model = ModelTemplate(windmill_client=windmill_client,
                              scene=args.scene,
                              accelerator=args.accelerator,
                              model_store_name=args.public_model_store,
                              algorithm=args.algorithm)
        model_name = model.suggest_template_model()
        bcelogger.info(f"Get template model {model_name} success")
    transform_model = windmill_client.get_model(workspace_id=parse_model_name(model_name).workspace_id,
                                                model_store_name=parse_model_name(model_name).model_store_name,
                                                local_name=parse_model_name(model_name).local_name)
    windmill_client.download_artifact(object_name=model_name, version="latest", output_uri=args.output_model_uri)

    # 3. 生成转换配置文件，固定名称 transform_config.yaml 保存在 output_model_uri
    if is_base64(args.advanced_parameters):
        transform_advanced_parameters = json.loads(base64.b64decode(args.advanced_parameters))
    else:
        transform_advanced_parameters = json.loads(args.advanced_parameters)
    config_for_sdk_file = os.path.join(model_uri, "config_for_sdk_encapsulation.yaml")
    if os.path.exists(config_for_sdk_file):
        encap_config = encapsulation_config.EncapsulationConfig(config_for_sdk_file)
        encap_config.parse()
        metadata['encapsulation_config'] = {}
        for key, value in encap_config.advanced_parameters().items():
            metadata['encapsulation_config'][key] = value
            bcelogger.info(f"Advanced parameters use \
                config_for_sdk_encapsulation.yaml update key: {key}, value: {value}")
        shutil.copy(config_for_sdk_file, args.output_model_uri)
    else:
        bcelogger.info(f"config_for_sdk_encapsulation.yaml not exist")
    transform_advanced_parameters.update({KEY_ACCELERATOR: args.accelerator})
    model_template = ModelTemplate(algorithm=args.algorithm)
    transform_advanced_parameters[KEY_NETWORK_ARCHITECTURE] = \
        model_template.suggest_network_architecture(transform_advanced_parameters[KEY_NETWORK_ARCHITECTURE])
    bcelogger.info(f"Advanced parameters: {transform_advanced_parameters}")
    config = Config(windmill_client=windmill_client, tracker_client=tracker_client, metadata=metadata)
    config.write_transform_config(model_uri=args.output_model_uri, advanced_parameters=transform_advanced_parameters)

    # 4. 修改config.pbtxt配置文件
    config.write_model_config(transform_model_uri=args.output_model_uri,
                              advanced_parameters=transform_advanced_parameters)

    # 5. 转换
    Transform(windmill_client=windmill_client).transform(transform_config_dir=args.output_model_uri,
                                                         src_model_uri=model_uri,
                                                         dst_model_uri=args.output_model_uri)

    # 6. 上传转换后的模型
    model_name_instance = parse_model_name(name=args.transform_model_name)
    workspace_id = model_name_instance.workspace_id
    model_store_name = model_name_instance.model_store_name
    local_name = model_name_instance.local_name
    prefer_model_server_parameters = transform_model.preferModelServerParameters
    prefer_model_server_parameters["resource"]["accelerator"] = args.accelerator
    tags = transform_model.artifact["tags"] if transform_model.artifact["tags"] is not None else {}
    tags.pop("sourceVersion", None)
    response = windmill_client.create_model(
        artifact_uri=args.output_model_uri,
        workspace_id=workspace_id,
        model_store_name=model_store_name,
        local_name=local_name,
        display_name=args.transform_model_display_name,
        prefer_model_server_parameters=prefer_model_server_parameters,
        category=transform_model.category["category"],
        artifact_metadata=config.metadata,
        artifact_tags=tags,
        model_formats=transform_model.modelFormats)
    bcelogger.info(f"Model {args.transform_model_name} created response: {response}")

    # 7. 输出文件
    write_file(obj=json.loads(response.raw_data)["artifact"], output_dir=args.output_model_uri)


if __name__ == "__main__":
    args = parse_args()
    transform(args=args)
