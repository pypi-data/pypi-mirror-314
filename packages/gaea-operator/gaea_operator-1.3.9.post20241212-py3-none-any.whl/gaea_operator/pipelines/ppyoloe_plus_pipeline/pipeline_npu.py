#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/10
# @Author  : yanxiaodong
# @File    : ppyoloe_plus_m_pipeline.py
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
from gaea_operator.nodes import TransformEval as BaseTransformEval
from gaea_operator.nodes import Package
from gaea_operator.nodes import Inference as BaseInference

NAME_TO_IMAGES = {
    BaseTrain.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/train/paddle_910b:0.5"),
        ],
    BaseEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/train/paddle_910b:0.5"),
        ],
    BaseTransform.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/transform:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/transform:1.3.7-hotfix-20240923"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/inference/ascend_arm64_model:v1.0.5"),
        ],
    BaseTransformEval.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/inference/ascend_arm64_model:v1.0.5")
        ],
    Package.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/inference/ascend_arm64_model:v1.0.5")
        ],
    BaseInference.name():
        [
            Image(kind=Accelerator.NVIDIA,
                  name="iregistry.baidu-int.com/windmill-public/inference/nvidia:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.KUNLUN,
                  name="iregistry.baidu-int.com/windmill-public/inference/kunlun:1.3.7-hotfix-20241119"),
            Image(kind=Accelerator.ASCEND,
                  name="iregistry.baidu-int.com/windmill-public/inference/ascend_arm64_model:v1.0.5")
        ]}


