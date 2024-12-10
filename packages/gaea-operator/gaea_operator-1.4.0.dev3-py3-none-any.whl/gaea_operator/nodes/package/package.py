#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : transform_component.py
"""
import copy
import json
import os
import time
from argparse import ArgumentParser

from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
import bcelogger
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillmodelv1.client.model_api_model import parse_model_name, ModelMetadata
from windmillartifactv1.client.artifact_api_artifact import get_name, parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient

from ..download_artifact import download_artifact
from gaea_operator.config import Config
from gaea_operator.model import format_name, format_display_name
from gaea_operator.utils import write_file, ModelTemplate, get_accelerator
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
    parser.add_argument("--ensemble-model-name",
                        type=str,
                        default=os.environ.get("ENSEMBLE_MODEL_NAME"))
    parser.add_argument("--ensemble-model-display-name",
                        type=str,
                        default=os.environ.get("ENSEMBLE_MODEL_DISPLAY_NAME"))
    parser.add_argument("--accelerator", type=str, default=os.environ.get("ACCELERATOR", "t4"))
    parser.add_argument("--algorithm", type=str, default=os.environ.get("ALGORITHM", ""))
    parser.add_argument("--transform-model-name",
                        type=str,
                        default=os.environ.get("TRANSFORM_MODEL_NAME"))
    parser.add_argument("--sub-extra-models",
                        type=str,
                        default=os.environ.get("SUB_EXTRA_MODELS"))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def create_model(windmill_client: WindmillClient,
                 tracker_client: ExperimentTracker,
                 model_uri: str,
                 model_name: str,
                 model_version: str,
                 workspace_id: str,
                 template_workspace_id: str,
                 model_store_name: str,
                 template_model_store_name: str,
                 transform_model_name: str,
                 transform_model_display_name: str,
                 scene: str,
                 accelerator: str,
                 model_index: int):
    """
    create model.
    """
    model_uri = os.path.join(model_uri, model_name, model_version)

    bcelogger.info(f"get model workspace id: {template_workspace_id} "
                   f"model store name: {template_model_store_name} local name: {model_name}")
    response = windmill_client.get_model(workspace_id=template_workspace_id,
                                         model_store_name=template_model_store_name,
                                         local_name=model_name)
    local_name = response.localName
    
    display_name = response.displayName
    if scene is None or len(scene) == 0:
        if response.category["category"] == "Image/Preprocess":
            local_name = format_name(transform_model_name, "pre" + str(model_index))
            display_name = format_display_name(transform_model_display_name, "预处理")
        if response.category["category"] == "Image/Postprocess":
            local_name = format_name(transform_model_name, "post" + str(model_index))
            display_name = format_display_name(transform_model_display_name, "后处理")
    else:
        local_name = local_name + str(model_index)

    bcelogger.info(f"created model {local_name}")
    prefer_model_server_parameters = response.preferModelServerParameters
    if prefer_model_server_parameters is None:
        prefer_model_server_parameters = get_accelerator(name=accelerator).suggest_model_server_parameters()
    else:
        prefer_model_server_parameters["resource"]["accelerator"] = accelerator
    tags = response.artifact["tags"] if response.artifact["tags"] is not None else {}
    tags.pop("sourceVersion", None)
    meta_data = ModelMetadata(experimentName=tracker_client.experiment_name,
                              jobName=tracker_client.job_name,
                              experimentRunID=tracker_client.run_id).dict()
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=display_name,
                                            category=response.category["category"],
                                            model_formats=response.modelFormats,
                                            prefer_model_server_parameters=prefer_model_server_parameters,
                                            artifact_tags=tags,
                                            artifact_metadata=meta_data,
                                            artifact_uri=model_uri)
    bcelogger.info(f"Model {local_name} created response: {response}")

    return response.localName, response.artifact["version"]


def package(args):
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

    # 1. 下载 transform model
    transform_model_uri, transform_model_name = download_artifact(windmill_client=windmill_client,
                                                                  input_uri=args.input_model_uri,
                                                                  artifact_name=args.transform_model_name,
                                                                  output_uri="/home/windmill/tmp/model")

    # 2. get transform model meta信息
    artifact_name = parse_artifact_name(name=transform_model_name)
    model = parse_model_name(name=artifact_name.object_name)
    transform = windmill_client.get_model(workspace_id=model.workspace_id,
                                          model_store_name=model.model_store_name,
                                          local_name=model.local_name)
    bcelogger.info(f"get model {artifact_name.object_name} response is {transform}")

    # 3. 解析ensemble模型
    model_names = {"ensemble_name": parse_model_name(name=args.ensemble_model_name),
                   "transform_model_name": parse_model_name(name=artifact_name.object_name)}

    is_new_ensemble_model = True
    try:
        ensemble = windmill_client.get_artifact(object_name=args.ensemble_model_name, version="latest")
        bcelogger.info(f"get ensemble model {args.ensemble_model_name} success")
        model_names["template_transform_model_name"] = parse_model_name(name=transform.name)
        model_names["template_ensemble_name"] = parse_model_name(name=args.ensemble_model_name)
        current_ensemble_name = ensemble.name
        is_new_ensemble_model = False
    except Exception:
        model_template = ModelTemplate(windmill_client=windmill_client,
                                       scene=args.scene,
                                       accelerator=args.accelerator,
                                       model_store_name=args.public_model_store,
                                       algorithm=args.algorithm)
        model_names["template_transform_model_name"] = parse_model_name(model_template.suggest_template_model())
        model_names["template_ensemble_name"] = parse_model_name(model_template.suggest_template_ensemble())
        current_ensemble_name = get_name(object_name=model_template.suggest_template_ensemble(), version="latest")
        ensemble = windmill_client.get_artifact(name=current_ensemble_name)
    bcelogger.info(f"is_new_ensemble_model: {is_new_ensemble_model}")

    # 4. 下载 ensemble 模型
    ensemble_model_uri = "/home/windmill/tmp/ensemble"
    bcelogger.info(f"Dumping model {current_ensemble_name} to {ensemble_model_uri}")
    windmill_client.dump_models(artifact_name=current_ensemble_name,
                                location_style="Triton",
                                output_uri=ensemble_model_uri)

    # 5. 获取 ensemble 的 sub models 和 extra models
    origin_sub_models = ensemble.metadata["subModels"]
    if 'extraModels' in ensemble.metadata and ensemble.metadata["extraModels"] is not None:
        origin_extra_models = ensemble.metadata["extraModels"]
    else:
        origin_extra_models = {}

    # 如果不是新创建的模型包，校验transform是否在ensemble
    if not is_new_ensemble_model:
        sub_extra_models = copy.deepcopy(origin_sub_models)
        sub_extra_models.update(origin_extra_models)
        name = model_names["transform_model_name"].local_name
        assert name in sub_extra_models, f"{name} not in {sub_extra_models}"
    bcelogger.info(f"ensemble {current_ensemble_name} "
                   f"sub models: {origin_sub_models} extra models: {origin_extra_models}")

    # 增加参数解析
    config_for_sdk_file = os.path.join(transform_model_uri, "config_for_sdk_encapsulation.yaml")
    if os.path.exists(config_for_sdk_file):
        encap_config = encapsulation_config.EncapsulationConfig(config_for_sdk_file)
        encap_config.parse()
        metadata = transform.artifact["metadata"]
        metadata['encapsulation_config'] = {}
        for key, value in encap_config.advanced_parameters().items():
            metadata['encapsulation_config'][key] = value
            bcelogger.info(f"Advanced parameters use \
                config_for_sdk_encapsulation.yaml update key: {key}, value: {value}")
    else:
        bcelogger.info(f"config_for_sdk_encapsulation.yaml not exist")

    # 5. 寻找关联节点并且修改对应的 config.pbtxt 配置文件
    config = Config(windmill_client=windmill_client,
                    tracker_client=tracker_client,
                    metadata=transform.artifact["metadata"])
    modify_sub_models, modify_extra_models = config.write_relate_config(
        model_repo=ensemble_model_uri,
        template_model_name=model_names["template_transform_model_name"].local_name,
        model_name=model_names["transform_model_name"].local_name,
        model_display_name=transform.displayName,
        template_ensemble_name=model_names["template_ensemble_name"].local_name,
        ensemble_name=model_names["ensemble_name"].local_name,
        template_ensemble_version=str(ensemble.version),
        is_new_ensemble_model=is_new_ensemble_model,
        sub_models=origin_sub_models,
        extra_models=origin_extra_models,
        is_update_labels=is_new_ensemble_model and (args.scene is None or args.scene == ""))
    bcelogger.info(f"modify sub models: {modify_sub_models} extra models: {modify_extra_models}")

    # 6. 解析指定的sub models 和 extra models
    sub_extra_models = args.sub_extra_models.strip(" ").split(",") \
        if args.sub_extra_models is not None and len(args.sub_extra_models) > 0 else []
    bcelogger.info(f"package sub and extra models: {sub_extra_models}")

    new_sub_models = copy.deepcopy(origin_sub_models)
    transform_is_sub_model = new_sub_models.pop(model_names["template_transform_model_name"].local_name, "")
    new_extra_models = copy.deepcopy(origin_extra_models)
    transform_is_extra_model = new_extra_models.pop(model_names["template_transform_model_name"].local_name, "")

    sub_extra_models.append(transform_model_name)
    for name in sub_extra_models:
        artifact_name = parse_artifact_name(name=name)
        model_name = parse_model_name(name=artifact_name.object_name)
        if model_name.local_name in new_sub_models or str(transform_is_sub_model) != "":
            new_sub_models[model_name.local_name] = str(artifact_name.version)
        if model_name.local_name in new_extra_models or str(transform_is_extra_model) != "":
            new_extra_models[model_name.local_name] = str(artifact_name.version)

    # 7. 创建需要上传的模型
    modify_models = {model_names["template_transform_model_name"].local_name:
                         (model_names["transform_model_name"].local_name, -1)}
    modify_sub_models.update(modify_extra_models)
    model_index: int = 1
    for name, version in modify_sub_models.items():
        local_name, version = create_model(
            windmill_client=windmill_client,
            tracker_client=tracker_client,
            model_uri=ensemble_model_uri,
            model_name=name,
            model_version=version,
            workspace_id=model_names["ensemble_name"].workspace_id,
            template_workspace_id=model_names["template_ensemble_name"].workspace_id,
            model_store_name=model_names["ensemble_name"].model_store_name,
            template_model_store_name=model_names["template_ensemble_name"].model_store_name,
            transform_model_name=model_names["transform_model_name"].local_name,
            transform_model_display_name=transform.displayName,
            scene=args.scene,
            accelerator=args.accelerator,
            model_index=model_index)
        model_index += 1
        modify_models[name] = (local_name, -1)
        if name in new_sub_models:
            new_sub_models.pop(name)
            new_sub_models[local_name] = str(version)
        if name in new_extra_models:
            new_extra_models.pop(name)
            new_extra_models[local_name] = str(version)

    # 7. 修改 ensemble 配置文件
    config.write_ensemble_config(model_repo=ensemble_model_uri,
                                 sub_models=origin_sub_models,
                                 extra_models=origin_extra_models,
                                 ensemble_name=model_names["template_ensemble_name"].local_name,
                                 ensemble_version=str(ensemble.version),
                                 model_name_pairs=modify_models)

    # 9. 上传 ensemble 模型
    ensemble_model_uri = os.path.join(ensemble_model_uri,
                                      model_names["template_ensemble_name"].local_name,
                                      str(ensemble.version))
    bcelogger.info(f"create ensemble sub models: {new_sub_models} and extra models: {new_extra_models}")
    config.metadata = {"subModels": new_sub_models,
                       "extraModels": new_extra_models,
                       "experimentName": tracker_client.experiment_name,
                       "jobName": tracker_client.job_name,
                       "experimentRunID": tracker_client.run_id}
    artifact_tags = {"model_type": "model"}

    response = windmill_client.get_model(workspace_id=model_names["template_ensemble_name"].workspace_id,
                                         model_store_name=model_names["template_ensemble_name"].model_store_name,
                                         local_name=model_names["template_ensemble_name"].local_name)
    prefer_model_server_parameters = response.preferModelServerParameters
    prefer_model_server_parameters["resource"]["accelerator"] = args.accelerator
    tags = response.artifact["tags"] if response.artifact["tags"] is not None else {}
    tags.pop("sourceVersion", None)
    artifact_tags.update(tags)
    bcelogger.info(f"prefer model server parameters: {prefer_model_server_parameters}")
    bcelogger.info(f"artifact tags: {artifact_tags}")
    bcelogger.info(f'model category is: {response.category["category"]}')

    response = windmill_client.create_model(
        workspace_id=model_names["ensemble_name"].workspace_id,
        model_store_name=model_names["ensemble_name"].model_store_name,
        local_name=model_names["ensemble_name"].local_name,
        display_name=args.ensemble_model_display_name,
        prefer_model_server_parameters=prefer_model_server_parameters,
        category=response.category["category"],
        model_formats=response.modelFormats,
        artifact_tags=artifact_tags,
        artifact_metadata=config.metadata,
        artifact_uri=ensemble_model_uri)
    bcelogger.info(f"Model {model_names['ensemble_name'].local_name} created response: {response}")

    # 10. 输出文件
    write_file(obj=json.loads(response.raw_data)["artifact"], output_dir=args.output_model_uri)

    # 11. 更新job tags
    model_name = response.artifact["name"]
    job_name = parse_job_name(tracker_client.job_name)
    response = windmill_client.get_job(workspace_id=job_name.workspace_id,
                                       project_name=job_name.project_name,
                                       local_name=job_name.local_name)
    
    bcelogger.info(f"Get job {tracker_client.job_name} response: {response}")
    tags = response.tags if response.tags is not None else {}
    tags.update({"modelName": model_name})
    bcelogger.info(f"Get job {tracker_client.job_name} tags: {tags}")
    for _ in range(5):
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        response = windmill_client.get_job(workspace_id=job_name.workspace_id,
                                           project_name=job_name.project_name,
                                           local_name=job_name.local_name)
        update_tags = response.tags if response.tags is not None else {}
        bcelogger.info(f"Update job {tracker_client.job_name} tags: {update_tags}")
        if "modelName" in update_tags:
            break
        time.sleep(3)
    bcelogger.info(f"Update job {tracker_client.job_name} tags: {tags}")


if __name__ == "__main__":
    args = parse_args()
    package(args=args)
