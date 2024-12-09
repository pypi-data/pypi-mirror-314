import nacos
from loguru import logger

from loguru import logger
from xinhou_openai_framework.utils.NetUtils import NetUtils


class NacosManager:
    """
    用于与Nacos服务器交互的辅助类。

    Attributes:
        service_name (str): 服务的名称。
        service_port (int): 服务运行的端口。
        service_group (str): 服务所属的组。
    """

    def __init__(self, server_endpoint, namespace_id, username=None, password=None):
        """
        初始化 NacosHelper 实例。

        Args:
            server_endpoint (str): Nacos服务器的端点。
            namespace_id (str): 要使用的命名空间ID。
            username (str, optional): 用于身份验证的用户名。默认为None。
            password (str, optional): 用于身份验证的密码。默认为None。
        """
        self.client = nacos.NacosClient(
            server_addresses=server_endpoint,
            namespace=namespace_id,
            username=username,
            password=password
        )
        self.endpoint = server_endpoint
        self.service_ip = NetUtils.get_host_ip()

    def register(self):
        """向Nacos服务器注册服务。"""
        self.client.add_naming_instance(
            self.service_name,
            self.service_ip,
            self.service_port,
            group_name=self.service_group,
            metadata="preserved.register.source=XINHOU_OPENAI"
        )

    def unregister(self):
        """从Nacos服务器注销服务。"""
        self.client.remove_naming_instance(
            self.service_name,
            self.service_ip,
            self.service_port
        )

    def discover(self):
        instances = self.client.select_instance(self.service_name)
        if instances:
            return instances[0]['ip'], instances[0]['port']
        else:
            print("No instances found")
            return None

    def set_service(self, service_name, service_port, service_group):
        """
        设置服务信息。

        Args:
            service_name (str): 服务的名称。
            service_port (int): 服务运行的端口。
            service_group (str): 服务所属的组。
        """
        self.service_name = service_name
        self.service_port = service_port
        self.service_group = service_group

    async def beat_callback(self):
        """向Nacos服务器发送心跳。"""
        try:
            self.client.send_heartbeat(
                service_name=self.service_name,
                ip=self.service_ip,
                port=self.service_port,
                group_name=self.service_group,
                metadata="preserved.register.source=XINHOU_OPENAI"
            )
        except Exception as e:
            logger.error("[Send beat message exception.]:{}".format(e))

    def load_conf(self, data_id, group):
        """
        从Nacos服务器加载配置。

        Args:
            data_id (str): 要加载的数据的ID。
            group (str): 数据所属的组。

        Returns:
            str: 配置数据。
        """
        return self.client.get_config(data_id=data_id, group=group, no_snapshot=True)

    def add_conf_watcher(self, data_id, group, callback):
        """
        添加配置观察器以监视配置更改。

        Args:
            data_id (str): 要监视的数据的ID。
            group (str): 数据所属的组。
            callback (function): 配置更改时要调用的回调函数。
        """
        self.client.add_config_watcher(data_id=data_id, group=group, cb=callback)
