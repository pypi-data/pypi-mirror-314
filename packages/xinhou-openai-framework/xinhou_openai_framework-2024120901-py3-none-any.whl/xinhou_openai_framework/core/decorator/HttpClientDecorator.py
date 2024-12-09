import logging
from functools import wraps
import requests
from retry import retry


class HttpClient:
    """
    HTTP 客户端类，用于发送 HTTP 请求。
    """

    def __init__(self, base_url, retry_times=3, retry_delay=1, retry_backoff=2, timeout=5):
        """
        初始化 HTTP 客户端。

        Args:
            base_url (str): 请求的基础 URL。
            retry_times (int): 重试次数，默认为 3。
            retry_delay (int): 重试延迟时间，默认为 1 秒。
            retry_backoff (int): 重试指数倍增时间，默认为 2。
            timeout (int): 请求超时时间，默认为 5 秒。
        """
        self.base_url = base_url
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff
        self.timeout = timeout

    def request(self, method, path, headers=None, json_data=None):
        """
        发送 HTTP 请求。

        Args:
            method (str): 请求方法，如 "GET"、"POST" 等。
            path (str): 请求路径。
            headers (dict): 请求头，默认为 None。
            json_data (dict): JSON 格式的请求数据，默认为 None。

        Returns:
            dict: 包含响应数据的字典。
        """

        @retry(exceptions=requests.exceptions.RequestException, tries=self.retry_times, delay=self.retry_delay,
               backoff=self.retry_backoff)
        def _request():
            url = self.base_url + path
            try:
                response = requests.request(method, url, headers=headers, json=json_data, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                return None

        return _request()


def http_client(base_url, path, method="GET", headers={"Content-Type": "application/json"}, json_data={}, retry_times=3,
                retry_delay=1, retry_backoff=2, timeout=5):
    """
    HTTP 客户端装饰器，用于发送 HTTP 请求，并将响应数据作为参数传递给被装饰的函数。

    Args:
        base_url (str): 请求的基础 URL。
        path (str): 请求路径。
        method (str): 请求方法，默认为 "GET"。
        headers (dict): 请求头，默认为 {"Content-Type": "application/json"}。
        json_data (dict): JSON 格式的请求数据，默认为空字典。
        retry_times (int): 重试次数，默认为 3。
        retry_delay (int): 重试延迟时间，默认为 1 秒。
        retry_backoff (int): 重试指数倍增时间，默认为 2。
        timeout (int): 请求超时时间，默认为 5 秒。

    Returns:
        function: 装饰器函数。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = HttpClient(base_url, retry_times, retry_delay, retry_backoff, timeout)

            # 提取调用方式二中传入的 headers 和 json_data 参数，如果没有传入则使用默认值
            headers_kwargs = kwargs.pop('headers', headers)
            json_data_kwargs = kwargs.pop('json_data', json_data)

            # 使用调用方式二中传入的参数调用请求方法
            response_data = client.request(method=method, path=path,
                                           headers=headers_kwargs, json_data=json_data_kwargs)
            # 将响应数据作为参数传递给被装饰的函数
            kwargs["response_data"] = response_data
            return func(*args, **kwargs)

        return wrapper

    return decorator


class OpenaiRemoteService:
    """
    OpenAI 远程服务类，用于调用远程服务。
    """

    @staticmethod
    @http_client("http://127.0.0.1:8000", path="/api/summary/callback", json_data={
        "summary_process_key": "1",
        "summary_process_result": "测试"
    }, headers={
        "tenant_id": '888888',
        "classify_type": 'role',
        "classify_id": '888888',
        "platform_code": 'pt'
    }, method="POST", retry_times=3, retry_delay=1, retry_backoff=2)
    def health(response_data, **kwargs):
        """
        健康检查函数。

        Args:
            response_data (dict): 响应数据。
            **kwargs: 关键字参数。

        Returns:
            None
        """
        if response_data:
            # 在这里处理业务逻辑，可以通过 res_data 获取响应数据
            print("Received response data:", response_data)
        else:
            print("No response data received.")


def main():
    # 调用方式默认使用@http_client注解时通过header 和json_data等参数设置
    OpenaiRemoteService.health()

    # 调用方式二
    OpenaiRemoteService.health(json_data={
        "summary_process_key": "2",
        "summary_process_result": "测试"
    }, headers={
        "tenant_id": '888888',
        "classify_type": 'role',
        "classify_id": '888888',
        "platform_code": 'pt'
    }, method="POST")


if __name__ == "__main__":
    main()
