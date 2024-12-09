# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
功能描述
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   ReturnData.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 09:59   shenpeng   1.0         None
"""
from xinhou_openai_framework.pages.Pager import Pager
from xinhou_openai_framework.pages.Paginate import Paginate
from xinhou_openai_framework.utils.ObjUtil import ObjUtil
from xinhou_openai_framework.utils.QueryUtil import QueryUtil


class ReturnData:
    """
    返回数据对象（支持分页转字典）
    """

    @staticmethod
    def page_to_dict(paginate: Paginate):
        return {
            "content": QueryUtil.query_set_to_dict(paginate.items),
            "pager": {
                "page_num": paginate.page_num,
                "page_size": paginate.page_size,
                "total_page": paginate.pages,
                "total_record": paginate.counts
            },
            "sorter": {
                "orders": ObjUtil.obj_to_dict(paginate.orders)
            }
        }

    @staticmethod
    def result_to_dict(datas, pager: Pager, sorter):
        return {
            "content": datas,
            "pager": {
                "page_num": pager.page_num,
                "page_size": pager.page_size,
                "total_page": pager.pages,
                "total_record": pager.counts
            },
            "sorter": {
                "orders": sorter.orders
            }
        }
