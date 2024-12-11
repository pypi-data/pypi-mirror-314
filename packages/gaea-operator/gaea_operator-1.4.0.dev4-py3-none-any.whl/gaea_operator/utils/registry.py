#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/21
# @Author  : yanxiaodong
# @File    : registry.py
"""
import inspect


class Registry(object):
    """
    Register a given module class.
    """

    def __init__(self, name: str):
        self._name = name
        self._module_dict = dict()

    def __repr__(self):
        format_str = self.__class__.__name__ + '(name={}, items={})'.format(
            self._name, list(self._module_dict.keys()))
        return format_str

    @property
    def name(self):
        """
        Get the registry name.
        """
        return self._name

    @property
    def module_dict(self):
        """
        Get the registry record.
        """
        return self._module_dict

    def get(self, key: str):
        """
        Get the registry record.
        """
        return self._module_dict.get(key)

    def _register_module(self, module_name, module_class):
        if not inspect.isclass(module_class):
            raise TypeError('module must be a class, but got {}'.format(type(module_class)))
        module_name = module_name if isinstance(module_name, str) and len(module_name) > 0 else module_class.__name__
        if module_name not in self._module_dict:
            self._module_dict[module_name] = module_class

    def register_module(self, name: str = None):
        """
        A record will be added to ``self._module_dict``, whose key is the class
        name or the specified name, and value is the class itself.
        """

        def _register(cls):
            self._register_module(name, cls)
            return cls

        return _register


METRIC = Registry('gaea_metric')