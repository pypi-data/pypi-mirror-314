#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/10
# @Author  : yanxiaodong
# @File    : std_algorithm_pipeline.py
"""
from typing import List, Dict
from paddleflow.pipeline import Pipeline
from paddleflow.pipeline import CacheOptions
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact
from paddleflow.pipeline import ExtraFS
from paddleflow.pipeline import FailureOptions

from windmillmodelv1.client.model_api_model import Category

from gaea_operator.artifacts import Variable
from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, \
    DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME, \
    ModelTemplate, \
    Accelerator, \
    get_accelerator
from gaea_operator.nodes import Image, Properties, set_node_parameters
from gaea_operator.nodes import Train as BaseTrain
from gaea_operator.nodes import Eval as BaseEval
from gaea_operator.nodes import Transform as BaseTransform
from gaea_operator.nodes import Package as BasePackage
from gaea_operator.nodes import TransformEval as BaseTransformEval
from gaea_operator.nodes import Inference as BaseInference

NAME_TO_IMAGES = {
    BaseTrain.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name=('iregistry.baidu-int.com/windmill-public/train/paddlepaddle:std-alg-138-dev102'))
        ],
    BaseEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name=('iregistry.baidu-int.com/windmill-public/train/paddlepaddle:std-alg-138-dev102'))
        ],
    BaseTransform.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/transform:1.3.5"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/transform:20240822_1724337412559-xmy4")
        ],
    BaseTransformEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.5"),
            Image(kind=Accelerator.KUNLUN,
                  name=('iregistry.baidu-int.com/windmill-public/inference/kunlun:'
                        '20240822_1724337412630-dev2-liubo41-dev3'))
        ],
    BasePackage.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.5"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:20240822_1724337412630-xmy9")
        ],
    BaseInference.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.5"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:20240822_1724337412630-xmy9")
        ]}


@Pipeline(
    name="std_algorithm",
    cache_options=CacheOptions(enable=True, max_expired_time=604800),
    parallelism=6,
    failure_options=FailureOptions(strategy="continue"),
)
def pipeline(accelerator: str = "T4",
             transform_accelerator: str = None,
             transform_eval_accelerator: str = None,
             package_accelerator: str = None,
             inference_accelerator: str = None,
             train_skip: int = -1,
             eval_skip: int = -1,
             transform_skip: int = -1,
             transform_eval_skip: int = -1,
             package_skip: int = -1,
             inference_skip: int = -1,
             eval_inputs: List[Variable] = None,
             transform_inputs: List[Variable] = None,
             transform_eval_inputs: List[Variable] = None,
             package_inputs: List[Variable] = None,
             inference_inputs: List[Variable] = None,
             extra_fs_name: str = "vistudio",
             extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-vistudio",
             windmill_ak: str = "",
             windmill_sk: str = "",
             org_id: str = "",
             user_id: str = "",
             windmill_endpoint: str = "",
             experiment_kind: str = "",
             experiment_name: str = "",
             modelstore_name: str = "",
             tracking_uri: str = "",
             project_name: str = "",
             scene: str = "",
             train_dataset_name: str = "",
             val_dataset_name: str = "",
             base_train_dataset_name: str = "",
             base_val_dataset_name: str = "",
             train_model_name: str = "",
             train_model_display_name: str = "",
             eval_dataset_name: str = "",
             eval_model_name: str = "",
             transform_input_model_name: str = "",
             transform_model_name: str = "",
             transform_model_display_name: str = "",
             transform_eval_input_model_name: str = "",
             transform_advanced_parameters: str = "",
             ensemble_model_name: str = "",
             ensemble_model_display_name: str = "",
             inference_input_model_name: str = ""):
    """
    Pipeline for std_algorithm training eval transform transform-eval package inference.
    """
    base_params = {"flavour": "c4m16gpu1",
                   "queue": "qtrain",
                   "windmill_ak": windmill_ak,
                   "windmill_sk": windmill_sk,
                   "org_id": org_id,
                   "user_id": user_id,
                   "windmill_endpoint": windmill_endpoint,
                   "experiment_name": experiment_name,
                   "experiment_kind": experiment_kind,
                   "tracking_uri": tracking_uri,
                   "project_name": project_name,
                   "model_store_name": modelstore_name,
                   "scene": scene,
                   "role": "false"}
    base_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                "PF_JOB_QUEUE_NAME": "{{queue}}",
                "WINDMILL_AK": "{{windmill_ak}}",
                "WINDMILL_SK": "{{windmill_sk}}",
                "ORG_ID": "{{org_id}}",
                "USER_ID": "{{user_id}}",
                "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                "EXPERIMENT_KIND": "{{experiment_kind}}",
                "EXPERIMENT_NAME": "{{experiment_name}}",
                "TRACKING_URI": "{{tracking_uri}}",
                "PROJECT_NAME": "{{project_name}}",
                "SCENE": "{{scene}}",
                "PIPELINE_ROLE": "windmill"}

    pre_nodes = {}
    if accelerator is None:
        accelerator = Accelerator.T4

    train = Train(train_skip=train_skip)
    train_step = train(base_params=base_params,
                       base_env=base_env,
                       extra_fs_name=extra_fs_name,
                       extra_fs_mount_path=extra_fs_mount_path,
                       train_dataset_name=train_dataset_name,
                       val_dataset_name=val_dataset_name,
                       base_train_dataset_name=base_train_dataset_name,
                       base_val_dataset_name=base_val_dataset_name,
                       train_model_name=train_model_name,
                       train_model_display_name=train_model_display_name)
    pre_nodes[train_step.name] = train_step

    eval = Eval(eval_skip=eval_skip, pre_nodes=pre_nodes)
    eval.inputs = eval_inputs
    eval_step = eval(base_params=base_params,
                     base_env=base_env,
                     eval_dataset_name=eval_dataset_name,
                     eval_model_name=eval_model_name)
    pre_nodes[eval_step.name] = eval_step

    if transform_accelerator is None:
        transform_accelerator = accelerator
    transform = Transform(transform_skip=transform_skip,
                          algorithm="CvResNet/Model",
                          category=Category.CategoryImageClassificationMultiTask.value,
                          accelerator=transform_accelerator,
                          pre_nodes=pre_nodes)
    transform.inputs = transform_inputs
    transform.properties = Properties(images=NAME_TO_IMAGES[transform.name()])
    transform_step = transform(base_params=base_params,
                               base_env=base_env,
                               train_model_name=transform_input_model_name,
                               transform_model_name=transform_model_name,
                               transform_model_display_name=transform_model_display_name,
                               advanced_parameters=transform_advanced_parameters)
    pre_nodes[transform_step.name] = transform_step

    if transform_eval_accelerator is None:
        transform_eval_accelerator = accelerator
    transform_eval = TransformEval(transform_eval_skip=transform_eval_skip,
                                   algorithm="CvResNet/Model",
                                   accelerator=transform_eval_accelerator,
                                   pre_nodes=pre_nodes)
    transform_eval.inputs = transform_eval_inputs
    transform_eval.properties = Properties(images=NAME_TO_IMAGES[transform_eval.name()])
    transform_eval_step = transform_eval(base_params=base_params,
                                         base_env=base_env,
                                         dataset_name=eval_dataset_name,
                                         transform_model_name=transform_eval_input_model_name)
    pre_nodes[transform_eval_step.name] = transform_eval_step

    if package_accelerator is None:
        package_accelerator = accelerator
    package = Package(package_skip=package_skip,
                      algorithm="CvResNet/Model",
                      accelerator=package_accelerator,
                      pre_nodes=pre_nodes)
    package.inputs = package_inputs
    package.properties = Properties(images=NAME_TO_IMAGES[package.name()])
    package_step = package(base_params=base_params,
                           base_env=base_env,
                           transform_model_name=transform_eval_input_model_name,
                           ensemble_model_name=ensemble_model_name,
                           sub_extra_models="",
                           ensemble_model_display_name=ensemble_model_display_name)
    pre_nodes[package_step.name] = package_step

    if inference_accelerator is None:
        inference_accelerator = accelerator
    inference = Inference(inference_skip=inference_skip,
                          accelerator=inference_accelerator,
                          pre_nodes=pre_nodes)
    inference.inputs = inference_inputs
    inference.properties = Properties(images=NAME_TO_IMAGES[inference.name()])
    inference_step = inference(base_params=base_params,
                               base_env=base_env,
                               ensemble_model_name=inference_input_model_name,
                               dataset_name=eval_dataset_name)
    pre_nodes[inference_step.name] = inference_step

    return None


class Train(BaseTrain):
    """
    Train
    """

    def __init__(self, train_skip: int = -1):
        super().__init__(train_skip=train_skip)
        self.properties = Properties(images=NAME_TO_IMAGES[self.name()],
                                     modelFormats={Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]}})

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 extra_fs_name: str = "vistudio",
                 extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-vistudio",
                 train_dataset_name: str = "",
                 val_dataset_name: str = "",
                 base_train_dataset_name: str = "",
                 base_val_dataset_name: str = "",
                 train_model_name: str = "",
                 train_model_display_name: str = ""):
        train_params = {"skip": self.train_skip,
                        "train_dataset_name": train_dataset_name,
                        "val_dataset_name": val_dataset_name,
                        "base_train_dataset_name": base_train_dataset_name,
                        "base_val_dataset_name": base_val_dataset_name,
                        "model_name": train_model_name,
                        "model_display_name": train_model_display_name,
                        "advanced_parameters": '{"epoch":"1",'
                                               '"LearningRate.base_lr":"0.001",'
                                               '"worker_num":"1",'
                                               '"eval_size":"640*640",'
                                               '"TrainReader.batch_size":"8"}'}
        train_env = {"TRAIN_DATASET_NAME": "{{train_dataset_name}}",
                     "VAL_DATASET_NAME": "{{val_dataset_name}}",
                     "BASE_TRAIN_DATASET_NAME": "{{base_train_dataset_name}}",
                     "BASE_VAL_DATASET_NAME": "{{base_val_dataset_name}}",
                     "MODEL_NAME": "{{model_name}}",
                     "MODEL_DISPLAY_NAME": "{{model_display_name}}",
                     "ADVANCED_PARAMETERS": "{{advanced_parameters}}",
                     "PF_EXTRA_WORK_DIR": extra_fs_mount_path}
        train_env.update(base_env)
        train_params.update(base_params)

        train = ContainerStep(
                name=Train.name(),
                docker_env=self.suggest_image(),
                parameters=train_params,
                env=train_env,
                extra_fs=[ExtraFS(name=extra_fs_name, mount_path=extra_fs_mount_path)],
                outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                command=f'cd /root && '
                        f'/usr/bin/python3 -m gaea_operator.config.std_algorithm.generate_std_pdc_input_config '
                        f'--advanced_parameters=$ADVANCED_PARAMETERS '
                        f'--dataset_name=$TRAIN_DATASET_NAME '
                        f'--output_root=$PF_WORK_DIR '
                        f'--output_uri=$PF_OUTPUT_ARTIFACT_OUTPUT_URI && '
                        f'cp /root/input_config.yaml /root/train_code/v2x_model_standardization/configs/ && '
                        f'if [ -e /root/eval_config.yaml ]; then '
                        f'cp /root/eval_config.yaml '
                        f' /root/train_code/v2x_model_standardization/paddle_framework/PaddleCls/tools/task_tools/;'
                        f'fi && '
                        f'export OUTPUT_MODEL_URI=$PF_OUTPUT_ARTIFACT_OUTPUT_MODEL_URI && '
                        f'export OUTPUT_URI=$PF_OUTPUT_ARTIFACT_OUTPUT_URI && '
                        f'/usr/bin/python3 -m gaea_operator.nodes.train.std_algorithm')
        if self.train_skip > 0:
            skip_parameter = "skip"
            train.condition = f"{train.parameters[skip_parameter]} < 0"

        return train


class Eval(BaseEval):
    """
    Eval
    """

    def __init__(self, eval_skip: int = -1, pre_nodes: Dict[str, ContainerStep] = None):
        """
            初始化ContainerStep类的实例。
        
        Args:
            eval_skip (int, optional): 跳过多少个步骤进行评估，默认为-1，表示不跳过任何步骤。 Default: -1.
            pre_nodes (Dict[str, ContainerStep], optional): 前置节点字典，包含每个前置节点的名称和对应的ContainerStep实例。 Default: None.
        
        Returns:
            None.
        """
        super().__init__(eval_skip=eval_skip, pre_nodes=pre_nodes)
        self.properties = Properties(images=NAME_TO_IMAGES[self.name()],
                                     modelFormats={Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]}})

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 eval_dataset_name: str = "",
                 eval_model_name: str = ""):
        eval_params = {"skip": self.eval_skip,
                       "dataset_name": eval_dataset_name,
                       "model_name": eval_model_name,
                       "advanced_parameters": '{"conf_threshold":"0.5",'
                                              '"iou_threshold":"0.5"}'}
        eval_env = {"DATASET_NAME": "{{dataset_name}}",
                    "MODEL_NAME": "{{model_name}}",
                    "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        eval_env.update(base_env)
        eval_params.update(base_params)

        eval = ContainerStep(
                name=Eval.name(),
                docker_env=self.suggest_image(),
                parameters=eval_params,
                env=eval_env,
                outputs={"output_uri": Artifact(),
                        "output_dataset_uri": Artifact(),
                        "output_model_uri": Artifact()},
                # 添加INPUT_MODEL_URI，否则eval无法找到输入的配置文件
                command=f'export INPUT_MODEL_URI=$PF_INPUT_ARTIFACT_INPUT_MODEL_URI && '
                        f'export OUTPUT_MODEL_URI=$PF_OUTPUT_ARTIFACT_OUTPUT_MODEL_URI && '
                        f'export OUTPUT_URI=$PF_OUTPUT_ARTIFACT_OUTPUT_URI && '
                        f'mkdir -p $OUTPUT_MODEL_URI && '
                        # f'cp {{{{input_model_uri}}}}/input_config.yaml '
                        # f'/root/train_code/v2x_model_standardization/configs/ && '
                        # f'cp {{{{input_model_uri}}}}/best_model* $OUTPUT_MODEL_URI && '
                        f'/usr/bin/python3 -m gaea_operator.nodes.eval.std_algorithm '
                        f'--output-dataset-uri={{{{output_dataset_uri}}}} ')

        set_node_parameters(skip=self.eval_skip, step=eval, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return eval

class Transform(BaseTransform):
    """
    Transform
    """
    NAME = "transform"
    DISPLAY_NAME = "模型转换"

    def __init__(self,
                 transform_skip: int = -1,
                 algorithm: str = "",
                 category: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):

        super().__init__(
                transform_skip=transform_skip, 
                algorithm=algorithm, 
                category=category, 
                accelerator=accelerator, 
                pre_nodes=pre_nodes)
        nvidia_accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        ascend_accelerator = get_accelerator(kind=Accelerator.ASCEND)

        self.properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: ["training"] + nvidia_accelerator.suggest_resource_tips(),
                                    Accelerator.KUNLUN: ["training"],
                                    Accelerator.ASCEND: ["training"] + ascend_accelerator.suggest_resource_tips(),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: nvidia_accelerator.suggest_flavour_tips(),
                                    Accelerator.KUNLUN: "c4m16",
                                    Accelerator.ASCEND: ascend_accelerator.suggest_flavour_tips(),
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {f"{self.name()}.train_model_name": ["PaddlePaddle"],
                                                         f"{self.name()}.transform_model_name": ["TensorRT"]},
                                    Accelerator.KUNLUN: {f"{self.name()}.train_model_name": ["PaddlePaddle"],
                                                         f"{self.name()}.transform_model_name": ["PaddleLite"]},
                                    Accelerator.ASCEND: {f"{self.name()}.train_model_name": ["PaddlePaddle"],
                                                         f"{self.name()}.transform_model_name": ["Other"]},
                                })

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 train_model_name: str = "",
                 transform_model_name: str = "",
                 transform_model_display_name: str = "",
                 advanced_parameters: str = ""):
        """
        call
        """
        transform_params = {"skip": self.transform_skip,
                            "train_model_name": train_model_name,
                            "transform_model_name": transform_model_name,
                            "transform_model_display_name": transform_model_display_name,
                            "accelerator": self.properties.accelerator,
                            "advanced_parameters": advanced_parameters}
        transform_env = {"TRAIN_MODEL_NAME": "{{train_model_name}}",
                         "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                         "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                         "ACCELERATOR": "{{accelerator}}",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_env.update(base_env)
        transform_params.update(base_params)

        transform = ContainerStep(name=Transform.name(),
                                  docker_env=self.suggest_image(),
                                  env=transform_env,
                                  parameters=transform_params,
                                  outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                  command=f'cd /workspace/KCVSDK-Ubuntu_x86_64 && source scripts/set_env.sh xpu2 && '
                                          f'cd /root && '
                                          f'python3 -m gaea_operator.nodes.transform.transform '
                                          f'--algorithm={self.algorithm} '
                                          f'--category={self.category} '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}} '
                                          f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.transform_skip, step=transform, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return transform
class TransformEval(BaseTransformEval):
    """
    Transform
    """
    NAME = "transform-eval"
    DISPLAY_NAME = "模型转换评估"

    def __init__(self,
                 transform_eval_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):

        nvidia_accelerator = get_accelerator(kind=Accelerator.NVIDIA)
        kunlun_accelerator = get_accelerator(kind=Accelerator.KUNLUN)
        ascend_accelerator = get_accelerator(kind=Accelerator.ASCEND)

        super().__init__(transform_eval_skip=transform_eval_skip, algorithm=algorithm, 
            accelerator=accelerator, pre_nodes=pre_nodes)

        self.properties = Properties(accelerator=accelerator,
                                computeTips={
                                    Accelerator.NVIDIA: ["training"] + nvidia_accelerator.suggest_resource_tips(),
                                    Accelerator.KUNLUN: ["training"] + kunlun_accelerator.suggest_resource_tips(),
                                    Accelerator.ASCEND: ["training"] + ascend_accelerator.suggest_resource_tips(),
                                },
                                flavourTips={
                                    Accelerator.NVIDIA: nvidia_accelerator.suggest_flavour_tips(),
                                    Accelerator.KUNLUN: kunlun_accelerator.suggest_flavour_tips(),
                                    Accelerator.ASCEND: ascend_accelerator.suggest_flavour_tips(),
                                },
                                modelFormats={
                                    Accelerator.NVIDIA: {f"{self.name()}.model_name": ["TensorRT"]},
                                    Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddleLite"]},
                                    Accelerator.ASCEND: {f"{self.name()}.model_name": ["Other"]},
                                })
        
    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 dataset_name: str = "",
                 transform_model_name: str = ""):
        transform_eval_params = {"skip": self.transform_eval_skip,
                                 "accelerator": self.properties.accelerator,
                                 "dataset_name": dataset_name,
                                 "model_name": transform_model_name,
                                 "advanced_parameters": '{"conf_threshold":"0.5",'
                                                        '"iou_threshold":"0.5"}'}
        transform_eval_env = {"ACCELERATOR": "{{accelerator}}",
                              "DATASET_NAME": "{{dataset_name}}",
                              "MODEL_NAME": "{{model_name}}",
                              "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_eval_params.update(base_params)
        transform_eval_env.update(base_env)
        accelerator = get_accelerator(name=self.properties.accelerator)
        transform_eval_env.update(accelerator.suggest_env())

        transform_eval = ContainerStep(name=TransformEval.name(),
                                       docker_env=self.suggest_image(),
                                       env=transform_eval_env,
                                       parameters=transform_eval_params,
                                       outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                                       command=f'cd /root && '
                                               f'python3 -m gaea_operator.nodes.transform_eval.transform_eval '
                                               f'--algorithm={self.algorithm} '
                                               f'--input-model-uri={{{{input_model_uri}}}} '
                                               f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                               f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                               f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.transform_eval_skip,
                            step=transform_eval,
                            inputs=self.inputs,
                            pre_nodes=self.pre_nodes)

        return transform_eval
class Package(BasePackage):
    """
    Transform
    """
    NAME = "package"
    DISPLAY_NAME = "模型组装"

    def __init__(self,
                 package_skip: int = -1,
                 algorithm: str = "",
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(package_skip=package_skip, algorithm=algorithm, accelerator=accelerator, pre_nodes=pre_nodes)
    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 transform_model_name: str = "",
                 ensemble_model_name: str = "",
                 sub_extra_models: str = "",
                 ensemble_model_display_name: str = ""):
        package_params = {"skip": self.package_skip,
                          "accelerator": self.properties.accelerator,
                          "transform_model_name": transform_model_name,
                          "ensemble_model_name": ensemble_model_name,
                          "sub_extra_models": sub_extra_models,
                          "ensemble_model_display_name": ensemble_model_display_name}
        package_env = {"ACCELERATOR": "{{accelerator}}",
                       "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                       "ENSEMBLE_MODEL_NAME": "{{ensemble_model_name}}",
                       "SUB_EXTRA_MODELS": "{{sub_extra_models}}",
                       "ENSEMBLE_MODEL_DISPLAY_NAME": "{{ensemble_model_display_name}}"}
        package_params.update(base_params)
        package_env.update(base_env)

        package = ContainerStep(name=Package.name(),
                                docker_env=self.suggest_image(),
                                env=package_env,
                                parameters=package_params,
                                outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                command=f'cd /root && '
                                        f'python3 -m gaea_operator.nodes.package.package '
                                        f'--algorithm={self.algorithm} '
                                        f'--input-model-uri={{{{input_model_uri}}}} '
                                        f'--output-uri={{{{output_uri}}}} '
                                        f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.package_skip, step=package, inputs=self.inputs, pre_nodes=self.pre_nodes)


        return package
    
class Inference(BaseInference):
    """
    Transform
    """
    NAME = "inference"
    DISPLAY_NAME = "模型包评估"

    def __init__(self,
                 inference_skip: int = -1,
                 accelerator: str = Accelerator.T4,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(inference_skip=inference_skip, accelerator=accelerator, pre_nodes=pre_nodes)
    
    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 ensemble_model_name: str = "",
                 dataset_name: str = ""):
        inference_params = {"skip": self.inference_skip,
                            "accelerator": self.properties.accelerator,
                            "model_name": ensemble_model_name,
                            "dataset_name": dataset_name,
                            "advanced_parameters": '{"conf_threshold":"0.5"}'}
        inference_env = {"ACCELERATOR": "{{accelerator}}",
                         "MODEL_NAME": "{{model_name}}",
                         "DATASET_NAME": "{{dataset_name}}",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        inference_params.update(base_params)
        inference_env.update(base_env)
        accelerator = get_accelerator(name=self.properties.accelerator)
        inference_env.update(accelerator.suggest_env())

        inference = ContainerStep(name=Inference.name(),
                                  docker_env=self.suggest_image(),
                                  env=inference_env,
                                  parameters=inference_params,
                                  outputs={"output_uri": Artifact()},
                                  command=f'cd /root && '
                                          f'python3 -m gaea_operator.nodes.inference.inference '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}}')
        set_node_parameters(skip=self.inference_skip, step=inference, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return inference
        
if __name__ == "__main__":
    pipeline_client = pipeline(
        accelerator="T4",
        windmill_ak="a1a9069e2b154b2aa1a83ed12316d163",
        windmill_sk="eefac23d2660404e93855197ce60efb3",
        windmill_endpoint="http://10.27.240.5:8340",
        experiment_kind="Aim",
        experiment_name="std_algorithm",
        tracking_uri="aim://10.27.240.5:8329",
        project_name="workspaces/internal/projects/proj-o97H2oAE",
        train_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        val_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        eval_dataset_name="workspaces/internal/projects/yxdTestPipeline/datasets/ds-xplNB7iS/versions/1",
        train_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm",
        train_model_display_name="std_algorithm",
        eval_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm/versions/latest",
        transform_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm/versions/latest",
        transform_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm-t4",
        transform_model_display_name="std_algorithm-t4",
        transform_eval_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm-t4/"
                                        "versions/latest",
        ensemble_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm-ensemble",
        ensemble_model_display_name="std_algorithm-ensemble",
        inference_input_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/std_algorithm-ensemble/"
                                   "versions/latest")
    pipeline_client.compile(save_path="std_algorithm_pipeline.yaml")
    _, run_id = pipeline_client.run(fs_name="vistudio")
