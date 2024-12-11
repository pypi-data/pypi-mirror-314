# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
模型转换配置文件生成

Authors: zhouwenlong(zhouwenlong01@baidu.com)
Date:    2024/2/26 10:40
"""
import yaml
import bcelogger
import os
from typing import Dict

FRAMEWORK_LIST = ["onnx", "paddle"]
ACCELERATOR_LIST = ["t4", "v100", "a100", "a800", "a10", "a40", "r200", "atlas310"]

KEY_SOURCE_FRAMEWORK = 'source_framework'
KEY_ACCELERATOR = 'accelerator'
KEY_NETWORK_ARCHITECTURE = 'networkArchitecture'
KEY_EVAL_WIDTH = 'eval_width'
KEY_EVAL_HEIGHT = 'eval_height'
KEY_EVAL_SIZE = 'eval_size'
KEY_IOU_THRESHOLD = 'iou_threshold'
KEY_CONF_THRESHOLD = 'conf_threshold'
KEY_MAX_BOX_NUM = 'max_box_num'
KEY_MAX_BATCH_SIZE = 'max_batch_size'
KEY_PRECISION = 'precision'
KEY_CONTAIN_PREPROCESS = "contain_preprocess"


def save_yaml(yaml_data, yaml_name):
    """
    将字典数据保存为YAML格式的文件。
    
    Args:
        yaml_data (dict): 需要保存的字典数据。
        yaml_name (str): YAML文件名，包含路径。
    
    Returns:
        None; 无返回值，直接写入文件。
    """
    with open(yaml_name, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)


def get_yaml(yaml_name):
    """
    读取指定的YAML文件，返回解析后的字典格式数据。如果YAML文件不存在，则抛出FileNotFoundError异常。
    
    Args:
        yaml_name (str): YAML文件名，包含路径信息。
    
    Returns:
        dict, None: 返回一个字典类型的数据，如果YAML文件内容为空或者无法解析，则返回None。
    
    Raises:
        FileNotFoundError: 当指定的YAML文件不存在时抛出此异常。
    """
    if not os.path.exists(yaml_name):
        raise FileNotFoundError(yaml_name)
    with open(yaml_name, 'r', encoding='utf-8') as f:
        file_data = f.read()

        yaml_data = yaml.load(file_data, Loader=yaml.FullLoader)
        return yaml_data


def gen_input_shape(model_name, width, height, max_batch_size):
    """
    generate input shape 
    """
    batch = -1 if max_batch_size > 1 else 1
    input_shape = {}

    if "ppyoloe" in model_name:
        input_shape = {"image": [batch, 3, height, width], "scale_factor": [batch, 2]}
        if "change" in model_name:
            input_shape["tmp_image"] = [batch, 3, height, width]
    elif "vit-base" in model_name or "resnet" in model_name or 'dbnet' in model_name or 'svtr_lcnet' in model_name:
        input_shape["x"] = [batch, 3, height, width]
    elif "maskformer" in model_name or \
            "ocrnet" in model_name:
        bcelogger.warning("maskformer and ocrnet not support batchsize > 1")
        batch = 1
        input_shape['x'] = [batch, 3, height, width]
        if "change" in model_name:
            input_shape['x'] = [batch, 6, height, width]
    elif "convnext" in model_name or "repvit" in model_name:
        input_shape['raw'] = [batch, 3, height, width]
    elif "codetr" in model_name:
        input_shape['input'] = [1, 3, height, width]
        bcelogger.warning("codetr not support batchsize > 1")
    elif "yoloseg" in model_name:
        input_shape['im_shape'] = [batch, 2]
        input_shape['image'] = [batch, 3, height, width]
        input_shape['scale_factor'] = [batch, 2]
    else:
        raise ValueError("model name not in model list")
    return input_shape


def _trans_shape(input_shape: dict) -> dict:
    """
    trans shape 
    """
    new_input_shape = {}
    for key, value in input_shape.items():
        if len(value) == 4:
            new_input_shape[key] = [value[0], value[2], value[3], value[1]]
        else:
            new_input_shape[key] = list(value)
    return new_input_shape

def _get_yoloseg_kunlun_wh(input_shape):
    """
    获取YOLOseg在KUNLUN平台的输入形状，返回一个列表，包含两个元素，分别是宽和高。如果输入形状中没有'image'键，则返回[0, 0]。
    
    Args:
        input_shape (dict): 字典类型，包含一个或多个键值对，其中键为'image'，值为一个长度为2的列表，第一个元素为宽，第二个元素为高；否则返回[0, 0]。
    
    Returns:
        list, tuple: 一个长度为2的列表或元组，包含宽和高。如果输入形状中没有'image'键，则返回[0, 0]。
    """
    if 'image' in input_shape:
        w = input_shape['image'][-1]
        h = input_shape['image'][-2]
        return [w, h]
    else:
        return [0, 0]

def _generate_yoloseg_kunlun(input_shape: dict) -> dict:
    """
        generate yoloseg for kunlun
    """
    # 1. paddle2onnx
    paddle2onnx_dict = {'type': 'PaddleToOnnx', 'input_shape': input_shape}

    # 2. onnx2onnx
    w, h = _get_yoloseg_kunlun_wh(input_shape)
    onnx2onnx_dict = {'type': 'OnnxToOnnx', 'input_shape': input_shape, 
        'output_nodes': {
            "multiclass_nms3_0.tmp_0": [-1, 6],
            "multiclass_nms3_0.tmp_2": [-1],
            "p2o.Mul.324": [-1, h, w]
        }}

    # 3. onnx2kunlun
    paddle2kunlun_dict = {'type': 'OnnxToKunlun', 'input_shape': input_shape, 
        'device_type': 'r200'}
    
    return [paddle2onnx_dict, onnx2onnx_dict, paddle2kunlun_dict]


def create_common_config(advanced_parameters: dict,
                         input_shape: dict,
                         mean: dict = None,
                         std: dict = None,
                         rename_list: list = None,
                         transpose: bool = False,
                         norm: bool = False,
                         cfg_path: str = ""
                         ):
    """
    create config file for model tranform

    Args:
        input_shape (dict): 输入模型shape，类型为dict，例如{"image":[-1,3,640,640], "scale_factor":[-1,2]}
        cfg_path (str): 生成的转换配置文件保存路径
        rename_list (list, optional): 为onnx模型修改输出名称. 类型为字典列表，
        例如[{concat_1.tmp_0:float32}, {concat_0.tmp_0:int64}], 顺序需要与模型输出顺序一致，数据类型也与模型输出一致。默认为None
        transpose (bool, optional): 为onnx模型添加预处理时，添加transpose操作. 默认为False，不添加
        norm (bool, optional): 为onnx模型添加预处理时，添加norm操作. 默认为False，不添加
    """

    max_batch_size = int(advanced_parameters[KEY_MAX_BATCH_SIZE]) if KEY_MAX_BATCH_SIZE in advanced_parameters else 1

    max_boxes = int(advanced_parameters[KEY_MAX_BOX_NUM]) if KEY_MAX_BOX_NUM in advanced_parameters else None
    conf_thres = float(advanced_parameters[KEY_CONF_THRESHOLD]) if KEY_CONF_THRESHOLD in advanced_parameters else None
    iou_thres = float(advanced_parameters[KEY_IOU_THRESHOLD]) if KEY_IOU_THRESHOLD in advanced_parameters else None
    drop_nms = False

    pipeline_cfg = []

    source_framework = advanced_parameters.get(KEY_SOURCE_FRAMEWORK, "paddle").lower()
    accelerator = advanced_parameters[KEY_ACCELERATOR].split("/")[-1].lower()

    nms_params = None
    onnx_op_flag = False

    if max_boxes is not None and conf_thres is not None and iou_thres is not None:
        nms_params = {"max_boxes": max_boxes,
                      "conf_thres": conf_thres,
                      "iou_thres": iou_thres,
                      "drop_nms": drop_nms}
        bcelogger.info("nms_params: {}".format(nms_params))

    # add OnnxToOnnx
    OnnxToOnnxParam = {}
    if mean is not None or std is not None or rename_list is not None or \
            transpose is not False or norm is not False or nms_params is not None:
        bcelogger.info('use onnx2onnx mode.')
        onnx_op_flag = True
        OnnxToOnnxParam['type'] = 'OnnxToOnnx'
        OnnxToOnnxParam['input_shape'] = input_shape.copy()
        if 'scale_factor' in OnnxToOnnxParam['input_shape']:
            OnnxToOnnxParam['input_shape'].pop('scale_factor')
        if mean is not None and std is not None:
            OnnxToOnnxParam["mean"] = mean
            OnnxToOnnxParam["std"] = std
        if rename_list is not None:
            OnnxToOnnxParam["rename_list"] = rename_list
        OnnxToOnnxParam["transpose"] = transpose
        OnnxToOnnxParam["norm"] = norm
        if nms_params is not None:
            OnnxToOnnxParam["nms_params"] = nms_params

        bcelogger.info("OnnxToOnnxParam = {}".format(OnnxToOnnxParam))

        if advanced_parameters[KEY_NETWORK_ARCHITECTURE] == "dbnet_student":
            OnnxToOnnxParam["rename_list"] = [{'tmp_36': 'float32'}]

    # check args
    if source_framework not in FRAMEWORK_LIST:
        raise ValueError("{} is not supported".format(source_framework))
    if accelerator not in ACCELERATOR_LIST:
        raise ValueError("{} is not supported".format(accelerator))

    model_name = advanced_parameters[KEY_NETWORK_ARCHITECTURE].lower()
    # kunlun 
    if accelerator == "r200":
        OnnxToOnnxParam = {}  # R200 不做预处理内置
        OnnxToKunlunParam = {}
        if source_framework == "paddle":
            if 'yoloseg' in model_name:
                bcelogger.info('meet yoloseg for kunlun')
                pipeline_cfg = _generate_yoloseg_kunlun(input_shape)
            elif 'ppyoloe' not in model_name and 'cvresnet' not in model_name : # 除ppyoloe之外的模型
                PaddleToOnnxParam = {}
                PaddleToOnnxParam["type"] = "PaddleToOnnx"
                PaddleToOnnxParam["input_shape"] = input_shape
                pipeline_cfg.append(PaddleToOnnxParam)

                OnnxToKunlunParam['type'] = 'OnnxToKunlun'
                OnnxToKunlunParam['device_type'] = accelerator
                OnnxToKunlunParam["input_shape"] = input_shape
                if KEY_PRECISION in advanced_parameters and advanced_parameters[KEY_PRECISION] == 'fp16':
                    OnnxToKunlunParam['dtype'] = 'fp16'
                    if 'ocrnet' in model_name:
                        OnnxToKunlunParam['convert_params'] = {
                            "op_precision":
                                {"nn.softmax": "fp32",
                                "nn.general_batch_matmul": "fp32"}}
                    if 'codetr' in model_name:
                        OnnxToKunlunParam['convert_params'] = {
                            "fusion_pattern": ["fuse_add_maskformer", 
                                                "fuse_attention_maskformer", 
                                                "fuse_ms_deform_attn", 
                                                "remove_where"],
                            "op_precision": {"clip": "fp32",
                                            "divide": "fp32",
                                            "log": "fp32",
                                            "sigmoid": "fp32",
                                            "subtract": "fp32"}}
                    if 'maskformer' in model_name:
                        OnnxToKunlunParam['convert_params'] = {
                            "fusion_pattern": ["fuse_add_maskformer", 
                                                "fuse_attention_maskformer"]}
                pipeline_cfg.append(OnnxToKunlunParam)
            else:
                PaddleToKunlunParam = {}
                PaddleToKunlunParam["type"] = "PaddleToKunlun"
                PaddleToKunlunParam['device_type'] = accelerator
                PaddleToKunlunParam["input_shape"] = input_shape
                PaddleToKunlunParam['dtype'] = advanced_parameters[KEY_PRECISION] \
                    if KEY_PRECISION in advanced_parameters else 'fp32'
                # convert_op_list.append(PaddleToKunlunParam)
                pipeline_cfg.append(PaddleToKunlunParam)

        elif source_framework == "onnx":
            OnnxToKunlunParam['type'] = 'OnnxToKunlun'
            OnnxToKunlunParam["input_shape"] = input_shape
            OnnxToKunlunParam['dtype'] = advanced_parameters[KEY_PRECISION] \
                if KEY_PRECISION in advanced_parameters else 'fp32'
            pipeline_cfg.append(OnnxToKunlunParam)

            if onnx_op_flag and len(OnnxToOnnxParam) != 0:
                pipeline_cfg.insert(0, OnnxToOnnxParam)
        else:
            raise NotImplementedError("{} is not supported".format(source_framework))
    elif accelerator == "atlas310":
        PaddleToOnnxParam = {}
        PaddleToOnnxParam["type"] = "PaddleToOnnx"
        PaddleToOnnxParam["input_shape"] = input_shape
        pipeline_cfg.append(PaddleToOnnxParam)

        if 'ppyoloe' in model_name:
            OnnxToOnnxParam = {}
            OnnxToOnnxParam["type"] = "OnnxToOnnx"
            OnnxToOnnxParam["input_shape"] = input_shape
            OnnxToOnnxParam["norm"] = False
            OnnxToOnnxParam["transpose"] = False
            OnnxToOnnxParam["nms_params"] = {"drop_nms": True}
            pipeline_cfg.append(OnnxToOnnxParam)

        OnnxToAscendParam = {}
        OnnxToAscendParam["type"] = "OnnxToAscend"
        OnnxToAscendParam["input_shape"] = input_shape
        if 'ppyoloe' in model_name:
            OnnxToAscendParam["net_name"] = "ppyoloe"
        OnnxToAscendParam["device"] = "Ascend310P3"
        OnnxToAscendParam["precision"] = "fp16"
        pipeline_cfg.append(OnnxToAscendParam)
    elif accelerator in ACCELERATOR_LIST:
        if source_framework == "paddle":
            PaddleToOnnxParam = {}
            PaddleToOnnxParam["type"] = "PaddleToOnnx"
            PaddleToOnnxParam["model_name"] = "model"
            PaddleToOnnxParam["input_shape"] = input_shape
            pipeline_cfg.append(PaddleToOnnxParam)

        if onnx_op_flag:
            pipeline_cfg.append(OnnxToOnnxParam)

        OnnxToTensorrtParam = {}
        min_batch = 1
        opt_batch = max(max_batch_size // 2, 1)
        max_batch = max_batch_size

        OnnxToTensorrtParam["type"] = "OnnxToTensorRT"

        new_input_shape_str = {}
        if len(OnnxToOnnxParam) > 0 and 'transpose' in OnnxToOnnxParam and OnnxToOnnxParam['transpose']:
            new_input_shape = _trans_shape(input_shape)
        else:
            new_input_shape = input_shape

        for name, shape in new_input_shape.items():
            shape[0] = 1
            new_input_shape_str[name] = "x".join(str(x) for x in shape)

        cmd = ""
        for b, param_name in zip([min_batch, opt_batch, max_batch], ["--minShapes", "--optShapes", "--maxShapes"]):
            start_param = f"{param_name}="
            for name, shape in new_input_shape_str.items():
                shape = str(b) + shape[1:]
                start_param += name
                start_param += ":"
                start_param += shape
                start_param += ","
            start_param = start_param[:-1]
            cmd += start_param + " "
        if min_batch == max_batch:
            cmd = f" --workspace=12288"
        else:
            cmd += f" --workspace=12288"
        if KEY_PRECISION not in advanced_parameters or \
                advanced_parameters[KEY_PRECISION].lower() in ["fp32", "float32"]:
            pass
        else:
            if KEY_PRECISION in advanced_parameters:
                cmd += f" --{advanced_parameters[KEY_PRECISION]}"

        if model_name in ['codetr']:
            cmd += f" --staticPlugins=/usr/src/tensorrt/plugins/libmmdeploy_tensorrt_ops.so"
        bcelogger.info(f"OnnxToTensorrt cmd = {cmd}")

        OnnxToTensorrtParam["cmd"] = cmd

        pipeline_cfg.append(OnnxToTensorrtParam)
    # bitmain
    else:
        raise NotImplementedError("{} is not supported".format(accelerator))

    cfg = {}
    cfg['pipeline'] = pipeline_cfg

    dir_name = os.path.dirname(cfg_path)
    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)

    with open(cfg_path, "w") as f:
        yaml.dump(cfg, f, indent=4)


def get_norm_transpose(accelerator, contain_preprocess):
    """
        only nvidia add preproc-operators
    """
    if contain_preprocess == "true":
        return True, True
    else:
        return False, False


def get_mean_std(metadata: Dict, model_name: str):
    """
    get mean/std from meta.yaml
    """
    yaml_data = metadata
    model_input_name = ['x']
    if 'ppyoloe' in model_name:
        model_input_name = ['image']
        if 'change' in model_name:
            model_input_name.append('tmp_image')
    if 'convnext' in model_name or 'repvit' in model_name:
        model_input_name = ['raw']
    if 'codetr' in model_name:
        model_input_name = ['input']

    if 'artifact' in yaml_data and 'metadata' in yaml_data['artifact'] \
            and 'algorithmParameters' in yaml_data['artifact']['metadata']:
        alg_param = yaml_data['artifact']['metadata']['algorithmParameters']
    elif 'algorithmParameters' in yaml_data:
        alg_param = yaml_data['algorithmParameters']
    else:
        return None, None

    if 'mean' in alg_param and 'std' in alg_param:
        mean_dict = {}
        std_dict = {}
        for n in model_input_name:
            if model_name.startswith('change-') and "ocrnet" in model_name:
                mean_dict[n] = eval(alg_param['mean']) + eval(alg_param['mean'])
                std_dict[n] = eval(alg_param['std']) + eval(alg_param['std'])
            else:
                mean_dict[n] = eval(alg_param['mean'])
                std_dict[n] = eval(alg_param['std'])
        return mean_dict, std_dict

    return None, None


def generate_transform_config(advanced_parameters: dict, config_name: str, metadata: Dict):
    """
    Create a config file for the specific model
    """
    model_name = advanced_parameters[KEY_NETWORK_ARCHITECTURE].lower()
    mean, std = get_mean_std(metadata, model_name)
    input_shape = gen_input_shape(model_name, int(advanced_parameters[KEY_EVAL_WIDTH]),
                                  int(advanced_parameters[KEY_EVAL_HEIGHT]),
                                  int(advanced_parameters[KEY_MAX_BATCH_SIZE]))

    bcelogger.info(str(input_shape))

    accelerator = advanced_parameters[KEY_ACCELERATOR].split("/")[-1].lower()
    if accelerator == "r200" or accelerator == "atlas310":
        bcelogger.info(f"Accelerator is {accelerator}, set contain preprocess to false")
        advanced_parameters[KEY_CONTAIN_PREPROCESS] = "false"
    norm, transpose = get_norm_transpose(advanced_parameters[KEY_ACCELERATOR].lower(),
                                         advanced_parameters.get(KEY_CONTAIN_PREPROCESS, "true"))
    bcelogger.info(f"Transform norm = {norm}, transpose = {transpose}")
    bcelogger.info(f"Transform mean = {mean}, std = {std}")

    create_common_config(advanced_parameters,
                         input_shape=input_shape,
                         mean=mean,
                         std=std,
                         norm=norm,
                         transpose=transpose,
                         cfg_path=config_name)


if __name__ == "__main__":
    param = {
        KEY_SOURCE_FRAMEWORK: "paddle",
        KEY_ACCELERATOR: 'r200',
        KEY_NETWORK_ARCHITECTURE: 'change-ocrnet',
        KEY_EVAL_WIDTH: '600',
        KEY_EVAL_HEIGHT: '600',
        KEY_IOU_THRESHOLD: '0.56',
        KEY_CONF_THRESHOLD: '0.12',
        KEY_MAX_BOX_NUM: '24',
        KEY_MAX_BATCH_SIZE: '123',
        KEY_PRECISION: 'fp16'
    }
    generate_transform_config(param, './tran.yaml', {})
