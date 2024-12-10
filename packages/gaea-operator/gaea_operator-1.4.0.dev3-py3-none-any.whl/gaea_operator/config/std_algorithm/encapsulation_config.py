# -*- coding: utf-8 -*-
"""
本模块用于解析标准化产线的配置文件

Authors: xumingyang02(xumingyang02@baidu.com)
Date:    2024/08/21
"""
import yaml
import bcelogger

class EncapsulationConfig():
    """
    标准化产线的配置文件解析
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.normalize_mean = None
        self.normalize_std = None
        self.resize_type = 1
        self.resize_height = None
        self.resize_width = None
        self.tasks = None
    def __check(self):
        if self.resize_height is None or self.resize_width is None:
            return False
        if self.normalize_mean is None or self.normalize_std is None:
            return False
        if self.tasks is None:            
            return False
        return True
    def parse(self):
        """
        解析配置文件
        """
        with open(self.config_file) as f:
            dataMap = yaml.safe_load(f)
            
            if 'paddle_framework' not in dataMap.keys():
                raise Exception("not found paddle_framework")
            framework = dataMap['paddle_framework'].lower()
            if framework == 'paddlecls' or framework == 'ppcls':
                self.pre_image = {}
                self.__parse_paddle_cls(dataMap)
            elif framework == 'paddledet' or framework == 'ppdet' or framework == 'ppyolo':
                self.__parse_paddle_det(dataMap)
            elif framework == 'others':
                self.__pares_other(dataMap)
            else:
                raise Exception("unsupport framework: {} name: {}".format(framework, self.config_file))
            
            self.__parse_tasks(dataMap)
        if not self.__check():
            raise Exception("parse config error")
        return True
            
    def __parse_paddle_cls(self, dataMap):
        if 'DataLoader' in dataMap.keys() and \
            'Eval' in dataMap['DataLoader'].keys() and \
            'dataset' in dataMap['DataLoader']['Eval'].keys() and \
            'transform_ops' in dataMap['DataLoader']['Eval']['dataset'].keys():
            trans_ops = dataMap['DataLoader']['Eval']['dataset']['transform_ops']
            for op in trans_ops:
                if 'ResizeImage' in op.keys():
                    if 'size' in op['ResizeImage'].keys():
                        if isinstance(op['ResizeImage']['size'], int):
                            self.resize_height = op['ResizeImage']['size']
                            self.resize_width = op['ResizeImage']['size']
                        elif isinstance(op['ResizeImage']['size'], list) and len(op['ResizeImage']['size']) >= 2: 
                            self.resize_height = op['ResizeImage']['size'][1]
                            self.resize_width = op['ResizeImage']['size'][0]
                        else:
                            raise Exception("ResizeImage size type not support")
                    else:
                        raise Exception("ResizeImage unsupport data type")
                elif 'NormalizeImage' in op.keys():
                    if 'mean' in op['NormalizeImage'].keys() and 'std' in op['NormalizeImage'].keys():
                        self.normalize_mean = op['NormalizeImage']['mean']
                        self.normalize_std = op['NormalizeImage']['std']
                        assert len(self.normalize_mean) == 3 and len(self.normalize_std) == 3, "mean std must be three"
                    else:
                        raise Exception("NormalizeImage mean or std unsupport")
    def __parse_paddle_det(self, dataMap):
        for it in dataMap['TestReader']['sample_transforms']:
            if 'Resize' in it.keys():
                if it['Resize']['interp'] == 0:
                    self.resize_type = "nearest"
                elif it['Resize']['interp'] == 1:
                    self.resize_type = "bilinear"
                else:
                    self.resize_type = "bilinear"
                    bcelogger.warning('do NOT support resize-type. {} use default: {}'.format(
                        it['Resize']['interp'], self.resize_type))
                if 'target_size' in it['Resize'].keys():
                    if isinstance(it['Resize']['target_size'], int):
                        self.resize_height = it['Resize']['target_size']
                        self.resize_width = it['Resize']['target_size']
                    elif isinstance(it['Resize']['target_size'], list) and len(it['Resize']['target_size']) >= 2:
                        self.resize_height = it['Resize']['target_size'][0]
                        self.resize_width = it['Resize']['target_size'][1]
            elif 'NormalizeImage' in it.keys():
                #归一化参数默认是按rgb给出,转入后按bgr给出
                mean = it['NormalizeImage']['mean']
                std = it['NormalizeImage']['std']
                assert len(mean) == 3 and len(std) == 3, "mean std must be three"
                self.normalize_mean = mean
                self.normalize_std = std
    def __pares_other(self, dataMap):
        pass
    
    def __parse_tasks(self, dataMap):
        super_category_task_type = ['image_classification']
        if 'tasks' in dataMap.keys():
            self.tasks = dataMap['tasks']
            for task in self.tasks:
                task['task_source'] = 'standard'
                task_name = None
                if 'task_name' in task.keys():
                    task_name = task['task_name']
                task_type = None
                if 'task_type' in task.keys():
                    task_type = task['task_type']
                if 'categories' in task.keys():
                    new_dict = {int(k): v for k, v in task['categories'].items()} 
                    sorted_list = sorted(new_dict.items(), key=lambda x: x[0])  
                    new_categories = []
                    for k, v in sorted_list:
                        item_category = {'id': k, 'name': v} if isinstance(v, str) else {'id': k, 'name': str(v)}
                        if task_name is not None and task_type is not None and task_type in super_category_task_type:
                            item_category['super_category'] = task_name
                            if 'anno_key' in task.keys():
                                item_category['super_category_id'] = int(task['anno_key']) - 1
                            else:
                                bcelogger.info('multiclassify task do NOT find key: anno_key, only set super_category')
                        new_categories.append(item_category)
                    task['categories'] = new_categories
            return True
        return False
    def advanced_parameters(self):
        """
        获取高级参数
        """
        params = {}
        params['eval_size'] = str(self.resize_width) + '*' + str(self.resize_height)
        params['normalize_mean'] = self.normalize_mean
        params['normalize_std'] = self.normalize_mean
        params['tasks'] = self.tasks
        return params

