# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify parse.yaml
Authors: zhouwenlong(zhouwenlong01@baidu.com)
         wanggaofei(wanggaofei03@baidu.com)
Date:    2023-03-16
"""
import yaml
import os
import argparse
import bcelogger

KEY_OUTPUTS = 'outputs'
KEY_MODEL_NAME = 'model_name'
KEY_MODEL_CN_NAME = 'model_cn_name'
KEY_PARSE_NAME = 'parse.yaml'


class ParseYamlConfig(object):
    """
    解析修改模型包 parse.yaml
    """
    def __init__(self, yaml_name):
        """
            初始化YAML数据类，用于读取和解析指定名称的YAML文件。
        
        Args:
            yaml_name (str): YAML文件名，不包含路径信息。
        
        Returns:
            None.
        """
        self.yaml_data = self.get_yaml(yaml_name)

    def get_yaml(self, yaml_name):
        """
            read parse.yaml
        """
        if not os.path.exists(yaml_name):
            raise FileNotFoundError(yaml_name)
        with open(yaml_name, 'r', encoding='utf-8') as f:
            file_data = f.read()
            yaml_data = yaml.load(file_data, Loader=yaml.FullLoader)
            return yaml_data

    def modify_labels(self, labels : list, modify_model_name: str, template_model_name: str):
        """
            modify categories by model-name
        """
        class_field = self.yaml_data.get(KEY_OUTPUTS , None)
        if class_field is None:
            raise ValueError("outputs is None")
        
        ensemble_field = class_field[0]
        fields_map = ensemble_field.get("fields_map", None)
        if fields_map is None or len(fields_map) == 0:
            raise ValueError("fields_map is None or len(fields_map) == 0")

        for single_map in fields_map:
            model_name = single_map.get(KEY_MODEL_NAME, None)
            if model_name is None:
                raise ValueError("model_name is None")
            
            model_name = model_name.split('|')[0]
            if model_name == modify_model_name or model_name == template_model_name:
                new_categories = []
                for task in labels:
                    task_category = []
                    if 'categories' not in task:
                        bcelogger.error('task can not get categories. model_name: {}'.format(model_name))
                        continue
                    for cidx, class_name in enumerate(task['categories']):
                        id_names = {
                            "display_name": class_name["displayName"] if "displayName" in class_name else "",
                            "name": class_name["name"],
                            "id": str(class_name["id"])
                        }
                        if "super_category" in class_name:
                            id_names["super_category"] = class_name["super_category"]
                        if "super_category_id" in class_name:
                            id_names["super_category_id"] = class_name["super_category_id"]
                        task_category.append(id_names)

                    bcelogger.info('set categories. model_name: {} num: {}'.format(model_name, len(task_category)))
                    if 'task_source' in task and task['task_source'] == 'standard':
                        if task['task_type'] == 'instance_segmentation':
                            new_categories.extend(task_category)
                        else:
                            new_categories.append(task_category)
                        bcelogger.info('standard task use double list categories.  \
                            model_name: {} current task_num: {}'.format(model_name, len(new_categories)))
                    else:
                        new_categories.extend(task_category)
                        bcelogger.info('other task use single list categories.  \
                            model_name: {} current category_num: {}'.format(model_name, len(new_categories)))

                single_map["categories"] = new_categories
                bcelogger.info('set categories. model_name: {} num: {}'.format(model_name, len(new_categories)))

    def modify_model_name(self, modify_model_name: str, template_model_name: str, modify_model_display_name: str):
        """
        modify model name
        """
        class_field = self.yaml_data.get(KEY_OUTPUTS, None)
        if class_field is None:
            raise ValueError("outputs is None")

        ensemble_field = class_field[0]
        fields_map = ensemble_field.get("fields_map", None)
        if fields_map is None:
            raise ValueError("fields_map is None")

        for single_map in fields_map:
            model_name_id = single_map.get(KEY_MODEL_NAME, None)
            if model_name_id is None:
                raise ValueError("model_name is None")

            split_model_name_id = model_name_id.split('|')
            model_name = split_model_name_id[0]
            model_id = split_model_name_id[-1] if len(split_model_name_id) > 1 else None
            if model_name == modify_model_name or model_name == template_model_name:
                if model_id is not None:
                    single_map[KEY_MODEL_NAME] = "|".join([modify_model_name, model_id])
                else:
                    single_map[KEY_MODEL_NAME] = modify_model_name
                single_map[KEY_MODEL_CN_NAME] = modify_model_display_name
                bcelogger.info('set model_name: {} model_cn_name: {}'.format(single_map[KEY_MODEL_NAME],
                                                                             single_map[KEY_MODEL_CN_NAME]))

    def modify_ensemble_name(self, ensemble_name: str):
        """
            modify ensemble name
        """
        if KEY_OUTPUTS in self.yaml_data:
            for _, v in enumerate(self.yaml_data[KEY_OUTPUTS]):
                if KEY_MODEL_NAME in v and 'ensemble' in v[KEY_MODEL_NAME]:
                    v[KEY_MODEL_NAME] = ensemble_name
                    bcelogger.info('modify ensemble name: {}'.format(ensemble_name))
        else:
            bcelogger.error('do NOT find key in parse.yaml: {}'.format(KEY_OUTPUTS))

    def save_yaml(self, yaml_name):
        """
        将字典数据保存为YAML格式的文件。
        
        Args:
            yaml_name (str): YAML文件名，包含路径。
        
        Returns:
            None; 无返回值，直接写入文件。
        """
        with open(yaml_name, 'w', encoding='utf-8') as f:
            yaml.dump(self.yaml_data, f, allow_unicode=True, sort_keys=False)

if __name__ == '__main__':
    cfg = ParseYamlConfig('./parse.yaml')

    # 1. set ensemble name
    cfg.modify_ensemble_name('abc-ensemble')

    # 2. set categories
    # categories = ['label1', 'label2']
    # label = {}
    # label['categories'] = categories
    # cfg.modify_labels([label])

    # 3. save
    cfg.save_yaml('./output-parse.yaml')