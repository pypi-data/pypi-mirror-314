import requests
import yaml


class NacosOpenApiClientManager:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.access_token = None
        if username and password:
            self.auth_login()

    def _check_token(self):
        if not self.access_token:
            self.auth_login()

    def _request(self, method, path, **kwargs):
        self._check_token()  # 检查 token 是否存在或过期
        url = f"{self.base_url}{path}"
        try:
            if self.access_token is not None:
                kwargs["params"]["accessToken"] = self.access_token
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Nacos Request Error: {e}")
            return None

    def auth_login(self):
        """
        使用用户名和密码登录 Nacos，获取访问令牌
        """
        response = self.session.post(f"{self.base_url}/nacos/v1/auth/login",
                                     params={"username": self.username, "password": self.password})
        body = response.json()
        self.access_token = body.get("accessToken")

    # 配置管理接口
    def get_config(self, data_id, group, namespace_id=None):
        """
        获取配置
        :param data_id: 配置的数据ID
        :param group: 配置的分组
        :param namespace_id: 命名空间，默认为public与 ''相同
        :return: 返回获取到的配置信息
        """
        path = f"/nacos/v1/cs/configs"
        params = {"dataId": data_id, "group": group, "tenant": namespace_id}
        response = self._request("GET", path, params=params)
        return response.content

    def publish_config(self, data_id, group, content, namespace_id=None):
        """
        发布配置
        :param data_id: 配置的数据ID
        :param group: 配置的分组
        :param content: 配置内容
        :param namespace_id: 命名空间，默认为public与 ''相同
        :return: 返回发布配置的结果
        """
        path = f"/nacos/v1/cs/configs"
        payload = {"dataId": data_id, "group": group, "content": content, "tenant": namespace_id}
        response = self._request("POST", path, json=payload)
        return response.json()

    def delete_config(self, data_id, group, namespace_id=None):
        """
        删除配置
        :param data_id: 配置的数据ID
        :param group: 配置的分组
        :param namespace_id: 命名空间，默认为public与 ''相同
        :return: 返回删除配置的结果
        """
        path = f"/nacos/v1/cs/configs"
        params = {"dataId": data_id, "group": group, "tenant": namespace_id}
        response = self._request("DELETE", path, params=params)
        return response.json()

    # 实例注册接口
    def register_instance(self, namespace, serviceName, ip, port, clusterName=None, metadata=None):
        """
        注册实例
        :param namespace: 命名空间
        :param serviceName: 服务名称
        :param ip: 实例 IP
        :param port: 实例端口
        :param clusterName: 集群名称
        :param metadata: 实例元数据
        :return: 返回注册实例的结果
        """
        path = f"/nacos/v1/ns/instance"
        payload = {
            "namespaceId": namespace,
            "serviceName": serviceName,
            "ip": ip,
            "port": port,
            "clusterName": clusterName,
            "metadata": metadata
        }
        response = self._request("POST", path, json=payload)
        return response.json()

    # 实例更新接口
    def update_instance(self, namespace, serviceName, ip, port, clusterName=None, metadata=None):
        """
        更新实例信息
        :param namespace: 命名空间
        :param serviceName: 服务名称
        :param ip: 实例 IP
        :param port: 实例端口
        :param clusterName: 集群名称
        :param metadata: 实例元数据
        :return: 返回更新实例的结果
        """
        path = f"/nacos/v1/ns/instance"
        payload = {
            "namespaceId": namespace,
            "serviceName": serviceName,
            "ip": ip,
            "port": port,
            "clusterName": clusterName,
            "metadata": metadata
        }
        response = self._request("PUT", path, json=payload)
        return response.json()

    # 实例销毁接口
    def delete_instance(self, namespace, serviceName, ip, port, clusterName=None):
        """
        销毁实例
        :param namespace: 命名空间
        :param serviceName: 服务名称
        :param ip: 实例 IP
        :param port: 实例端口
        :param clusterName: 集群名称
        :return: 返回销毁实例的结果
        """
        path = f"/nacos/v1/ns/instance"
        payload = {
            "namespaceId": namespace,
            "serviceName": serviceName,
            "ip": ip,
            "port": port,
            "clusterName": clusterName
        }
        response = self._request("DELETE", path, json=payload)
        return response.json()

    # 实例心跳接口
    def send_heartbeat(self, namespace, serviceName, groupName, ip, port, clusterName=None, metadata=None):
        """
        实例心跳
        :param namespace: 命名空间
        :param serviceName: 服务名称
        :param groupName: 分组名称
        :param ip: 实例 IP
        :param port: 实例端口
        :param clusterName: 集群名称
        :param metadata: 实例元数据
        :return: 返回心跳的结果
        """
        path = f"/nacos/v1/ns/instance/beat"
        payload = {
            "namespaceId": namespace,
            "serviceName": serviceName,
            "groupName": groupName,
            "ip": ip,
            "port": port,
            "clusterName": clusterName,
            "metadata": metadata
        }
        response = self._request("PUT", path, json=payload)
        return response.json()


if __name__ == '__main__':
    # 使用示例
    # 创建 NacosOpenAPIV2 实例
    base_url = "http://127.0.0.1:8848"
    username = "nacos"
    password = "nacos"

    nacos_api = NacosOpenApiClientManager(base_url, username=username, password=password)
    print("Access Token:", nacos_api.access_token)

    # 获取配置示例
    config = nacos_api.get_config(data_id="application-dev.yml",
                                  group="XINHOU_OPENAI_GROUP",
                                  namespace_id="bf534543-5e01-4e34-8621-b09d0b438265")
    print("Retrieved Config:", config)
    # 将字符串转换成字典
    config_dict = yaml.safe_load(config)

    # 将字典格式化成 YAML 格式并打印输出
    formatted_yaml = yaml.dump(config_dict, default_flow_style=False)
    print(formatted_yaml)

    # # 发布配置示例
    # publish_result = nacos_api.publish_config(data_id="example_data", group="example_group", content="test_content")
    # print("Publish Result:", publish_result)
    #
    # # 注册实例示例
    # register_result = nacos_api.register_instance(namespace="example_namespace", serviceName="example_service",
    #                                               ip="127.0.0.1", port=8080)
    # print("Register Instance Result:", register_result)
    #
    # # 更新实例示例
    # update_result = nacos_api.update_instance(namespace="example_namespace", serviceName="example_service",
    #                                           ip="127.0.0.1", port=8080)
    # print("Update Instance Result:", update_result)
    #
    # # 销毁实例示例
    # delete_result = nacos_api.delete_instance(namespace="example_namespace", serviceName="example_service",
    #                                           ip="127.0.0.1", port=8080)
    # print("Delete Instance Result:", delete_result)
    #
    # # 发送心跳示例
    # heartbeat_result = nacos_api.send_heartbeat(namespace="example_namespace", serviceName="example_service",
    #                                             groupName="example_group", ip="127.0.0.1", port=8080)
    # print("Heartbeat Result:", heartbeat_result)
