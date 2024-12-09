# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
ZipUtil压缩工具类
支持文件压缩，批量文件压缩
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ZipUtil.py    
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 11:42   shenpeng   1.0         None
"""

import zipfile


class ZipUtil:
    """压缩文件的类。

    属性：
        compression_type: 压缩使用的类型（默认是ZIP_DEFLATED）。
        compression_level: 压缩使用的级别（默认是9）。
    """

    def __init__(self, compression_type=zipfile.ZIP_DEFLATED, compression_level=9):
        """使用给定的压缩类型和级别初始化ZipUtil类。

        args：
            compression_type: 压缩使用的类型（默认是ZIP_DEFLATED）。
            compression_level: 压缩使用的级别（默认是9）。
        """
        self.compression_type = compression_type
        self.compression_level = compression_level

    def compress_file(self, file_path, zip_file_path):
        """将单个文件压缩到给定文件路径的zip存档中。

        args：
            file_path: 要压缩的文件的路径。
            zip_file_path: 要创建的zip存档的路径。
        """
        with zipfile.ZipFile(zip_file_path, 'w', compression=self.compression_type,
                             compresslevel=self.compression_level) as zip:
            zip.write(file_path)

    def compress_files(self, file_paths, zip_file_path):
        """将多个文件压缩到给定文件路径的zip存档中。

        参数：
            file_paths: 要压缩的文件的路径列表。
            zip_file_path: 要创建的zip存档的路径。
        """
        with zipfile.ZipFile(zip_file_path, 'w', compression=self.compression_type,
                             compresslevel=self.compression_level) as zip:
            for file_path in file_paths:
                zip.write(file_path)


if __name__ == '__main__':
    # 使用默认压缩类型和级别实例化ZipUtil类
    zip_util = ZipUtil()

    # 压缩单个文件
    zip_util.compress_file(r'C:\path\to\file.txt', r'C:\path\to\file.zip')

    # 压缩多个文件
    zip_util.compress_files([r'C:\path\to\file1.txt', r'C:\path\to\file2.txt'], r'C:\path\to\files.zip')
