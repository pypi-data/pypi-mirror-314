#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/26
# @Author  : liyinggang
# @File    : resnet_pipeline.py
"""
import os
from paddleflow.pipeline import Pipeline
from paddleflow.pipeline import CacheOptions
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, \
    DEFAULT_PYTORCH_MODEL_FILE_NAME, \
    ModelTemplate
from gaea_operator.nodes.transform_eval import transform_eval_step
from gaea_operator.nodes.package import package_step
from gaea_operator.nodes.inference import inference_step


@Pipeline(
    name="convnext",
    cache_options=CacheOptions(enable=False),
)
def pipeline(accelerator: str = "T4",
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
             train_dataset_name: str = "",
             val_dataset_name: str = "",
             base_train_dataset_name: str = "",
             base_val_dataset_name: str = "",
             train_model_name: str = "",
             train_model_display_name: str = "",
             eval_dataset_name: str = "",
             transform_model_name: str = "",
             transform_model_display_name: str = "",
             ensemble_model_name: str = "",
             ensemble_model_display_name: str = ""):
    """
    Pipeline for convnext training eval transform transform-eval package inference.
    """
    base_params = {"flavour": "c4m16gpu1",
                   "queue": "qtrain",
                   "windmill_ak": windmill_ak,
                   "windmill_sk": windmill_sk,
                   "windmill_endpoint": windmill_endpoint,
                   "experiment_name": experiment_name,
                   "experiment_kind": experiment_kind,
                   "tracking_uri": tracking_uri,
                   "project_name": project_name,
                   "model_store_name": modelstore_name}
    base_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                "PF_JOB_QUEUE_NAME": "{{queue}}",
                "WINDMILL_AK": "{{windmill_ak}}",
                "WINDMILL_SK": "{{windmill_sk}}",
                "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                "EXPERIMENT_KIND": "{{experiment_kind}}",
                "EXPERIMENT_NAME": "{{experiment_name}}",
                "TRACKING_URI": "{{tracking_uri}}",
                "PROJECT_NAME": "{{project_name}}"}

    train_params = {"train_dataset_name": train_dataset_name,
                    "val_dataset_name": val_dataset_name,
                    "base_train_dataset_name": base_train_dataset_name,
                    "base_val_dataset_name": base_val_dataset_name,
                    "model_name": train_model_name,
                    "model_display_name": train_model_display_name,
                    "advanced_parameters": '{"epochs":"20",'
                                            '"warmup_epochs":"2",'
                                            '"lr":"0.0001",'
                                            '"num_workers":"4",'
                                            '"eval_height":"224",'
                                            '"eval_width":"224",'
                                            '"batch_size":"24",'
                                            '"networkArchitecture":"convnext_tiny"}'}
    train_env = {"TRAIN_DATASET_NAME": "{{train_dataset_name}}",
                 "VAL_DATASET_NAME": "{{val_dataset_name}}",
                 "BASE_TRAIN_DATASET_NAME": "{{base_train_dataset_name}}",
                 "BASE_VAL_DATASET_NAME": "{{base_val_dataset_name}}",
                 "MODEL_NAME": "{{model_name}}",
                 "MODEL_DISPLAY_NAME": "{{model_display_name}}",
                 "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    train_env.update(base_env)
    train_params.update(base_params)
    train = ContainerStep(name="train",
                          docker_env="iregistry.baidu-int.com/windmill-public/train/"
                                     "paddlepaddle-2.5.2-gpu-cuda12.0-cudnn8.9-trt86:v1.2.0.9",
                          parameters=train_params,
                          env=train_env,
                          outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                          command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                  f'python3 -m gaea_operator.components.train.convnext '
                                  f'--output-model-uri={{{{output_model_uri}}}} '
                                  f'--output-uri={{{{output_uri}}}} '
                                  f'--log_dir={{{{output_uri}}}} '
                                  f'$package_path/convnext/tools/train.py '
                                  f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                  f'-o output_dir={{{{output_model_uri}}}}')

    eval_params = {"dataset_name": eval_dataset_name}
    eval_env = {"DATASET_NAME": "{{dataset_name}}"}
    eval_env.update(base_env)
    eval_params.update(base_params)
    eval = ContainerStep(name="eval",
                         docker_env="iregistry.baidu-int.com/windmill-public/train/"
                                    "paddlepaddle-2.5.2-gpu-cuda12.0-cudnn8.9-trt86:v1.2.0.9",
                         parameters=eval_params,
                         env=eval_env,
                         inputs={"input_model_uri": train.outputs["output_model_uri"]},
                         outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                         command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                 f'python3 -m gaea_operator.components.eval.convnext '
                                 f'--input-model-uri={{{{input_model_uri}}}} '
                                 f'--output-uri={{{{output_uri}}}} '
                                 f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                 f'--log_dir={{{{output_uri}}}} '
                                 f'$package_path/convnext/tools/eval.py '
                                 f'-c {{{{input_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                 f'-o weight_path='
                                 f'{{{{input_model_uri}}}}/{DEFAULT_PYTORCH_MODEL_FILE_NAME}')

    transform_params = {"transform_model_name": transform_model_name,
                        "transform_model_display_name": transform_model_display_name,
                        "accelerator": "T4",
                        "advanced_parameters": '{"max_batch_size":"4",'
                                               '"eval_height":"224",'
                                               '"eval_width":"224",'
                                               '"source_framework":"onnx",'
                                               '"networkArchitecture":"convnext"}'}
    transform_env = {"TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                     "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                     "ACCELERATOR": "{{accelerator}}",
                     "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    transform_env.update(base_env)
    transform_params.update(base_params)
    transform = ContainerStep(name="transform",
                              docker_env="iregistry.baidu-int.com/windmill-public/transform:v1.2.0.6",
                              env=transform_env,
                              parameters=transform_params,
                              inputs={"input_model_uri": train.outputs["output_model_uri"]},
                              outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                              command=f'python3 -m gaea_operator.components.transform.convnext '
                                      f'--input-model-uri={{{{input_model_uri}}}} '
                                      f'--output-uri={{{{output_uri}}}} '
                                      f'--output-model-uri={{{{output_model_uri}}}}').after(eval)

    transform_eval = transform_eval_step(algorithm=ModelTemplate.CONVNEXT_NAME,
                                         windmill_ak=windmill_ak,
                                         windmill_sk=windmill_sk,
                                         windmill_endpoint=windmill_endpoint,
                                         experiment_kind=experiment_kind,
                                         experiment_name=experiment_name,
                                         tracking_uri=tracking_uri,
                                         project_name=project_name,
                                         accelerator=accelerator,
                                         eval_step=eval,
                                         transform_step=transform)

    package = package_step(algorithm=ModelTemplate.CONVNEXT_NAME,
                           windmill_ak=windmill_ak,
                           windmill_sk=windmill_sk,
                           windmill_endpoint=windmill_endpoint,
                           experiment_kind=experiment_kind,
                           experiment_name=experiment_name,
                           tracking_uri=tracking_uri,
                           project_name=project_name,
                           accelerator=accelerator,
                           transform_step=transform,
                           transform_eval_step=transform_eval,
                           ensemble_model_name=ensemble_model_name,
                           ensemble_model_display_name=ensemble_model_display_name)

    inference = inference_step(windmill_ak=windmill_ak,
                               windmill_sk=windmill_sk,
                               windmill_endpoint=windmill_endpoint,
                               experiment_kind=experiment_kind,
                               experiment_name=experiment_name,
                               tracking_uri=tracking_uri,
                               project_name=project_name,
                               accelerator=accelerator,
                               eval_step=eval,
                               package_step=package)

    return inference.outputs["output_uri"]


if __name__ == "__main__":
    pipeline_client = pipeline(
        accelerator="T4",
        windmill_ak="a1a9069e2b154b2aa1a83ed12316d163",
        windmill_sk="eefac23d2660404e93855197ce60efb3",
        windmill_endpoint="http://10.27.240.5:8340",
        experiment_kind="Aim",
        experiment_name="convnext",
        tracking_uri="aim://10.27.240.5:8329",
        project_name="workspaces/internal/projects/lyg-proj",
        train_dataset_name="workspaces/internal/projects/lyg-proj/datasets/motion-clas/versions/1",
        val_dataset_name="workspaces/internal/projects/lyg-proj/datasets/motion-clas/versions/1",
        eval_dataset_name="workspaces/internal/projects/lyg-proj/datasets/motion-clas/versions/1",
        train_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/convnext",
        train_model_display_name="convnext-tiny",
        transform_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/convnext-t4",
        transform_model_display_name="convnext-t4",
        ensemble_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/convnext-ensemble",
        ensemble_model_display_name="convnext-ensemble")
    pipeline_client.compile(save_path="./convnext_pipeline.yaml")
    _, run_id = pipeline_client.run(fs_name="vistudio")
    print(f"Run ID: {run_id}")
