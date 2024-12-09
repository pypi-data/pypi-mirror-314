# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework  
@File    :   PathUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/11/17 16:28   shenpeng   1.0         None
"""
import os
import shutil
from shutil import copyfile

from loguru import logger

from xinhou_openai_framework.utils.StrUtil import StrUtil


class PathUtil:

    @staticmethod
    def get_root_path() -> str:
        """ 获取项目根路径 """
        return os.getcwd()

    @staticmethod
    def get_project_path_name() -> str:
        """ 在项目根路径上获取项目名称 """
        return StrUtil.sub_str_after(PathUtil.get_root_path(), "/", True)

    @staticmethod
    def get_file_path(filePath: str) -> str:
        """ 获取指定文件的目录路径 """
        return os.path.abspath(os.path.dirname(filePath))

    @staticmethod
    def get_file_up_path(filePath: str, level: int) -> str:
        """
        根据文件反馈层级目录路径
        :param filePath:
        :param level: 需要向上取层级（从文件开始计算 文件>目录>目录）
        :return:
        """
        while level > 0:
            filePath = os.path.abspath(os.path.dirname(filePath))
            # logger.info(filePath)
            level = level - 1
        return filePath

    @staticmethod
    def not_exists_mkdir(path) -> str:
        """ 检查目录是否存在，如果不存在则创建并创建初始化py文件 """
        if not os.path.exists(path):
            os.makedirs(path)
            copyfile(PathUtil.get_root_path() + "/templates/code/__init__.py", path + "/__init__.py")
        return path

    @staticmethod
    def rmdir(path):
        if os.path.exists(path):
            if os.listdir(path):
                for i in os.listdir(path):
                    path_file = os.path.join(path, i)  # 取文件绝对路径
                    logger.info(path_file)
                    if os.path.isfile(path_file):
                        os.remove(path_file)
                    else:
                        PathUtil.rmdir(path_file)
                        shutil.rmtree(path_file)


if __name__ == '__main__':
    # logger.info(PathUtil.get_project_path_name())
    PathUtil.rmdir(f"{PathUtil.get_root_path()}/vectordb/1_prompt_999")
