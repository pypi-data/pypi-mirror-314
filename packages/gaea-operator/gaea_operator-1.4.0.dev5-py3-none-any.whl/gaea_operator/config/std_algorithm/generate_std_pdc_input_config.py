# -*- coding: utf-8 -*-
"""
本模块自动生成 std pdc 产线的三个配置文件
1. 对数据集的标签描述文件 (label_description.yaml) 中的任务按照指定顺序进行排列
2. 根据任务的标签描述文件生成对应的评测配置文件 (eval_config.yaml)
3. 自动生成 input_config.yaml 文件

Authors: liubo41(liubo41@baidu.com)
Date:    2024/06/19 16:45:00
"""

import argparse
import os
import yaml
import json
import base64

import bcelogger
from bcelogger.base_logger import setup_logger
# from windmillclient.client.windmill_client import WindmillClient
from gaea_operator.utils import is_base64

def parse_args():
    """
    外部输出参数解析
    """

    parser = argparse.ArgumentParser(description="you should add those parameter")
    parser.add_argument("--windmill-ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill-sk", type=str, default=os.environ.get("WINDMILL_SK"))
    parser.add_argument("--org-id", type=str, default=os.environ.get("ORG_ID"))
    parser.add_argument("--user-id", type=str, default=os.environ.get("USER_ID"))
    parser.add_argument("--windmill-endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument('--dataset_name', required=True, help="windmill dataset name")
    parser.add_argument('--advanced_parameters', type=str, default="", help="batch_size")
    parser.add_argument('--output_root', required=True, help="output root")
    parser.add_argument("--output_uri", type=str, default=os.environ.get("OUTPUT_URI"))

    args = parser.parse_args()

    return args

def load_config(file_path):
    """
    加载 yaml 文件

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: 加载好的 yaml 文件. 加载失败时返回为 None
    """

    assert os.path.exists(file_path), "{} does not exist.".format(file_path)

    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except:
        bcelogger.error("Failed to read {}".format(file_path))
        return None


def generate_detection_task(class_num, data_preprocess, preprocess=None):
    """
    生成检测任务

    Args:
        class_num (int): 类别数
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    # 如果没有指定预处理器，则使用默认的标准预处理器
    preprocess = 'CommonGtBoxPreprocess' if preprocess is None else preprocess

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': ['gt_bbox', 'gt_class'],
        'num_classes': [-4, class_num],
        'sample_prob': [0, 1],
        'sample_type': ['', 'class'],
        'min_image_num': [1, 1]
    }

    data_preprocess.append({'obj_box': task_config})


def generate_sample_id_task(class_num, anno_key, data_preprocess, preprocess):
    """
    生成目标检测的采样任务

    Args:
        class_num (int): 类别数
        anno_key (str): 标签的 key
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': [anno_key],
        'num_classes': [class_num + 1],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'sample_id': task_config})


def generate_image_classification_task(class_num, anno_key, data_preprocess, preprocess):
    """
    生成全图分类任务

    Args:
        class_num (int): 类别数
        anno_key (str): 标签的 key
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    preprocess = 'none' if preprocess is None else preprocess

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': [anno_key],
        'num_classes': [class_num],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'img_{}'.format(anno_key): task_config})


def generate_obj_classification_task(class_num, anno_key, data_preprocess, preprocess):
    """
    生成目标分类任务

    Args:
        class_num (int): 类别数
        anno_key (str): 标签的 key
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    preprocess = 'none' if preprocess is None else preprocess

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': [anno_key],
        'num_classes': [class_num],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'obj_{}'.format(anno_key): task_config})


