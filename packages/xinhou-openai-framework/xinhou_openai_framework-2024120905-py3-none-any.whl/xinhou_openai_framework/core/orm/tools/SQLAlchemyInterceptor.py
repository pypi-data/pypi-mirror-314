from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class SQLAlchemyInterceptor:
    def __init__(self, session: Session):
        """
        初始化拦截器

        :param session: SQLAlchemy Session对象
        """
        self.session = session

    def before_execute(self, conn, clauseelement, multiparams, params):
        """
        SQL执行前的回调方法

        :param conn: 数据库连接对象
        :param clauseelement: SQL表达式对象
        :param multiparams: 执行参数的多参数列表
        :param params: 执行参数字典
        """
        print("Before SQL Execution:")
        print(str(clauseelement.compile(dialect=self.session.bind.dialect)))

    def after_execute(self, conn, clauseelement, multiparams, params, result):
        """
        SQL执行后的回调方法

        :param conn: 数据库连接对象
        :param clauseelement: SQL表达式对象
        :param multiparams: 执行参数的多参数列表
        :param params: 执行参数字典
        :param result: SQL执行结果
        """
        print("After SQL Execution:")
        print(str(clauseelement.compile(dialect=self.session.bind.dialect)))


def intercept_sql_execution(session: Session):
    """
    注册SQL执行拦截器

    :param session: SQLAlchemy Session对象
    """
    interceptor = SQLAlchemyInterceptor(session)

    @event.listens_for(Engine, "before_execute")
    def before_execute(conn, clauseelement, multiparams, params):
        """
        SQLAlchemy before_execute事件监听器

        :param conn: 数据库连接对象
        :param clauseelement: SQL表达式对象
        :param multiparams: 执行参数的多参数列表
        :param params: 执行参数字典
        """
        interceptor.before_execute(conn, clauseelement, multiparams, params)

    @event.listens_for(Engine, "after_execute")
    def after_execute(conn, clauseelement, multiparams, params, result):
        """
        SQLAlchemy after_execute事件监听器

        :param conn: 数据库连接对象
        :param clauseelement: SQL表达式对象
        :param multiparams: 执行参数的多参数列表
        :param params: 执行参数字典
        :param result: SQL执行结果
        """
        interceptor.after_execute(conn, clauseelement, multiparams, params, result)


# 使用示例
# 创建Session对象
# session = Session()

# 注册拦截器
# intercept_sql_execution(session)

# 执行SQL语句
# session.query(MyModel).filter(MyModel.id == 1).all()

# 关闭Session对象
# session.close()
