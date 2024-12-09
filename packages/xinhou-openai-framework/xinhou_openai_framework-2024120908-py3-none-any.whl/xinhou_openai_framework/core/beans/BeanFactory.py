import inspect

from xinhou_openai_framework.core.annotations.BeanAnnotations import Dao, Service, Bean
from xinhou_openai_framework.core.beans.BeansContext import BeansContext


class BeanEntity:
    def __init__(self, name):
        self.name = name

    def init(self):
        print(f"Bean {self.name} 初始化")

    def business_logic(self):
        print(f"执行 {self.name} 的业务逻辑")

    def destroy(self):
        print(f"Bean {self.name} 销毁")


class BeanProxy:
    def __init__(self, bean_class, name):
        self.bean_class = bean_class
        self.name = name

    def init(self):
        print(f"Bean {self.name} 初始化（代理）")
        self.bean = self.bean_class(self.name)
        self.bean.init()

    def business_logic(self):
        if hasattr(self, 'bean'):
            self.bean.business_logic()
        else:
            raise ValueError("Bean 还未初始化")

    def destroy(self):
        if hasattr(self, 'bean'):
            self.bean.destroy()
        else:
            raise ValueError("Bean 还未初始化")


@Bean
class ExampleBean:
    def __init__(self):
        pass

    def do_something(self):
        print("ExampleBean Doing something...")


@Dao
class ExampleDao:
    def __init__(self):
        self.example_bean = BeansContext.get_instance('ExampleBean')

    def do_something(self):
        print("ExampleDao Doing something...")
        self.example_bean.do_something()


@Service
class ExampleService:
    def __init__(self):
        self.example_dao = BeansContext.get_instance('ExampleDao')

    def do_something(self):
        print("ExampleService Doing something...")
        self.example_dao.do_something()


if __name__ == '__main__':
    example_service = BeansContext.get_instance('ExampleService')
    example_service.do_something()
