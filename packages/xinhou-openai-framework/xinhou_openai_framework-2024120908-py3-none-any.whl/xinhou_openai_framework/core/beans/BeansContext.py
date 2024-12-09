from typing import Any, Optional
from threading import Lock


class BeansContext:
    _instances: dict = {}
    _lock: Lock = Lock()

    @classmethod
    def add_instance(cls, name: str, instance: Any) -> None:
        """Add an instance to the context."""
        with cls._lock:
            cls._instances[name] = instance

    @classmethod
    def get_instance(cls, name: str) -> Optional[Any]:
        """Get an instance from the context."""
        with cls._lock:
            return cls._instances.get(name)

    @classmethod
    def remove_instance(cls, name: str) -> Optional[Any]:
        """Remove an instance from the context."""
        with cls._lock:
            return cls._instances.pop(name, None)

    @classmethod
    def clear(cls) -> None:
        """Clear all instances from the context."""
        with cls._lock:
            cls._instances.clear()


# 使用示例
class DemoClass:
    def __init__(self, name: str):
        self.name = name


if __name__ == '__main__':
    # 在初始化阶段添加实例到 ApplicationContext
    obj1 = DemoClass("Object 1")
    BeansContext.add_instance("obj1", obj1)

    obj2 = DemoClass("Object 2")
    BeansContext.add_instance("obj2", obj2)

    # 在其他地方获取实例
    instance1 = BeansContext.get_instance("obj1")
    print(instance1.name)  # 输出: Object 1

    # 在不再需要时移除实例
    BeansContext.remove_instance("obj1")

    # 清空 ApplicationContext
    BeansContext.clear()
