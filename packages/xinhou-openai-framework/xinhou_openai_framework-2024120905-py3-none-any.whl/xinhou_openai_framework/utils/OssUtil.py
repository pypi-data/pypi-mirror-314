# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   OssUtil.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/17 17:02   shenpeng   1.0         None
"""
from io import BytesIO

import requests
from loguru import logger


import oss2
from typing import Union, List

from xinhou_openai_framework.core.context.model.AppContext import AppContext
from xinhou_openai_framework.core.context.model.SystemContext import ctx
from xinhou_openai_framework.utils.PathUtil import PathUtil


class OssFile:
    def __init__(self, local_path, oss_key, signed_url):
        self.local_path = local_path
        self.oss_key = oss_key
        self.signed_url = signed_url


class OssResult:
    def __init__(self, success, message=None, data=None):
        self.success = success
        self.message = message
        self.data = data


class UploadedFileInfo:
    def __init__(self, file_id, file_name, file_size, oss_key, signed_url):
        self.file_id = file_id
        self.file_name = file_name
        self.file_size = file_size
        self.oss_key = oss_key
        self.signed_url = signed_url


class DownloadedFileInfo:
    def __init__(self, file_id, file_name, file_size, oss_key, local_path):
        self.file_id = file_id
        self.file_name = file_name
        self.file_size = file_size
        self.oss_key = oss_key
        self.local_path = local_path


class OssUtil:
    def __init__(self, endpoint=None, access_key_id=None, access_key_secret=None, bucket_name=None):
        if endpoint is None or access_key_id is None or access_key_secret is None or bucket_name is None:
            context: AppContext = ctx.__getattr__("context")  # 全局变量
            # 阿里云OSS配置信息
            self.endpoint = context.aliyun_oss.endpoint

            # 创建OSS认证和Bucket实例
            self.auth = oss2.Auth(context.aliyun_oss.access_key_id, context.aliyun_oss.access_key_secret)
            self.bucket = oss2.Bucket(self.auth, self.endpoint, context.aliyun_oss.bucket_name)
        else:
            # 阿里云OSS配置信息
            self.endpoint = endpoint

            # 创建OSS认证和Bucket实例
            self.auth = oss2.Auth(access_key_id, access_key_secret)
            self.bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name)

    def upload_file(self, local_file_path, oss_object_key) -> OssResult:
        try:
            # 上传文件到OSS
            self.bucket.put_object_from_file(oss_object_key, local_file_path)
            message = f"已上传 '{local_file_path}' 为 '{oss_object_key}'"
            return OssResult(success=True, message=message)
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def download_file(self, oss_object_key, local_file_path) -> OssResult:
        try:
            # 从OSS下载文件
            self.bucket.get_object_to_file(oss_object_key, local_file_path)
            message = f"已下载 '{oss_object_key}' 为 '{local_file_path}'"
            return OssResult(success=True, message=message,
                             data={"oss_object_key": oss_object_key,
                                   "local_file_path": PathUtil.get_root_path() + "/" + local_file_path})
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def get_object(self, oss_object_key, local_file_path=None) -> Union[DownloadedFileInfo, OssResult]:
        try:
            # 查询单个文件并返回下载文件信息
            object_info = self.bucket.get_object(oss_object_key)
            file_id = object_info.request_id
            file_name = oss_object_key.split('/')[-1]
            file_size = object_info.content_length
            signed_url = self.bucket.sign_url('GET', oss_object_key, 60)

            if local_file_path:
                self.bucket.get_object_to_file(oss_object_key, local_file_path)
                downloaded_file_info = DownloadedFileInfo(file_id, file_name, file_size, oss_object_key,
                                                          local_file_path)
                return OssResult(success=True,
                                 data=OssFile(local_path=downloaded_file_info.local_path, oss_key=oss_object_key,
                                              signed_url=signed_url))
            else:
                return OssResult(success=True,
                                 data=OssFile(local_path=None, oss_key=oss_object_key, signed_url=signed_url))
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def read_object_bytes(self, oss_object_key) -> Union[bytes, OssResult]:
        try:
            # 从OSS读取文件内容并返回字节数据
            result = self.bucket.get_object(oss_object_key)
            content = result.read()
            return content
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def list_objects(self, prefix=None) -> OssResult:
        object_list: List[OssFile] = []
        try:
            # 列出满足查询条件的OSS对象并生成签名URL
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
                signed_url = self.bucket.sign_url('GET', obj.key, 60)
                oss_file = OssFile(local_path=None, oss_key=obj.key, signed_url=signed_url)
                object_list.append(oss_file)
            return OssResult(success=True, data=object_list)
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def delete_object(self, oss_object_key) -> OssResult:
        try:
            # 从OSS中删除对象
            self.bucket.delete_object(oss_object_key)
            message = f"已删除 '{oss_object_key}'"
            return OssResult(success=True, message=message)
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

    def upload_image_from_url(self, image_url, oss_object_key) -> OssResult:
        try:
            # 下载图片
            response = requests.get(image_url)
            if response.status_code == 200:
                image_content = BytesIO(response.content)
                # 上传图片到OSS
                self.bucket.put_object(oss_object_key, image_content)
                message = f"已上传网络图片 '{image_url}' 为 '{oss_object_key}'"
                return OssResult(success=True, message=message)
            else:
                return OssResult(success=False,
                                 message=f"Failed to download image. Status code: {response.status_code}")
        except oss2.exceptions.OssError as e:
            return OssResult(success=False, message=str(e))

if __name__ == '__main__':
    # 初始化OssUtil
    endpoint = 'https://oss-cn-shanghai.aliyuncs.com'
    access_key_id = 'LTAI5tEXLTanjHcjZnZpDVG9'
    access_key_secret = 'YRqH5MOMTGADn5NF9noUXbBwlZCWNJ'
    bucket_name = 'wechat-luobo'
    oss_util = OssUtil(endpoint, access_key_id, access_key_secret, bucket_name)

    # 示例用法
    # local_file_path = '/Users/shenpeng/Downloads/《大乘入楞伽经》（简体注音版）.docx'
    # oss_object_key = 'static/uploads/888888_prompt_888888/606a9ec248aa11eeb1ae3a05baecfa0a.txt'

    # # 上传文件并返回上传结果
    # upload_result = oss_util.upload_file(local_file_path, oss_object_key)
    # if upload_result.success:
    #     logger.info(upload_result.message)
    # else:
    #     logger.info(upload_result.message)
    #
    # # 下载文件并返回下载结果
    # download_result = oss_util.download_file(oss_object_key, '/Users/shenpeng/Downloads/file.docx')
    # if download_result.success:
    #     logger.info(download_result.message)
    # else:
    #     logger.info(download_result.message)

    # 查询单个文件并返回结果
    get_object_result = oss_util.get_object("static/uploads/audio/25198d8565ac40669f376852a24c0e74.mpga")
    if get_object_result.success:
        obj = get_object_result.data
        logger.info(f"OSS Object Key: {obj.oss_key}")
        logger.info(f"Signed URL: {obj.signed_url}")
    else:
        logger.info(get_object_result.message)

    # 列出对象并返回查询结果
    # list_result = oss_util.list_objects(prefix="static/uploads/888888_prompt_888888/")
    # if list_result.success:
    #     for obj in list_result.data:
    #         logger.info(f"OSS Object Key: {obj.oss_key}")
    #         logger.info(f"Signed URL: {obj.signed_url}")
    # else:
    #     logger.info(list_result.message)

    # 删除对象并返回删除结果
    # delete_result = oss_util.delete_object(oss_object_key)
    # if delete_result.success:
    #     logger.info(delete_result.message)
    # else:
    # oss_object_key = 'static/uploads/pt_1_1699858443_test.mp3'
    # 读取在线文件并返回字节数据
    # read_result = oss_util.read_object_bytes(oss_object_key)
    # if isinstance(read_result, bytes):
    #     # 处理字节数据，比如保存到本地文件或进行其他处理
    #     with open('downloaded_file.txt', 'wb') as f:
    #         f.write(read_result)
    #     logger.info(f"文件内容：\n{read_result.decode('utf-8')}")
    # else:
    #     logger.info(read_result.message)

    # # 示例用法
    # image_url = 'https://example.com/path/to/your/image.jpg'
    # oss_object_key = 'static/uploads/your_uploaded_image.jpg'
    #
    # # 上传网络图片并返回上传结果
    # upload_result = oss_util.upload_image_from_url(image_url, oss_object_key)
    # if upload_result.success:
    #     logger.info(upload_result.message)
    # else:
    #     logger.info(upload_result.message)