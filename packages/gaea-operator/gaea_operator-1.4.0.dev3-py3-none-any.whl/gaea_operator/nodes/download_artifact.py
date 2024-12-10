#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/6/25
# @Author  : yanxiaodong
# @File    : load_artifact.py
"""
import bcelogger
import json
import shutil
import os

from windmillclient.client.windmill_client import WindmillClient
from gaea_operator.utils import read_file


def download_artifact(windmill_client: WindmillClient,
                      input_uri: str,
                      artifact_name: str,
                      output_uri: str,
                      is_copy: bool = False):
    """
    download artifact
    """
    if input_uri is not None and len(input_uri) > 0:
        bcelogger.info(f"Artifact input uri is {input_uri}")
        response = read_file(input_dir=input_uri)
        artifact_name = response["name"]
        if is_copy:
            bcelogger.info(f"Copying artifact from input uri {input_uri} to output uri {output_uri}")
            shutil.copytree(input_uri, output_uri, dirs_exist_ok=True)
        else:
            output_uri = input_uri

        return output_uri, artifact_name

    bcelogger.info(f"Model artifact name is {artifact_name}")
    assert artifact_name is not None and len(artifact_name) > 0, "Artifact name is None"
    response = windmill_client.get_artifact(name=artifact_name)
    response = json.loads(response.raw_data)
    windmill_client.download_artifact(object_name=response["objectName"],
                                      version=str(response["version"]),
                                      output_uri=output_uri)

    return output_uri, artifact_name