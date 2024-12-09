# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   marmot-xinhou-openai-framework
@File    :   FileUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/1 14:58   shenpeng   1.0         None
"""
import os
import shutil

from loguru import logger


class FileUtil:
    """
    FileUtil是一个文件处理工具类，提供了常用的文件处理功能以及文件上传下载功能。
    """

    @staticmethod
    def create_file(file_path, content=None):
        """
        创建文件
        :param file_path: 文件路径
        :param content: 文件内容，默认为None
        :return: None
        """
        with open(file_path, 'w') as f:
            if content:
                f.write(content)

    @staticmethod
    def read_file(file_path):
        """
        读取文件内容
        :param file_path: 文件路径
        :return: 文件内容
        """
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def append_to_file(file_path, content):
        """
        在文件末尾追加内容
        :param file_path: 文件路径
        :param content: 追加的内容
        :return: None
        """
        with open(file_path, 'a') as f:
            f.write(content)

    @staticmethod
    def copy_file(src_file_path, dst_file_path):
        """
        复制文件
        :param src_file_path: 源文件路径
        :param dst_file_path: 目标文件路径
        :return: None
        """
        shutil.copy(src_file_path, dst_file_path)

    @staticmethod
    def move_file(src_file_path, dst_file_path):
        """
        移动文件
        :param src_file_path: 源文件路径
        :param dst_file_path: 目标文件路径
        :return: None
        """
        shutil.move(src_file_path, dst_file_path)

    @staticmethod
    def delete_file(file_path):
        """
        删除文件
        :param file_path: 文件路径
        :return: None
        """
        os.remove(file_path)


if __name__ == '__main__':
    file_path = 'test.txt'

    # 创建文件
    FileUtil.create_file(file_path, 'Hello, FileUtil!')

    # 读取文件内容
    logger.info('文件内容:', FileUtil.read_file(file_path))

    # 在文件末尾追加内容
    FileUtil.append_to_file(file_path, '\nAppended text!')
    logger.info('文件内容:', FileUtil.read_file(file_path))

    # 复制文件
    copy_file_path = 'copy_' + file_path
    FileUtil.copy_file(file_path, copy_file_path)

    # 移动文件
    move_file_path = 'move_' + file_path
    FileUtil.move_file(copy_file_path, move_file_path)

    # 删除文件
    FileUtil.delete_file(file_path)
    FileUtil.delete_file(move_file_path)
