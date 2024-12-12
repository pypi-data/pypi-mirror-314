#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/23
# @Author  : yanxiaodong
# @File    : train_component.py
"""
import os
import json
import yaml
from argparse import ArgumentParser
import time
import shutil

from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillclient.client.windmill_client import WindmillClient
import bcelogger

from gaea_operator.utils import find_upper_level_folder
from gaea_operator.utils import write_file
from gaea_operator.metric.types.metric import LOSS_METRIC_NAME, \
    MAP_METRIC_NAME, \
    AP50_METRIC_NAME, \
    AR_METRIC_NAME, \
    BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME, \
    ACCURACY_METRIC_NAME, \
    CLASSIFICATION_ACCURACY_METRIC_NAME, \
    SEG_MAP_METRIC_NAME, \
    SEG_AP50_METRIC_NAME, \
    SEG_AR_METRIC_NAME
from gaea_operator.trainer import Trainer
from gaea_operator.model import Model
from gaea_operator.metric import update_metric_file
from gaea_operator.utils import NX_METRIC_MAP, _retrive_path, _copy_annotation_file_2_backup_path, \
    get_annotation_type, _modify_annotation, pre_listdir_folders, rle_to_polygon, \
    NX_ANNOTATION_TYPE_CLS, NX_ANNOTATION_TYPE_INSTANCE_SEG, generate_label_description
from gaea_operator.config import generate_task
from gaea_operator.dataset import CocoDataset, MultiAttributeDataset
from gaea_operator.nodes.download_artifact import download_artifact

LABEL_DESCRIPTION_NAME = 'label_description.yaml'
KEY_ANNOTATION = 'annotation'
KEY_TRAIN = 'train'
KEY_VAL = 'val'


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
                        default=os.environ.get("PUBLIC_MODEL_STORE", "workspaces/public/modelstores/public"))
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--dataset-name",
                        type=str,
                        default=os.environ.get("DATASET_NAME"))
    parser.add_argument("--val-dataset-name", type=str, default=os.environ.get("VAL_DATASET_NAME"))
    parser.add_argument("--base-train-dataset-name",
                        type=str,
                        default=os.environ.get("BASE_TRAIN_DATASET_NAME"))
    parser.add_argument("--base-val-dataset-name", type=str, default=os.environ.get("BASE_VAL_DATASET_NAME"))
    parser.add_argument("--model-name", type=str, default=os.environ.get("MODEL_NAME"))
    parser.add_argument("--model-display-name",
                        type=str,
                        default=os.environ.get("MODEL_DISPLAY_NAME"))
    parser.add_argument("--advanced-parameters",
                        type=str,
                        default=os.environ.get("ADVANCED_PARAMETERS", "{}"))

    parser.add_argument("--input-model-uri", type=str, default=os.environ.get("INPUT_MODEL_URI"))
    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-dataset-uri", type=str, default=os.environ.get("OUTPUT_DATASET_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))
    parser.add_argument("--train_config_params_uri", type=str, default=os.environ.get("TRAIN_CONFIG_PARAMS_URI"))

    args, _ = parser.parse_known_args()

    return args


def std_algorithm_train(args):
    """
    Train component for ppyoloe_plus model.
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
    
    response = windmill_client.get_artifact(name=args.dataset_name)
    filesystem = windmill_client.suggest_first_filesystem(workspace_id=response.workspaceID,
                                                                       guest_name=response.parentName)
    bcelogger.info(f"------filesystem------ : {filesystem}")
    
    base_uri = ''
    for _path in response.metadata["paths"]:
        relative_path = windmill_client.get_path(filesystem, _path)
        base_uri = _path[:_path.index(relative_path)].rstrip('/')
    bcelogger.info(f'base_uri: {base_uri}')
    bcelogger.info(f'tracker_client.work_dir: {tracker_client.work_dir}')

    train_val_annotation_files = {}
    tmp_dataset_path = '/root/annotations'
    if not os.path.exists(tmp_dataset_path):
        os.makedirs(tmp_dataset_path)
    
    # 原来默认存在的input_config.yaml文件并不适用，因此无论是否存在都需要下载后复制
    # if not os.path.exists(input_config_file):
    # 获取模型路径信息以添加input_config.yaml best_model*作为输入
    output_model_uri, artifact_model_name = download_artifact(
        windmill_client=windmill_client,
        input_uri=args.input_model_uri,
        artifact_name=args.model_name,
        output_uri=args.output_model_uri,
        is_copy=True,
    )

    config_file = os.path.join(output_model_uri, "input_config.yaml")
    input_config_file = "/root/train_code/v2x_model_standardization/configs/input_config.yaml"
    try:
        shutil.copyfile(config_file, input_config_file)
        bcelogger.info("Commands 'cp input_config.yaml' executed successfully.")
    except Exception as e:
        bcelogger.error(f"An error occurred in executing 'cp input_config.yaml': {e}")
    
    # 读取 v2x config YAML 文件
    with open(input_config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    model_name = config.get('model_name', 'StandardizeModel2')

    # 获取目前全部参与训练图片所在文件夹的路径
    label_description_path = None
    all_image_folders = set()

    if not os.path.exists(args.output_dataset_uri):
        os.makedirs(args.output_dataset_uri, exist_ok=True)

    for _path in response.metadata["paths"]:
        relative_path = windmill_client.get_path(filesystem, _path)
        local_dataset_path = os.path.join(tracker_client.work_dir, relative_path)
        bcelogger.info(f"-----local_dataset_path----- : {local_dataset_path}")

        prefix = [KEY_TRAIN, KEY_VAL, KEY_ANNOTATION]
        for p in prefix:
            src_names = []
            if not os.path.isfile(local_dataset_path):
                src_names = _retrive_path(local_dataset_path, ['json', 'txt'], p, p)
            else:
                src_names.append(local_dataset_path)
            if len(src_names) <= 0:
                continue
            abs_work_path = find_upper_level_folder(src_names[0], 2) # according to document MUST have annotation-folder
            for src_name in src_names:
                dst_name = _modify_annotation(src_name, tmp_dataset_path, abs_work_path, all_image_folders, 
                                              s3_filesystem_head=base_uri, 
                                              local_filesystem_head=tracker_client.work_dir)
                if p in train_val_annotation_files:
                    train_val_annotation_files[p].append(dst_name)
                else:
                    train_val_annotation_files[p] = [dst_name]
            # check label description file
            if label_description_path is None:
                for name in src_names:
                    label_des_file = os.path.join(os.path.dirname(name), LABEL_DESCRIPTION_NAME)
                    if os.path.exists(label_des_file):
                        label_description_path = label_des_file
                        break
        
        if KEY_ANNOTATION in train_val_annotation_files:
            bcelogger.info('---find annotation label files, set to train & val')
            for k in [KEY_TRAIN, KEY_VAL]:
                if k in train_val_annotation_files:
                    train_val_annotation_files[k].extend(train_val_annotation_files[KEY_ANNOTATION])
                else:
                    train_val_annotation_files[k] = train_val_annotation_files[KEY_ANNOTATION]
            del train_val_annotation_files[KEY_ANNOTATION]

        # 获取 label_description_path
        if label_description_path is not None:
            bcelogger.info('find label description file name: {}'.format(label_description_path))
            os.system(f'cp {label_description_path} {args.output_dataset_uri}')
        else:
            bcelogger.info('do NOT find label description file name, need generate')
            anno_path = train_val_annotation_files[KEY_TRAIN]
            anno_path = anno_path if isinstance(anno_path, str) else anno_path[0]
            label_description_path = generate_label_description(model_name, anno_path, args.output_dataset_uri)

    with open(label_description_path, 'r') as f:
        label_description = yaml.safe_load(f)

    # 通过 os.listdir() 预先缓存所有文件夹，避免后续的 os.listdir() 耗时
    pre_listdir_folders(all_image_folders)

    # 获取标签类型
    annotation_type = get_annotation_type(label_description_path)

    # 3. 合并分片数据集
    std_dataset = None
    if annotation_type == NX_ANNOTATION_TYPE_INSTANCE_SEG:
        std_dataset = CocoDataset(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
        std_dataset.concat_dataset(dataset_name=args.dataset_name,
                                output_dir=args.output_dataset_uri,
                                usage=CocoDataset.usages[1])
    elif annotation_type == NX_ANNOTATION_TYPE_CLS:
        std_dataset = MultiAttributeDataset(windmill_client=windmill_client, work_dir=tracker_client.work_dir)
        std_dataset.concat_dataset(dataset_name=args.dataset_name,
                                    output_dir=args.output_dataset_uri,
                                    usage=MultiAttributeDataset.usages[1],
                                    save_label=True)
    else:
        bcelogger.error(f'do NOT support annotation type: {annotation_type}')

    # 生成 input_confif 的 data_preprocess 字段
    data_preprocess = generate_task(label_description, config['supported_tasks'])
    config['data_preprocess'] = data_preprocess

    # 将 dataset 配置清空，读取实际的 dataset 配置，并填充
    if 'data_load' in config and isinstance(config['data_load'], dict):
        config['data_load'][KEY_TRAIN] = {}
        config['data_load']['eval'] = {}
        config['data_load']['infer'] = {}

    task_name = config['task_name']
    bcelogger.info(f"------task_name is------: {task_name}")

    image_dir_name = "image_dir"
    data_dir_name = "dataset_dir"
    anno_dir_name = "anno_path"
    key_sample_prob = 'sample_prob'

    config['data_load']['label_description'] = os.path.join(args.output_dataset_uri, LABEL_DESCRIPTION_NAME)

    val_file_path = os.path.join(args.output_dataset_uri, std_dataset.usages[1][0])

    if annotation_type == NX_ANNOTATION_TYPE_INSTANCE_SEG:
        rle_to_polygon(val_file_path)

    # 因为本阶段只负责评测，所以将 train, eval, infer 配置都指向同一个文件夹
    config['data_load'][KEY_TRAIN][image_dir_name] = "./"
    config['data_load'][KEY_TRAIN][data_dir_name] = '/'
    config['data_load'][KEY_TRAIN][anno_dir_name] = [val_file_path]
    config['data_load'][KEY_TRAIN][key_sample_prob] = 1

    config['data_load']['eval'][image_dir_name] = "./"
    config['data_load']['eval'][data_dir_name] = '/'
    config['data_load']['eval'][anno_dir_name] = [val_file_path]

    config['data_load']['infer'][image_dir_name] = "./"
    config['data_load']['infer'][data_dir_name] = '/'
    config['data_load']['infer'][anno_dir_name] = [val_file_path]

    if not os.path.exists(args.output_model_uri):
        os.makedirs(args.output_model_uri, exist_ok=True)

    config['output_root_dir'] = args.output_model_uri
    with open(input_config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

    bcelogger.info(f"-----input_config_file------:{config}")
    bcelogger.info(f'output_dataset_uri: {args.output_dataset_uri}')
    
    if not os.path.exists(args.output_uri):
        os.makedirs(args.output_uri, exist_ok=True)    
    os.system(f'cp {val_file_path} {args.output_uri}')

    trainer = Trainer(framework="PaddlePaddle", tracker_client=tracker_client)
    metric_names = NX_METRIC_MAP['metric_names'].get(annotation_type, [])
    trainer.track_model_score(metric_names=metric_names)
    model_name = config.get('model_name', 'StandardizeModel2')
    train_command = (
            f'cd /root/train_code/ && '
            f'python -m v2x_model_standardization --model_name {model_name} --step eval')
    result = os.system(train_command)
    if result != 0:
        trainer.training_exit_flag = True
        raise RuntimeError(f"eval failed: {result}")
    else:
        bcelogger.info(f"eval result: {result}")
    
    trainer.training_exit_flag = True

    # 4. 更新指标文件
    bcelogger.info(f'begin to update metric. model-name: {artifact_model_name} output_model_uri: {output_model_uri}')
    response = windmill_client.get_artifact(name=artifact_model_name)
    write_file(obj=json.loads(response.raw_data), output_dir=output_model_uri)

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

    # try:
    #     if args.icafe_id:
    #         from gaea_operator.components.icafe import icafe
    #         icafe.sync_icafe_eval_end(args)
    # except Exception as e:
    #     bcelogger.error(f"Sync icafe failed args:{args} exception: {e}")


if __name__ == "__main__":
    args = parse_args()
    std_algorithm_train(args=args)