@Pipeline(
    name="ppyoloe_plus",
    cache_options=CacheOptions(enable=True, max_expired_time=604800),
    parallelism=6,
    failure_options=FailureOptions(strategy="continue"),
)
def pipeline(accelerator: str = "T4",
             train_accelerator: str = None,
             eval_accelerator: str = None,
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
             extra_fs_name: str = "defaultfs",
             extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-defaultfs",
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
    Pipeline for ppyoloe_plus_m training eval transform transform-eval package inference.
    """
    base_params = {"flavour": "c8m32npu1",
                   "queue": "a910b",
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
        accelerator = Accelerator.Ascend910B

    # 1. Train
    if train_accelerator is None:
        train_accelerator = accelerator
    train = Train(train_skip=train_skip, accelerator=train_accelerator)
    train.properties = Properties(images=NAME_TO_IMAGES[train.name()])
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

    # 2. Eval
    if eval_accelerator is None:
        eval_accelerator = accelerator
    eval = Eval(eval_skip=eval_skip, pre_nodes=pre_nodes, accelerator=eval_accelerator)
    eval.inputs = eval_inputs
    eval.properties = Properties(images=NAME_TO_IMAGES[eval.name()])
    eval_step = eval(base_params=base_params,
                     base_env=base_env,
                     eval_dataset_name=eval_dataset_name,
                     eval_model_name=eval_model_name)
    pre_nodes[eval_step.name] = eval_step

    # 3. Transform
    if transform_accelerator is None:
        transform_accelerator = accelerator
    transform = Transform(transform_skip=transform_skip,
                          algorithm=ModelTemplate.PPYOLOE_PLUS_NAME,
                          category=Category.CategoryImageObjectDetection.value,
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

    # 4. TransformEval
    if transform_eval_accelerator is None:
        transform_eval_accelerator = accelerator
    transform_eval = TransformEval(transform_eval_skip=transform_eval_skip,
                                   algorithm=ModelTemplate.PPYOLOE_PLUS_NAME,
                                   accelerator=transform_eval_accelerator,
                                   pre_nodes=pre_nodes)
    transform_eval.inputs = transform_eval_inputs
    transform_eval.properties = Properties(images=NAME_TO_IMAGES[transform_eval.name()])
    transform_eval_step = transform_eval(base_params=base_params,
                                         base_env=base_env,
                                         dataset_name=eval_dataset_name,
                                         transform_model_name=transform_eval_input_model_name)
    pre_nodes[transform_eval_step.name] = transform_eval_step

    # 5. Package
    if package_accelerator is None:
        package_accelerator = accelerator
    package = Package(package_skip=package_skip,
                      algorithm=ModelTemplate.PPYOLOE_PLUS_NAME,
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

    # 6. Inference
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


class Train(BaseTrain):
    """
    Train
    """

    def __init__(self, train_skip: int = -1, accelerator: str=Accelerator.Ascend910B):
        super().__init__(train_skip=train_skip, accelerator=accelerator)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.ASCEND: {f"{self.name()}.model_name": ["PaddlePaddle"]},
        })

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
                        "advanced_parameters": '{"epoch":"10",'
                                               '"LearningRate.base_lr":"0.001",'
                                               '"worker_num":"1",'
                                               '"eval_size":"640*640",'
                                               '"TrainReader.batch_size":"8",'
                                               '"networkArchitecture":"检测模型-标准版"}'}
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

        train = ContainerStep(name=Train.name(),
                              docker_env=self.suggest_image(),
                              parameters=train_params,
                              env=train_env,
                              extra_fs=[ExtraFS(name=extra_fs_name, mount_path=extra_fs_mount_path)],
                              outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                              command=f'cd /root && '
                                      f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])")  && '
                                      f'export HUAWEI_ASCEND_TOOLKIT_HOME="/usr/local/Ascend/driver" && '
                                      f'export HUAWEI_ASCEND_TOOLKIT_HOME="/usr/local/Ascend/ascend-toolkit" && '
                                      f'export LD_LIBRARY_PATH=/usr/local/Ascend/atb/1.0.RC1/atb/lib'
                                      f'/:$LD_LIBRARY_PATH &&'
                                      f'export LD_LIBRARY_PATH=/usr/local/Ascend/ascend-toolkit/latest/'
                                      f'aarch64-linux/lib64/libmsprofiler.so:$LD_LIBRARY_PATH && '
                                      f'export ASCEND_RT_VISIBLE_DEVICES="$ASCEND_VISIBLE_DEVICES" && '
                                      f'export FLAGS_npu_storage_format=0 && '
                                      f'export FLAGS_npu_jit_compile=0 && '
                                      f'export FLAGS_use_stride_kernel=0 && '
                                      f'. /usr/local/Ascend/ascend-toolkit/set_env.sh && '
                                      f'sh -c "bash /usr/local/Ascend/atb/set_env.sh" && '
                                      f'python3 -m gaea_operator.nodes.train.ppyoloe_plus '
                                      f'--output-model-uri={{{{output_model_uri}}}} '
                                      f'--output-uri={{{{output_uri}}}} '
                                      f'$package_path/paddledet/tools/train.py '
                                      f'--eval '
                                      f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                      f'-o save_dir={{{{output_model_uri}}}}')

        if self.train_skip > 0:
            skip_parameter = "skip"
            train.condition = f"{train.parameters[skip_parameter]} < 0"

        return train


class Eval(BaseEval):
    """
    Eval
    """

    def __init__(self,
                 eval_skip: int = -1,
                 accelerator: str = Accelerator.Ascend910B,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(eval_skip=eval_skip, accelerator=accelerator, pre_nodes=pre_nodes)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.KUNLUN: {f"{self.name()}.model_name": ["PaddlePaddle"]},
            Accelerator.ASCEND: {f"{self.name()}.model_name": ["PaddlePaddle"]},
        })

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

        eval = ContainerStep(name=Eval.name(),
                             docker_env=self.suggest_image(),
                             parameters=eval_params,
                             env=eval_env,
                             outputs={"output_uri": Artifact(),
                                      "output_dataset_uri": Artifact(),
                                      "output_model_uri": Artifact()},

                             command=f'cd /root && '
                                     f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                     f'export HUAWEI_ASCEND_TOOLKIT_HOME="/usr/local/Ascend/driver" && '
                                     f'export HUAWEI_ASCEND_TOOLKIT_HOME="/usr/local/Ascend/ascend-toolkit" && '
                                     f'export LD_LIBRARY_PATH=/usr/local/Ascend/atb/1.0.RC1/atb/lib/:$LD_LIBRARY_PATH '
                                     f'&&'
                                     f'export LD_LIBRARY_PATH=/usr/local/Ascend/ascend-toolkit/latest/'
                                     f'aarch64-linux/lib64/libmsprofiler.so:$LD_LIBRARY_PATH && '
                                     f'export ASCEND_RT_VISIBLE_DEVICES="$ASCEND_VISIBLE_DEVICES" && '
                                     f'export FLAGS_npu_storage_format=0 && '
                                     f'export FLAGS_npu_jit_compile=0 && '
                                     f'export FLAGS_use_stride_kernel=0 && '
                                     f'. /usr/local/Ascend/ascend-toolkit/set_env.sh && '
                                     f'sh -c "bash /usr/local/Ascend/atb/set_env.sh" && '
                                     f'python3 -m gaea_operator.nodes.eval.ppyoloe_plus '
                                     f'--input-model-uri={{{{input_model_uri}}}} '
                                     f'--output-model-uri={{{{output_model_uri}}}} '
                                     f'--output-uri={{{{output_uri}}}} '
                                     f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                     f'$package_path/paddledet/tools/eval.py '
                                     f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                     f'-o weights={{{{output_model_uri}}}}/{DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME}')

        set_node_parameters(skip=self.eval_skip, step=eval, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return eval


class Transform(BaseTransform):
    """
    Transform
    """

    def __init__(self,
                 transform_skip: int = -1,
                 algorithm: str = "",
                 category: str = "",
                 accelerator: str = Accelerator.Atlas310P,
                 pre_nodes: Dict[str, ContainerStep] = None):
        super().__init__(transform_skip=transform_skip,
                         algorithm=algorithm,
                         category=category,
                         accelerator=accelerator,
                         pre_nodes=pre_nodes)
        self.properties = Properties(modelFormats={
            Accelerator.NVIDIA: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["TensorRT"]},
            Accelerator.KUNLUN: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["PaddleLite"]},
            Accelerator.ASCEND: {
                f"{self.name()}.train_model_name": ["PaddlePaddle"],
                f"{self.name()}.transform_model_name": ["Other"]},
        })

    def __call__(self,
                 base_params: dict = None,
                 base_env: dict = None,
                 train_model_name: str = "",
                 transform_model_name: str = "",
                 transform_model_display_name: str = "",
                 advanced_parameters: str = ""):

        transform_params = {"skip": self.transform_skip,
                            "train_model_name": train_model_name,
                            "transform_model_name": transform_model_name,
                            "transform_model_display_name": transform_model_display_name,
                            "accelerator": self.properties.accelerator,
                            "advanced_parameters": '{"iou_threshold":"0.7",'
                                                   '"conf_threshold":"0.01",'
                                                   '"max_box_num":"30",'
                                                   '"max_batch_size":"1",'
                                                   '"precision":"fp16",'
                                                   '"eval_size":"640*640",'
                                                   '"source_framework":"paddle",'
                                                   '"networkArchitecture":"检测模型-标准版"}'}
        transform_env = {"TRAIN_MODEL_NAME": "{{train_model_name}}",
                         "TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                         "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                         "ACCELERATOR": "Atlas310",
                         "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
        transform_env.update(base_env)
        transform_params.update(base_params)

        transform = ContainerStep(name=Transform.name(),
                                  docker_env=self.suggest_image(),
                                  env=transform_env,
                                  parameters=transform_params,
                                  outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                                  command=f'cd /root && '
                                          f' . /usr/local/Ascend/ascend-toolkit/set_env.sh && '
                                          f'python3 -m gaea_operator.nodes.transform.transform '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}} '
                                          f'--output-model-uri={{{{output_model_uri}}}}')
        set_node_parameters(skip=self.transform_skip, step=transform, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return transform


class TransformEval(BaseTransformEval):
    """
    TransformEval
    """

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
                                       command=f'. /usr/local/Ascend/ascend-toolkit/set_env.sh && '
                                               f'export ASCEND_RT_VISIBLE_DEVICES="0" && '
                                               f'export XPU_VISIBLE_DEVICES="0" && '
                                               f'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/extend_libs:'
                                               f'/usr/local/Ascend/ascend-toolkit/latest/runtime/lib64/stub && '
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


class Inference(BaseInference):
    """
    Inference
    """

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
                                          f'. /usr/local/Ascend/ascend-toolkit/set_env.sh && '
                                          f'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/extend_libs:'
                                          f'/usr/local/Ascend/ascend-toolkit/latest/runtime/lib64/stub && '
                                          f'export ASCEND_RT_VISIBLE_DEVICES="0" && '
                                          f'export XPU_VISIBLE_DEVICES="0" && '
                                          f'python3 -m gaea_operator.nodes.inference.inference '
                                          f'--input-model-uri={{{{input_model_uri}}}} '
                                          f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                          f'--output-uri={{{{output_uri}}}}')

        set_node_parameters(skip=self.inference_skip, step=inference, inputs=self.inputs, pre_nodes=self.pre_nodes)

        return inference

if __name__ == "__main__":
    ppl = pipeline(
        accelerator="Atlas910",
        windmill_ak="a440a816330a4e558ec33d50aaad379d",
        windmill_sk="d9068f8ff3604a45a83b81c987de673a",
        windmill_endpoint="http://172.0.56.186:8340",
        experiment_kind="Aim",
        experiment_name="ppyoloe_plus_m",
        tracking_uri="aim://172.0.56.186:8329",
        project_name="workspaces/wsimtrii/projects/spiproject",
        train_dataset_name="workspaces/wsimtrii/projects/spiproject/datasets/ds-qmuEoSm2/versions/1",
        val_dataset_name="workspaces/wsimtrii/projects/spiproject/datasets/ds-qmuEoSm2/versions/1",
        eval_dataset_name="workspaces/wsimtrii/projects/spiproject/datasets/ds-qmuEoSm2/versions/1",
        train_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus44444",
        train_model_display_name="ppyoloe-plus",
        eval_model_name="workspaces/public/modelstores/modelstore/models/ppyoloe-plus/versions/latest",
        transform_input_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus/versions/latest",
        transform_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus-t4",
        transform_model_display_name="ppyoloe-plus-t4",
        transform_eval_input_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus-t4/"
                                        "versions/latest",
        ensemble_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus-ensemble",
        ensemble_model_display_name="ppyoloe-plus-ensemble",
        inference_input_model_name="workspaces/wsimtrii/modelstores/modelstore/models/ppyoloe-plus-ensemble/"
                                   "versions/latest")

    ppl.compile(save_path="ppyoloe_plus_pipeline_npu.yaml")
    _, run_id = ppl.run(fs_name="defaultfs")