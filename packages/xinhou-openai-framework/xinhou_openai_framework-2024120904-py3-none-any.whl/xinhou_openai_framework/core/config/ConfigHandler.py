# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
配置处理器

用于在系统启动时加载yml配置文件
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ConfigHandler.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/3/10 00:15   shenpeng   1.0         None
"""
import yaml


class ConfigHandler:

    @staticmethod
    def init_config(app):
        pass

    @staticmethod
    def read_yaml(config_path):
        if config_path:
            with open(config_path, encoding='utf-8') as f:
                conf = yaml.full_load(f.read())
            if conf is None:
                raise KeyError("未找到对应的配置信息")
            return conf
        else:
            raise ValueError("请输入正确的配置名称或配置文件路径")

    def load_yaml(content):
        conf = yaml.full_load(content)
        if conf is None:
            raise KeyError("未找到对应的配置信息")
        return conf