def generate_obj_regression_task(class_num, anno_key, data_preprocess, preprocess):
    """
    生成目标回归任务

    Args:
        class_num (int): 类别数
        anno_key (str): 标签的 key
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    preprocess = 'none' if preprocess is None else preprocess

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': [anno_key],
        'num_classes': [-1],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'obj_{}'.format(anno_key): task_config})


def generate_empty_sample_task(detection_class_num, data_preprocess):
    """
    生成空图采样任务

    Args:
        detection_class_num (int): 检测任务的类别数
        data_preprocess (list(dict)): 已有的任务
    """

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': 'CommonEmptySamplePreprocess',
        'anno_key': ['class_with_empty'],
        'num_classes': [detection_class_num + 1],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'sample_id': task_config})


def generate_semantic_segmentation_task(class_num, anno_key, data_preprocess, preprocess):
    """
    生成语义分割任务

    Args:
        class_num (int): 类别数
        anno_key (str): 标签的 key
        task_type (str): 任务类型
        data_preprocess (list(dict)): 已有的任务
        preprocess (str): 预处理器名称
    """

    preprocess = 'none' if preprocess is None else preprocess

    task_config = {
        'weights': 1.0,
        'ignore_transform_ops': [],
        'preprocess': preprocess,
        'anno_key': [anno_key],
        'num_classes': [class_num],
        'sample_prob': [1],
        'sample_type': ['class'],
        'min_image_num': [1]
    }

    data_preprocess.append({'seg_attr': task_config})


def generate_task(label_description, supported_tasks):
    """
    根据 label_description 自动生成任务配置
    
    单任务有以下参数需要进行配置
    - obj_box:
        weights: 1.0                         # 默认不修改
        ignore_transform_ops: []             # 默认不修改
        preprocess: XXXXX                    # 根据 label_description 生成
        anno_key: [gt_bbox, gt_class]        # 根据 label_description 生成
        num_classes: [-4, 16]                # 根据 label_description 生成
        sample_prob: [0, 1]                  # 按任务进行均衡采样
        sample_type: ['', 'class']           # 默认 class 采样
        min_image_num: [1, 1]                # 默认不修改

    Args:
        label_description (dict): 已经加载好的标签描述文件
        supported_tasks (list): 当前 base 都支持哪些任务

    Returns:
        data_preprocess (dict): 生成的任务配置
    """

    data_preprocess = []

    # 逐任务生成
    all_task_types = set()
    detection_class_num = 0
    detection_task_index = 0
    detection_input_preprocess = None

    for index, task in enumerate(label_description['tasks']):

        # 获取任务参数
        task_type = task['task_type']
        anno_key = task['anno_key']
        class_num = len(task['categories'])
        preprocess = task.get('preprocess', None)

        all_task_types.add(task_type)

        # 按照 task_type 生成任务配置参数
        if task_type == 'detection':
            detection_class_num = class_num
            detection_task_index = index
            detection_input_preprocess = preprocess
            generate_detection_task(class_num, data_preprocess, preprocess)
        elif task_type == 'sample_id':
            generate_sample_id_task(class_num, anno_key, data_preprocess, preprocess)
        elif task_type == 'image_classification':
            generate_image_classification_task(
                class_num, anno_key, data_preprocess, preprocess)
        elif task_type == 'obj_classification':
            generate_obj_classification_task(
                class_num, anno_key, data_preprocess, preprocess)
        elif task_type == 'obj_regression':
            generate_obj_regression_task(
                class_num, anno_key, data_preprocess, preprocess)
        elif task_type == 'semantic_segmentation':
            generate_semantic_segmentation_task(
                class_num, anno_key, data_preprocess, preprocess)
        else:
            bcelogger.warning('{} is not supproted.'.format(task_type))

    # 如果存在检测任务 且 这个任务没有预先指定预处理算子 且 该任务没有指定采样算子，则配置空图采样任务
    if 'detection' in all_task_types and detection_input_preprocess is None and 'sample_id' not in all_task_types:
        # 生成空图采样任务
        generate_empty_sample_task(detection_class_num, data_preprocess)

        # 将原有的检测采样概率置为 0
        data_preprocess[detection_task_index]['obj_box']['sample_prob'][1] = 0
        data_preprocess[detection_task_index]['obj_box']['sample_type'][1] = ''
    # else pass

    # 将所有任务的 sample_prob 进行归一化
    sample_prob_sum = 0
    for task in data_preprocess:
        task_name = list(task.keys())[0]
        task_config = task[task_name]
        sample_prob_sum += sum([x for x in task_config['sample_prob']])
    for task in data_preprocess:
        task_name = list(task.keys())[0]
        task_config = task[task_name]
        task_config['sample_prob'] = [x / sample_prob_sum for x in task_config['sample_prob']]

    return data_preprocess


def generate_hyperparameters(batch_size, learning_rate, epochs, advanced_parameters):
    """
    生成训练超参

    Args:
        batch_size (int): 用户指定的 batch_size
        learning_rate (float): 用户指定的 learning_rate
        epochs (int): 用户指定的 epochs
        advanced_parameters: 参数
    Returns:
        hyperparameters (dict): 生成的超参
    """

    if batch_size < 0 and learning_rate < 0:
        auto = True
        batch_size = 'none'
        lr = 'none'
    else:
        auto = False
        batch_size = int(advanced_parameters["TrainReader.batch_size"])
        lr = float(advanced_parameters["LearningRate.base_lr"])

    epochs = epochs if epochs > 0 else 'none'
    eval_size = advanced_parameters["eval_size"]
    hyperparameters = {'auto': auto, 'batch_size': batch_size, 'lr': lr, 'epochs': epochs, 'eval_size': eval_size}

    return hyperparameters


def get_base_and_pretrain(input_base, generate_config):
    """
    获取 base 和预训练模型

    Args:
        input_base (str): 产线输入指定的 base 
        generate_config (dict): 生成器所需的配置信息
    
    Returns:
        base (str): 根据 input_base 匹配到的 base，未找到返回 None
        pretrained_model (str): 根据 input_base 匹配到的预训练模型，未找到返回 None
    """

    base = generate_config['base_and_pretrain'][input_base]['base']
    pretrained_model = generate_config['base_and_pretrain'][input_base]['pretrained_model']

    return base, pretrained_model


def label_description_reorder(input_base, label_description, generate_config):
    """
    按照 generate_std_pdc_input_config.yaml 中 supported_tasks 配置的顺序重新排序

    Args:
        input_base (str): 产线输入指定的 base 
        label_description (dict): 已经加载好的标签描述文件
        generate_config (dict): 生成器所需的配置信息
    
    Returns:
        reordered_label_description (dict): 重新排序后的标签描述文件

    """

    reordered_label_description = {'tasks': []}
    supported_task_types = generate_config['base_and_pretrain'][input_base].get('supported_tasks', [])
    for supported_task_type in supported_task_types:
        for task in label_description['tasks']:
            if task['task_type'] == supported_task_type:
                reordered_label_description['tasks'].append(task)

    return reordered_label_description


def check_label_description(input_base, generate_config, label_description):
    """
    检查 label_description 与 base 是否匹配

    Args:
        input_base (str): 产线输入指定的 base 
        generate_config (dict): input_config 生成程序本身需要的一些参数
        label_description (dict): 已经加载好的标签描述文件
    
    Reutrns:
        ret (int): 0 表示成功，-1 表示失败
    """

    # 检查 input_base 是否存在于配置文件中
    if input_base not in generate_config['base_and_pretrain']:
        bcelogger.error('base 不存在于配置文件中\n您的 base 为 {}\n支持的 base 有: {}'.format(
            input_base, generate_config['base_and_pretrain'].keys()))
        return False
    # else pass

    # # 检查 label_description 与 base 是否匹配
    # supported_tasks = generate_config['base_and_pretrain'][input_base].get('supported_tasks', [])
    # for task in label_description['tasks']:
    #     task_type = task['task_type']
    #     if task_type not in supported_tasks:
    #         bcelogger.error("task_type {} is not supported by base {}".format(task_type, input_base))
    #         return False
    #     # else pass

    return True


def generate_eval_config(label_description):
    """
    根据任务的标签描述文件生成对应的评测配置文件 (eval_config.yaml)

    Args:
        label_description (dict): 已经加载好的标签描述文件

    Returns:
        eval_config (dict): 生成的评测配置文件
    """

    eval_config = {'NAME_MAP': {}, 'ID_MAP': {}, 'NO_PR_TASK': []}

    for task in label_description['tasks']:
        anno_key = task['anno_key']
        label_reflection = list(task['categories'].values())
        eval_config['NAME_MAP']['img_{}'.format(anno_key)] = label_reflection

    return eval_config


def generate_input_config(advanced_parameters, generate_config, label_description, input_config):
    """
    生成 input_config.yaml 文件

    Args:
        advanced_parameters: 产线界面配置的参数
        generate_config (dict): input_config 生成程序本身需要的一些参数
        label_description (dict): 已经加载好的标签描述文件
        input_config (dict): input_config 的模板
    """

    model_type = advanced_parameters["networkArchitecture"]

    ## 1. 任务名称
    paddle_framework = generate_config['base_and_pretrain'][model_type]['paddle_framework']
    task_name = paddle_framework + '_task'
    ## 2. 训练数据默认为空，等待产线自动填写，无需处理

    ## 3. 训练的模板和预训练权重，由外部指定 base 并关联到唯一预训练权重
    base, pretrained_model = get_base_and_pretrain(model_type, generate_config)

    ## 4. 根据 label_description 自动生成任务配置
    supported_tasks = generate_config['base_and_pretrain'][model_type].get('supported_tasks', [])
    # data_preprocess = generate_task(label_description, supported_tasks)

    ## 5. 数据增强策略，std pdc 产线预先定义，无需处理

    ## 6. 设置训练超参
    if "workerNum" in advanced_parameters:
        advanced_parameters['worker_num'] = advanced_parameters["workerNum"]
    if "batchSize" in advanced_parameters:
        advanced_parameters['TrainReader.batch_size'] = advanced_parameters["batchSize"]
    if "evalSize" in advanced_parameters:
        advanced_parameters['eval_size'] = advanced_parameters["evalSize"]
    hyperparameters = generate_hyperparameters(int(advanced_parameters["TrainReader.batch_size"]),
                                               float(advanced_parameters["LearningRate.base_lr"]),
                                               int(advanced_parameters["epoch"]), advanced_parameters)

    ## 7. 设置训练显卡, 默认使用所有可用显卡
    CUDA_VISIBLE_DEVICES = []

    # 修改 input_config
    input_config['task_name'] = task_name
    input_config['base'] = base
    input_config['pretrained_model'] = pretrained_model
    # input_config['data_preprocess'] = data_preprocess
    input_config['supported_tasks'] = supported_tasks
    input_config['hyperparameters'] = hyperparameters
    input_config['CUDA_VISIBLE_DEVICES'] = CUDA_VISIBLE_DEVICES
    input_config['model_name'] = generate_config['base_and_pretrain'][model_type].get(
            'model_name', 'StandardizeModel2')


def main(args):
    """
    The main entry point for the script.
    input_config 中一共分为 9 个部分，分别对每个部分进行处理
    """
    setup_logger(config=dict(file_name=os.path.join(args.output_uri, "worker.log")))

    # parse epoch, learning rate, batch size and base model
    try:
        if is_base64(args.advanced_parameters):
            advanced_parameters = json.loads(base64.b64decode(args.advanced_parameters))
        else:
            advanced_parameters = json.loads(args.advanced_parameters)
    except json.JSONDecodeError as e:
        bcelogger.error("invalid parameters: {}".format(args.advanced_parameters))
        raise ValueError(f"Advanced parameters decode error：{str(e)}")

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    # 加载一些参数文件
    ## 加载 input_config 生成程序本身需要的一些参数
    generate_config_file = os.path.join(script_dir, "template/generate_std_pdc_input_config.yaml")
    generate_config = load_config(generate_config_file)
    assert generate_config is not None, "Failed to load generate_std_pdc_input_config.yaml"

    ## 加载 input_config 的模板
    input_config_file = os.path.join(script_dir, "template/template_input_config.yaml")
    input_config = load_config(input_config_file)
    assert input_config is not None, "Failed to load template_input_config.yaml"

    ## 检测 label_description 与 base 是否匹配
    check_ret = check_label_description(advanced_parameters["networkArchitecture"], 
                                        generate_config, None)
    assert check_ret, "Failed to check {}".format(advanced_parameters["networkArchitecture"])

    # 功能3: 自动生成 input_config.yaml 文件
    generate_input_config(advanced_parameters, generate_config, None, input_config)
    input_config['output_root_dir'] = args.output_uri

    # 保存 input_config
    config_path = "/root"
    output_path = os.path.join(config_path, 'input_config.yaml')
    with open(output_path, 'w') as f:
        yaml.dump(input_config, f, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    args = parse_args()
    main(args)
