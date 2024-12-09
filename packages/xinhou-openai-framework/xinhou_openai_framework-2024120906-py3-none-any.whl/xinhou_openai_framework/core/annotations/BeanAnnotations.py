import inspect

from xinhou_openai_framework.core.beans.BeansContext import BeansContext


class BeanFactory:
    @classmethod
    def before_instantiation(cls):
        print("Before instantiation...")

    @classmethod
    def after_instantiation(cls):
        print("After instantiation...")

    @classmethod
    def create_bean(cls, target_class):
        cls.before_instantiation()
        # 获取构造函数参数列表
        constructor_params = inspect.signature(target_class.__init__).parameters
        # 根据参数列表获取依赖实例
        dependencies = {param_name: BeansContext.get_instance(param_name) for param_name in constructor_params if
                        param_name != 'self'}
        # 实例化目标类，并将依赖实例作为参数传递
        instance = target_class(**dependencies)
        cls.after_instantiation()
        # 将实例化目标类，放入Beans上下文中
        BeansContext.add_instance(target_class.__name__, instance)
        return instance


def Bean(cls):
    return BeanFactory.create_bean(cls)


def Dao(cls):
    return BeanFactory.create_bean(cls)


def Service(cls):
    return BeanFactory.create_bean(cls)
