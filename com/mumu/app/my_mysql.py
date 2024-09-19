from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建一个基础类
Base = declarative_base()

# 数据库连接信息
user = 'root'
password = 'root'
host = 'localhost'  # 或者你的MySQL服务器地址
database = 'wb'

class Database:
    def __init__(self, user, password, host, database):
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}', echo=False)
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def local_database():
        return Database(user, password, host, database)

    def get_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()
