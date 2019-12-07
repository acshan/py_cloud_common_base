from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_POOL_RECYCLE = 30


class MysqlAPI:
    def __init__(self, connection_str, pool_recycle=DEFAULT_POOL_RECYCLE):
        self.connection_str = connection_str
        self.pool_recycle = pool_recycle
        self.session = self.get_session()

    @staticmethod
    def get_session(connection_str, pool_recycle=DEFAULT_POOL_RECYCLE):
        db_engine = create_engine(connection_str, pool_recycle=pool_recycle)
        db_session_maker = sessionmaker(bind=db_engine)
        session = db_session_maker()
        return session


if __name__ == '__main__':
    mysqldb = MysqlAPI('test')
