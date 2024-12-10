#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : eval_component.py
"""
import os
from argparse import ArgumentParser
import json
import time

import bcelogger
from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillclient.client.windmill_client import WindmillClient

from ..download_artifact import download_artifact
from gaea_operator.dataset import CocoDataset
from gaea_operator.trainer import Trainer
from gaea_operator.metric import update_metric_file
from gaea_operator.utils import write_file
from gaea_operator.config import PPYOLOEPLUSMConfig


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
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--dataset-name", type=str, default=os.environ.get("DATASET_NAME"))
    parser.add_argument("--model-name", type=str, default=os.environ.get("MODEL_NAME"))
    parser.add_argument("--advanced-parameters",
                        type=str,
                        default=os.environ.get("ADVANCED_PARAMETERS", "{}"))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output-dataset-uri", type=str, default=os.environ.get("OUTPUT_DATASET_URI"))
    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args, _ = parser.parse_known_args()

    return args


def ppyoloe_plus_eval(args):
    """
    Eval component for ppyoloe_plus_m model.
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
    output_model_uri, model_name = download_artifact(windmill_client=windmill_client,
                                                     input_uri=args.input_model_uri,
                                                     artifact_name=args.model_name,
                                                     output_uri=args.output_model_uri,
                                                     is_copy=True)

    # 2. 获取模型信息
    response = windmill_client.get_artifact(name=model_name)
    write_file(obj=json.loads(response.raw_data), output_dir=output_model_uri)

    # 3. 合并分片数据集
    coco_dataset = CocoDataset(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
    coco_dataset.concat_dataset(dataset_name=args.dataset_name,
                                output_dir=args.output_dataset_uri,
                                usage=CocoDataset.usages[1])

    # 4. 生成评估配置文件
    PPYOLOEPLUSMConfig(windmill_client=windmill_client, tracker_client=tracker_client).write_eval_config(
        dataset_uri=args.output_dataset_uri,
        model_uri=output_model_uri)

    # 5. 评估
    trainer = Trainer(framework="PaddlePaddle", tracker_client=tracker_client)
    trainer.track_train_log(output_uri=args.output_uri)
    trainer.launch()

    # 6. 更新指标文件
    update_metric_file(windmill_client=windmill_client,
                       tracker_client=tracker_client,
                       dataset_name=args.dataset_name,
                       model_object_name=response.objectName,
                       model_artifact_name=response.name)

    # 7. 更新job tags
    job_name = parse_job_name(tracker_client.job_name)
    job = windmill_client.get_job(workspace_id=job_name.workspace_id,
                                  project_name=job_name.project_name,
                                  local_name=job_name.local_name)
    tags = job.tags if job.tags is not None else {}
    tags.update({"artifactName": response.name, "datasetName": args.dataset_name})
    bcelogger.info(f"Get job {tracker_client.job_name} tags: {tags}")
    for _ in range(5):
        windmill_client.update_job(workspace_id=job_name.workspace_id,
                                   project_name=job_name.project_name,
                                   local_name=job_name.local_name,
                                   tags=tags)
        job = windmill_client.get_job(workspace_id=job_name.workspace_id,
                                      project_name=job_name.project_name,
                                      local_name=job_name.local_name)
        update_tags = job.tags if job.tags is not None else {}
        bcelogger.info(f"Update job {tracker_client.job_name} tags: {update_tags}")
        if "artifactName" in update_tags:
            break
        time.sleep(3)
    bcelogger.info(f"Update job {tracker_client.job_name} tags: {tags}")


if __name__ == "__main__":
    args = parse_args()
    ppyoloe_plus_eval(args=args)
