import functools

from loguru import logger


class Decorator:
    @staticmethod
    def before(callback):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                callback.before(*args, **kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def after(callback):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                callback.after(result, *args, **kwargs)
                return result

            return wrapper

        return decorator

    @staticmethod
    def after_returning(callback):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                callback.after_returning(result, *args, **kwargs)
                return result

            return wrapper

        return decorator

    @staticmethod
    def after_throwing(callback):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    callback.after_throwing(e, *args, **kwargs)
                    raise

            return wrapper

        return decorator

    @staticmethod
    def around(callback):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logger.info("Before execution (Around)")
                result = callback.around(func, *args, **kwargs)
                logger.info("After execution (Around)")
                return result

            return wrapper

        return decorator


# 示例回调类
class DecoratorCallback:
    @classmethod
    def before(cls, *args, **kwargs):
        logger.info(f"Before execution - Input args: {args}, Input kwargs: {kwargs}")

    @classmethod
    def after(cls, result, *args, **kwargs):
        logger.info(f"After execution - Output result: {result}, Input args: {args}, Input kwargs: {kwargs}")

    @classmethod
    def after_returning(cls, result, *args, **kwargs):
        logger.info(f"After execution - Output result: {result}, Input args: {args}, Input kwargs: {kwargs}")

    @classmethod
    def after_throwing(cls, exception, *args, **kwargs):
        logger.info(f"After throwing exception: {exception}, Input args: {args}, Input kwargs: {kwargs}")

    @classmethod
    def around(cls, func, *args, **kwargs):
        logger.info(f"Inside around_callback - Received function: {func}, Input args: {args}, Input kwargs: {kwargs}")
        result = func(*args, **kwargs)
        return result


decorator = Decorator()


# 示例函数
@decorator.before(DecoratorCallback)
def example_function_before(param1, param2):
    logger.info(f"Inside example_function_before - Received params: {param1}, {param2}")


@decorator.after(DecoratorCallback)
def example_function_after(param1, param2):
    logger.info(f"Inside example_function_after - Received params: {param1}, {param2}")
    return param1 + param2


@decorator.after_returning(DecoratorCallback)
def example_function_after_returning(param1, param2):
    logger.info(f"Inside example_function_after_returning - Received params: {param1}, {param2}")
    return param1 * param2


@decorator.after_throwing(DecoratorCallback)
def example_function_after_throwing(param1, param2):
    logger.info(f"Inside example_function_after_throwing - Received params: {param1}, {param2}")
    raise ValueError("Some Error")


@decorator.around(DecoratorCallback)
def example_function_around(param1, param2):
    logger.info(f"Inside example_function_around - Received params: {param1}, {param2}")
    return param1 - param2


if __name__ == "__main__":
    example_function_before(10, 20)
    example_function_after(30, 40)
    example_function_after_returning(50, 60)
    try:
        example_function_after_throwing(70, 80)
    except ValueError as e:
        logger.error(e)
    example_function_around(90, 100)
