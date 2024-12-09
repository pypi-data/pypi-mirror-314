# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
代码生成工具
----------------------------------------------------
@Project :   marmot-xinhou-openai-framework  
@File    :   GenerateCodeController.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/8 13:35   shenpeng   1.0         None
"""
import time

from fastapi import APIRouter
from fastapi.params import Depends
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from sqlalchemy import text
from sqlalchemy.orm import Session

from xinhou_openai_framework.core.db.DatabaseManager import DatabaseManager
from xinhou_openai_framework.core.reponse.R import R
from xinhou_openai_framework.utils.PathUtil import PathUtil
from xinhou_openai_framework.utils.StrUtil import StrUtil

code_generater_api = APIRouter()


@code_generater_api.get('/common/code/generater',
                        tags=["tools"],
                        summary="自动生成代码接口",
                        description="通过数据结构自动推断生成模型")
async def generater(db: Session = Depends(DatabaseManager().get_session)):
    logger.info("[GenerateCodeTool][Begin]")
    # 生成表白名单(空生成全部)
    tables_white = [
        'llm_api_key',
        'llm_config',
        'llm_model',
        'llm_scene',
        'llm_version'
    ]
    # 获取所有表
    tables_sql = text('''
            SELECT table_name, engine, table_comment FROM information_schema.tables WHERE table_schema = (SELECT DATABASE())
        ''')
    tables_stock_list = db.execute(tables_sql)
    tables_row_proxy_list = tables_stock_list.fetchall()
    if not tables_row_proxy_list:
        return None
    tables_data_dict = [dict(zip(tables_stock_list.keys(), tables_row_proxy)) for tables_row_proxy in
                        tables_row_proxy_list]

    tables = []
    for table in tables_data_dict:
        if len(tables_white) > 0 and table["table_name"] in tables_white or tables_white is None:
            # 基本配置信息
            table["project_name"] = "xinhou-openai-framework"
            table["project_path"] = "/Users/shenpeng/Works/workspaces-git/" + table["project_name"]
            table["module_name"] = "admin"
            table["module_path"] = table["project_path"] + "/apps/" + table["module_name"]
            table["package_model"] = "common.entity"
            table["package_service"] = "common.service"
            table["package_schema"] = "apps." + table["module_name"] + ".schema"
            table["package_controller"] = "apps." + table["module_name"] + ".controller"

            table["class_name"] = StrUtil.to_upper_camel_case(StrUtil.sub_str_after(table["table_name"], "t_", True))
            table["clazz_name"] = StrUtil.to_lower_camel_case(StrUtil.sub_str_after(table["table_name"], "t_", True))
            table["file_name"] = table["class_name"] + ".py"

            table["blueprint_name"] = table["module_name"] + ":" + table["clazz_name"]
            table["blueprint_url_prefix"] = "/" + table["module_name"] + "/" + table["clazz_name"]

            # 文件注释信息
            table["contact"] = "sp_hrz@qq.com"
            table["modify_time"] = time.strftime("%Y/%m/%d %H:%M", time.localtime())
            table["author"] = "peng.shen"
            table["version"] = "v1.0.0"
            table["desciption"] = None

            # 忽略字段
            table["ignore_fields"] = ["id", "create_by", "created_at", "update_by", "updated_at", "remart"]

            # 循环获取表-》字段列表-》转换成属性字段字典
            fields_sql = text('''
                        SELECT column_name,column_type,column_default,column_comment,is_nullable, column_key, extra,ordinal_position FROM information_schema.columns WHERE table_name = :table_name AND table_schema = (SELECT DATABASE()) order by ordinal_position
                    ''')
            fields_stock_list = db.execute(fields_sql, {"table_name": table['table_name']})
            fields_row_proxy_list = fields_stock_list.fetchall()
            if not fields_row_proxy_list:
                return None
            fields_data_dict = [dict(zip(fields_stock_list.keys(), fields_row_proxy)) for fields_row_proxy in
                                fields_row_proxy_list]

            table["fields"] = fields_data_dict
            tables.append(table)

    # check_relation_model(table)

    # 解析字段-》生成模型 -》service》Controller
    env = Environment(loader=FileSystemLoader("templates"))
    # 注册自定义函数到模板jinja2环境
    env.filters["mapping_column_type"] = mapping_column_type
    env.filters["mapping_schema_column_type"] = mapping_schema_column_type
    env.filters["check_column_default"] = check_column_default
    env.filters["check_schema_column_default"] = check_schema_column_default

    for tb in tables:
        base_path = tb["project_path"]
        apps_module_path = tb["module_path"]
        PathUtil.not_exists_mkdir(apps_module_path)

        # 生成model
        with open(PathUtil.not_exists_mkdir(base_path + "/common/entity/") + tb["class_name"] + ".py",
                  "w") as out:
            template = env.get_template("code/Model.tpl.html")
            model_code_content = template.render({"table": tb})
            out.write(model_code_content)  # 写入模板 生成代码
            out.close()

        # 生成service
        with open(PathUtil.not_exists_mkdir(base_path + "/common/service/") + tb["class_name"] + "Service.py",
                  "w") as out:
            template = env.get_template("code/Service.tpl.html")
            service_code_content = template.render({"table": tb})
            out.write(service_code_content)  # 写入模板 生成代码
            out.close()

        # 生成schema
        with open(PathUtil.not_exists_mkdir(apps_module_path + "/schema/") + tb["class_name"] + "Schema.py",
                  "w") as out:
            template = env.get_template("code/Schema.tpl.html")
            schema_code_content = template.render({"table": tb})
            out.write(schema_code_content)  # 写入模板 生成代码
            out.close()

        # 生成controller
        with open(PathUtil.not_exists_mkdir(apps_module_path + "/controller/") + tb["class_name"] + "Controller.py",
                  "w") as out:
            template = env.get_template("code/Controller.tpl.html")
            controller_code_content = template.render({"table": tb})
            out.write(controller_code_content)  # 写入模板 生成代码
            out.close()

    logger.info("[GenerateCodeTool][End]")
    return R.SUCCESS(tables)


def mapping_column_type(column_type):
    # 属性映射
    # 1、Integer：整形，映射到数据库中是int类型
    # 2、Float：浮点类型，映射到数据库中是float类型。它占据的32位
    # 3、Double：双精度浮点类型，映射到数据库中是double类型，占据64位
    # 4、String：可变字符类型，映射到数据库中是varchar类型
    # 5、Boolean：布尔类型，映射到数据库中是tinyint类型
    # 6、Decimal：定点类型，是专门为了解决浮点类型精度丢失的问题的，一般作用于金钱类型
    # 7、Enum：枚举类型，指定某个字段只能是枚举中指定的几个值，不能为其他值
    # 8、Date：存储时间，只能存储年月日，映射到数据库中是date类型
    # 9、Datetime：存储时间，可以存储年月日时分秒
    # 10、Time：存储时间，存储时分秒
    # 11、Text：存储长字符串，映射到数据库是text类型
    # 12、Longtext：长文本类型，映射到数据库中是longtext类型
    if StrUtil.find_is_exists(column_type, "varchar"):
        return StrUtil.replace(column_type, "varchar", "String")
    if StrUtil.find_is_exists(column_type, "int") or StrUtil.find_is_exists(column_type, "tinyint"):
        return "Integer"
    if StrUtil.find_is_exists(column_type, "long") or StrUtil.find_is_exists(column_type, "bigint"):
        return "BigInteger"
    if StrUtil.find_is_exists(column_type, "timestamp"):
        return "TIMESTAMP"
    if StrUtil.find_is_exists(column_type, "text"):
        return "Text"
    if StrUtil.find_is_exists(column_type, "longtext"):
        return "Longtext"
    if StrUtil.find_is_exists(column_type, "decimal"):
        return StrUtil.replace(column_type, "decimal", "Numeric")
    return column_type


def mapping_schema_column_type(column_type):
    if StrUtil.find_is_exists(column_type, "varchar") \
            or StrUtil.find_is_exists(column_type, "text") \
            or StrUtil.find_is_exists(column_type, "longtext"):
        return "str"
    if StrUtil.find_is_exists(column_type, "int") \
            or StrUtil.find_is_exists(column_type, "tinyint") \
            or StrUtil.find_is_exists(column_type, "long") \
            or StrUtil.find_is_exists(column_type, "bigint"):
        return "int"
    if StrUtil.find_is_exists(column_type, "timestamp"):
        return "datetime"
    if StrUtil.find_is_exists(column_type, "decimal"):
        return "Decimal"
    return column_type


def check_column_default(column_default):
    # 检测列默认值
    if column_default:
        if StrUtil.find(column_default, "CURRENT_TIMESTAMP") != -1:
            return ", server_default=func.now()"
        return ", default='" + column_default + "'"
    return ""


def check_schema_column_default(column_default):
    # 检测列默认值
    if column_default:
        if StrUtil.find(column_default, "CURRENT_TIMESTAMP") != -1:
            return ""
        return ", default='" + column_default + "'"
    return ""


def check_column_comment(column_comment):
    # 检查并设置默认值
    pass


def check_relation_model(table):
    # 检查模型是否有关联对象
    relations = []
    ref_class_list = table["class_name"]
    for field in table["fields"]:
        if StrUtil.find_is_exists(field['column_comment'], "join"):
            logger.info(field['column_comment'])
            ref_class_list = ref_class_list + ", " + StrUtil.to_upper_camel_case(
                StrUtil.sub_str_after(table["table_name"], "t_"))
            relations.append({
                "main_class": table["class_name"],
                "relation_class": StrUtil.to_upper_camel_case(StrUtil.sub_str_after(table["table_name"], "t_")),
                "relation_clazz": StrUtil.to_lower_camel_case(StrUtil.sub_str_after(table["table_name"], "t_")),
                "join_field": field['column_name'],
            })
    table["relation"] = {
        "ref_class_list": ref_class_list,
        "refs": relations
    }
