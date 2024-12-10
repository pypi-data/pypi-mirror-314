#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : singleton_context
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 11:50
# Description :
"""
from threading import RLock
from contextvars import ContextVar


class SingletonContext(object):
    """
    单例模式，用于保存全局上下文变量。
    """

    single_lock = RLock()
    _instance = None

    def __init__(self):
        """
        初始化全局上下文
        """
        self.context = ContextVar("global_context", default={})

    @classmethod
    def instance(cls):
        """
        获取单例实例
        """
        with cls.single_lock:
            if cls._instance is None:
                cls._instance = SingletonContext()
        return cls._instance

    @staticmethod
    def set_var_value(key: str, value: str):
        """
        设置上下文变量值
        :param key: 变量名
        :param value: 变量值
        """
        var = SingletonContext.instance().context.get()
        if var is None:
            return False

        var[key] = value
        SingletonContext.instance().context.set(var)

    @staticmethod
    def get_context():
        """
        获取整个上下文
        """
        return SingletonContext.instance().context.get()

    @staticmethod
    def get_var_value(key: str):
        """
        获取上下文变量值
        :param key: 变量名
        :return: 变量值
        """
        var = SingletonContext.instance().context.get()
        if var is None:
            return None
        return var.get(key)