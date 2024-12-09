import asyncio

import httpx
from loguru import logger


class AsyncReqUtil:
    def __init__(self, base_url):
        if not base_url.startswith('http://') and not base_url.startswith('https://'):
            base_url = f'http://{base_url}'
        self.base_url = base_url
        self.headers = {}
        self.timeout = None

    async def set_headers(self, headers_list, convert_underscores=True):
        self.convert_underscores = convert_underscores
        for header_dict in headers_list:
            for key, value in header_dict.items():
                new_key = key.replace('_', '-') if self.convert_underscores else key
                str_value = str(value) if not isinstance(value, (str, bytes)) else value
                self.headers[new_key] = str_value

    async def set_timeout(self, timeout):
        self.timeout = timeout

    async def get(self, endpoint, params=None):
        async with httpx.AsyncClient() as client:
            url = self.base_url + endpoint
            response = await client.get(url, params=params, headers=self.headers, timeout=self.timeout)
            return response

    async def post(self, endpoint, data=None, json=None):
        async with httpx.AsyncClient() as client:
            url = self.base_url + endpoint
            response = await client.post(url, data=data, json=json, headers=self.headers, timeout=self.timeout)
            return response

    async def put(self, endpoint, data=None, json=None):
        async with httpx.AsyncClient() as client:
            url = self.base_url + endpoint
            response = await client.put(url, data=data, json=json, headers=self.headers, timeout=self.timeout)
            return response

    async def delete(self, endpoint):
        async with httpx.AsyncClient() as client:
            url = self.base_url + endpoint
            response = await client.delete(url, headers=self.headers, timeout=self.timeout)
            return response


async def main():
    base_url = "http://test-openai-api-v5.xinhouai.com"
    req_util = AsyncReqUtil(base_url)

    headers = [
        {"tenant-id": "888888"},
        {"classify-type": "role"},
        {"classify-id": "888888"},
        {"platform-code": "pt"}
    ]

    results = await asyncio.gather(*[
        req_util.set_headers(headers),
        req_util.get("/health", params={"username": "zhangsan", "password": "123456"})
    ])
    response_object = results[1].json()
    logger.info(response_object)

    # 其他请求示例
    # response = await req_util.get("/endpoint", params={"key": "value"})
    # response = await req_util.put("/endpoint/123", json={"key": "updated_value"})
    # response = await req_util.delete("/endpoint/123")


# 示例用法
if __name__ == "__main__":
    asyncio.run(main())
