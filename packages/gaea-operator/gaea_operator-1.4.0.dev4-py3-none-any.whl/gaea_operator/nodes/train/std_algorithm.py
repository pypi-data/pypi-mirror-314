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
import shutil
from gaea_tracker import ExperimentTracker
from bcelogger.base_logger import setup_logger
from windmillmodelv1.client.model_api_model import parse_model_name
from windmillmodelv1.client.model_api_model import ModelName
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillmodelv1.client.model_api_model import ModelMetadata
from windmillclient.client.windmill_client import WindmillClient
import bcelogger
from gaea_operator.utils import find_upper_level_folder

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
from gaea_operator.metric import get_score_from_file, update_metric_file_with_dataset
from gaea_operator.utils import write_file
from gaea_operator.utils import NX_METRIC_MAP, NX_CATEGORY_MAP, _retrive_path, _copy_annotation_file_2_backup_path, \
    get_annotation_type, _modify_annotation, pre_listdir_folders, generate_label_description, rle_to_polygon, \
    NX_ANNOTATION_TYPE_CLS, NX_ANNOTATION_TYPE_INSTANCE_SEG

from gaea_operator.config import generate_task
from gaea_operator.dataset import CocoDataset, MultiAttributeDataset

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
                        default=os.environ.get("PUBLIC_MODEL_STORE", "workspaces/public/modelstores/default"))
    parser.add_argument("--tracking-uri", type=str, default=os.environ.get("TRACKING_URI"))
    parser.add_argument("--experiment-name", type=str, default=os.environ.get("EXPERIMENT_NAME"))
    parser.add_argument("--experiment-kind", type=str, default=os.environ.get("EXPERIMENT_KIND"))
    parser.add_argument("--train-dataset-name",
                        type=str,
                        default=os.environ.get("TRAIN_DATASET_NAME"))
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

    parser.add_argument("--output-model-uri", type=str, default=os.environ.get("OUTPUT_MODEL_URI"))
    parser.add_argument("--output-uri", type=str, default=os.environ.get("OUTPUT_URI"))
    parser.add_argument("--train_config_params_uri", type=str, default=os.environ.get("TRAIN_CONFIG_PARAMS_URI"))

    args, _ = parser.parse_known_args()

    return args


