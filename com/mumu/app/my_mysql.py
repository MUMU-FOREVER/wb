from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector

# 创建一个基础类
Base = declarative_base()

class Database:
    def __init__(self, user, password, host, database):
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}', echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()
