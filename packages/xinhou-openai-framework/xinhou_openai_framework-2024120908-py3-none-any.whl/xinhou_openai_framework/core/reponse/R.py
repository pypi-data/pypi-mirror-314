import json
from datetime import datetime
from typing import Optional

from fastapi import Request
from starlette.responses import JSONResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from xinhou_openai_framework.core.exception.CodeEnum import CodeEnum
from xinhou_openai_framework.core.reponse.ReturnData import ReturnData
from xinhou_openai_framework.pages.Paginate import Paginate


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        return super().default(obj)


class R:
    """
    返回响应对象
    """

    @staticmethod
    def serialize_item(item):
        if isinstance(item, dict):
            return {k: R.serialize_item(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [R.serialize_item(i) for i in item]
        elif isinstance(item, datetime):
            return item.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(item, bytes):
            return item.decode('utf-8', errors='replace')
        elif hasattr(item, '__dict__'):
            return {k: R.serialize_item(v) for k, v in item.__dict__.items() if not k.startswith('_')}
        else:
            return item

    @staticmethod
    def serialize_data(data):
        if data is None:
            return None
        if isinstance(data, Paginate):
            return ReturnData.page_to_dict(data)
        elif isinstance(data, bool):
            return data
        elif isinstance(data, list):
            return [R.serialize_item(item) for item in data]
        else:
            return R.serialize_item(data)

    @staticmethod
    def SUCCESS(data: Optional[dict] = None):
        return R.jsonify(CodeEnum.SUCCESS, data=data)

    @staticmethod
    def NO_PARAMETER():
        return R.jsonify(CodeEnum.NO_PARAMETER)

    @staticmethod
    def PARAMETER_ERR(data=None):
        return R.jsonify(CodeEnum.PARAMETER_ERROR, data=data)

    @staticmethod
    def OTHER_LOGIN():
        return R.jsonify(CodeEnum.OTHER_LOGIN)

    @staticmethod
    def AUTH_ERR():
        return R.jsonify(CodeEnum.UNAUTHORIZED)

    @staticmethod
    def TOKEN_ERROR():
        return R.jsonify(CodeEnum.ERROR_TOKEN)

    @staticmethod
    def REQUEST_ERROR():
        return R.jsonify(CodeEnum.BAD_REQUEST)

    @staticmethod
    def ID_NOT_FOUND():
        return R.jsonify(CodeEnum.ID_NOT_FOUND)

    @staticmethod
    def SAVE_ERROR():
        return R.jsonify(CodeEnum.DB_ERROR)

    @staticmethod
    def UPDATE_ERROR():
        return R.jsonify(CodeEnum.DB_ERROR)

    @staticmethod
    def DELETE_ERROR():
        return R.jsonify(CodeEnum.DB_ERROR)

    @staticmethod
    def FILE_NO_FOUND():
        return R.jsonify(CodeEnum.FILE_NOT_FOUND)

    @staticmethod
    def ERROR_FILE_TYPE():
        return R.jsonify(CodeEnum.ERROR_FILE_TYPE)

    @staticmethod
    def UPLOAD_FAILD():
        return R.jsonify(CodeEnum.UPLOAD_FAILED)

    @staticmethod
    def OVER_SIZE():
        return R.jsonify(CodeEnum.OVER_SIZE)

    @staticmethod
    def SERVER_ERROR():
        return R.jsonify(CodeEnum.INTERNAL_SERVER_ERROR)

    @staticmethod
    def template(request: Request, dir_name, tpl_file, data=None):
        templates = Jinja2Templates(directory="templates/default/" + dir_name)
        serialized_data = R.serialize_data(data)
        return templates.TemplateResponse(
            tpl_file, {
                "request": request,
                "base_url": request.base_url,  # 基本请求路径
                "data": serialized_data
            })

    @staticmethod
    def jsonify(code_enum: CodeEnum, data=None):
        serialized_data = R.serialize_data(data)

        content = {
            "code": code_enum.value['code'],
            "msg": code_enum.value['msg'],
            "data": serialized_data
        }

        # 使用 CustomJSONEncoder 手动进行 JSON 编码
        json_str = json.dumps(content, cls=CustomJSONEncoder)

        # 返回 JSONResponse，使用编码后的 JSON 字符串
        return JSONResponse(content=json.loads(json_str))

    @staticmethod
    def Streaming(auto_generate_function):
        return StreamingResponse(auto_generate_function(), headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
        }, media_type="text/event-stream")