def check_columns_whether_all_no_labeled(filename):
    """
    检查多属性分类数据集的每一列是否全为 -1。如果有任何一列全为 -1，则抛出异常。
    """
    data = []
    # 从文件中读取每一行，并提取标签数据
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            # 提取行中的数值部分并转换为整数列表
            values = line.strip().split()[1:]  # 忽略文件名部分
            
            values = [int(value) for value in values]
            data.append(values)

    # 将数据转置，使每一列变成一行，便于逐行检查
    transposed_data = list(zip(*data))

    # 检查每一列是否全为 -1
    for col_idx, col in enumerate(transposed_data):
        if all(value == -1 for value in col):
            raise ValueError(f"Error: Column {col_idx} contains only -1 values.")
        else:
            # print(f"Column {col_idx} has valid values.")
            pass

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
    
    response = windmill_client.get_artifact(name=args.train_dataset_name)
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
    
    # 读取 v2x config YAML 文件
    input_config_file = "/root/train_code/v2x_model_standardization/configs/input_config.yaml"
    bcelogger.info(f"------input_config_file------: {input_config_file}")

    with open(input_config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    model_name = config.get('model_name', 'StandardizeModel2')

    # 获取目前全部参与训练图片所在文件夹的路径
    label_description_path = None
    all_image_folders = set()

    dataset_uri = "/home/windmill/tmp/dataset"
    if not os.path.exists(dataset_uri):
        os.makedirs(dataset_uri, exist_ok=True)

    tmp_dataset_path = '/root/annotations'
    if not os.path.exists(tmp_dataset_path):
        os.makedirs(tmp_dataset_path)

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
            os.system(f'cp {label_description_path} {dataset_uri}')
        else:
            bcelogger.info('do NOT find label description file name, need generate')
            anno_path = train_val_annotation_files[KEY_TRAIN]
            anno_path = anno_path if isinstance(anno_path, str) else anno_path[0]
            label_description_path = generate_label_description(model_name, anno_path, dataset_uri)
    
    with open(label_description_path, 'r') as f:
        label_description = yaml.safe_load(f)

    # 通过 os.listdir() 预先缓存所有文件夹，避免后续的 os.listdir() 耗时
    pre_listdir_folders(all_image_folders)

    # 获取标签类型
    annotation_type = get_annotation_type(label_description_path)

    std_dataset = None
    if annotation_type == NX_ANNOTATION_TYPE_CLS:
        std_dataset = MultiAttributeDataset(windmill_client=windmill_client, 
                                                 work_dir=tracker_client.work_dir)
    elif annotation_type == NX_ANNOTATION_TYPE_INSTANCE_SEG:
        std_dataset = CocoDataset(windmill_client=windmill_client,
                               work_dir=tracker_client.work_dir,
                               extra_work_dir=tracker_client.extra_work_dir)
    else:
        bcelogger.error(f'do NOT support dataset-type. {annotation_type}')

    if args.scene is not None and len(args.scene) > 0:
        bcelogger.info(f"Scene: {args.scene}")
        tags = [{"scene": args.scene}]
        response_data = windmill_client.list_model(workspace_id=parse_modelstore_name(
                                                args.public_model_store).workspace_id,
                                              model_store_name=parse_modelstore_name(
                                                  args.public_model_store).local_name,
                                              tags=tags)
        if len(response_data.result) == 0:
            bcelogger.warning(f"No model found with tags: {tags}")
        for model in response_data.result:
            if "baseDatasetName" in model["artifact"]["tags"]:
                args.base_train_dataset_name = model["artifact"]["tags"]["baseDatasetName"]
                args.base_val_dataset_name = model["artifact"]["tags"]["baseDatasetName"]

    # 1. 合并train分片数据集
    std_dataset.concat_dataset(dataset_name=args.train_dataset_name,
                                base_dataset_name=args.base_train_dataset_name,
                                output_dir=dataset_uri,
                                usage=std_dataset.usages[0])

    # 2. 合并val分片数据集
    std_dataset.concat_dataset(dataset_name=args.val_dataset_name,
                                base_dataset_name=args.base_val_dataset_name,
                                output_dir=dataset_uri,
                                usage=std_dataset.usages[1])
    
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

    train_file_path = os.path.join(dataset_uri, std_dataset.usages[0][0])
    val_file_path = os.path.join(dataset_uri, std_dataset.usages[1][0])

    # 如果是多属性分类任务，需要检查训练集和验证集标签的所有列是否标注
    if annotation_type == NX_ANNOTATION_TYPE_CLS:
        check_columns_whether_all_no_labeled(train_file_path)
        check_columns_whether_all_no_labeled(val_file_path)
    elif annotation_type == NX_ANNOTATION_TYPE_INSTANCE_SEG:
        rle_to_polygon(train_file_path)
        rle_to_polygon(val_file_path)


    config['data_load']['label_description'] = os.path.join(dataset_uri, LABEL_DESCRIPTION_NAME)
    config['data_load'][KEY_TRAIN][image_dir_name] = "./"
    config['data_load'][KEY_TRAIN][data_dir_name] = '/'
    config['data_load'][KEY_TRAIN][anno_dir_name] = [train_file_path]
    config['data_load'][KEY_TRAIN][key_sample_prob] = 1

    config['data_load']['eval'][image_dir_name] = "./"
    config['data_load']['eval'][data_dir_name] = '/'
    config['data_load']['eval'][anno_dir_name] = [val_file_path]

    config['data_load']['infer'][image_dir_name] = "none"
    config['data_load']['infer'][data_dir_name] = "none"
    config['data_load']['infer'][anno_dir_name] = "none"

    if not os.path.exists(args.output_model_uri):
        os.makedirs(args.output_model_uri, exist_ok=True)

    config['output_root_dir'] = args.output_model_uri
    with open(input_config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    # 同时将 input_config_file 写入到 output_model_uri，用于后面模型评测
    input_config_path2 = os.path.join(args.output_model_uri, 'input_config.yaml')
    os.system(f'cp {input_config_file} {input_config_path2}')
    bcelogger.info(f'cp {input_config_file} {input_config_path2}')

    bcelogger.info(f"-----input_config_file------:{config}")

    if not os.path.exists(args.output_uri):
        os.makedirs(args.output_uri, exist_ok=True)
    os.system(f'cp {train_file_path} {args.output_uri}')
    os.system(f'cp {val_file_path} {args.output_uri}')

    trainer = Trainer(framework="PaddlePaddle", tracker_client=tracker_client)
    metric_names = NX_METRIC_MAP['metric_names'].get(annotation_type, [])
    trainer.track_model_score(metric_names=metric_names)
    std_alg_log_name = os.path.join(args.output_uri, 'std-algorithm-train.log') 

    for step in [KEY_TRAIN, 'generate_encapsulation_config', 'export']:
        
        command = (f'cd /root/train_code/ && '
                f'python -m v2x_model_standardization --model_name {model_name} --step {step}')
        result = os.system(command)
        
        if result != 0:
            trainer.training_exit_flag = True
            raise ValueError(f"{step} failed, result: {result}")
        else:
            bcelogger.info(f"{step} finished. result: {result}")

    trainer.training_exit_flag = True

    bcelogger.info('standardization-algorithm-train-log file: {}'.format(std_alg_log_name))

    # 5. 更新指标文件
    update_metric_file_with_dataset(dataset_name=args.train_dataset_name,
                                    input_dir=args.output_model_uri,
                                    file_name="metric.json")
    
    # 6. 创建模型
    bcelogger.info(f"------begin to create model------")
    metric_name = NX_METRIC_MAP['metric_name'].get(annotation_type, BOUNDING_BOX_MEAN_AVERAGE_PRECISION_METRIC_NAME)
    if os.path.exists(os.path.join(args.output_model_uri, "metric.json")):
        current_score = get_score_from_file(filepath=os.path.join(args.output_model_uri, "metric.json"),
                                        metric_name=metric_name)
    else:
        current_score = 1.0

    best_score, version = Model(windmill_client=windmill_client). \
        get_best_model_score(model_name=args.model_name, metric_name=metric_name)
    tags = {metric_name: str(current_score)}
    alias = None
    if current_score >= best_score and version is not None:
        alias = ["best"]
        bcelogger.info(
            f"{metric_name.capitalize()} current score {current_score} >= {best_score}, update [best]")
        tags.update(
            {"bestReason": f"current.score({current_score}) greater than {version}.score({best_score})"})
    if version is None:
        alias = ["best"]
        bcelogger.info(f"First alias [best] score: {current_score}")
        tags.update({"bestReason": f"current.score({current_score})"})

    ## 构造 artifact_metadata
    meta_data = ModelMetadata(
            experimentName=tracker_client.experiment_name,
            jobName=tracker_client.job_name,
            jobDisplayName=tracker_client.job_display_name,
            algorithmParameters=None,
            experimentRunID=tracker_client.run_id)

    model_name = parse_model_name(args.model_name)
    workspace_id = model_name.workspace_id
    model_store_name = model_name.model_store_name
    local_name = model_name.local_name
    response = windmill_client.create_model(workspace_id=workspace_id,
                                            model_store_name=model_store_name,
                                            local_name=local_name,
                                            display_name=args.model_display_name,
                                            category=NX_CATEGORY_MAP[annotation_type],
                                            model_formats=["PaddlePaddle"],
                                            artifact_alias=alias,
                                            artifact_tags=tags,
                                            artifact_metadata=meta_data.dict(),
                                            artifact_uri=args.output_model_uri)
    bcelogger.info(f"Model {args.model_name} created response: {response}")

    # 7. 输出文件
    write_file(obj=json.loads(response.raw_data)["artifact"], output_dir=args.output_model_uri)


if __name__ == "__main__":
    args = parse_args()
    std_algorithm_train(args=args)
