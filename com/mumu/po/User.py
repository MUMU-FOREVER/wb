from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from com.mumu.app.my_mysql import Database

# 创建一个基础类
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    uid = Column(String(32))
    last_id = Column(BigInteger)
    webhook = Column(String(200))

    @classmethod
    def create_table(cls, db: Database):
        Base.metadata.create_all(db.engine)
        print("Table created successfully")

    @classmethod
    def add_user(cls, session, name, uid, last_id, webhook):
        new_user = cls(name=name, uid=uid, last_id=last_id, webhook=webhook)
        session.add(new_user)
        session.commit()

    @classmethod
    def get_all_users(cls, session):
        return session.query(cls).all()

    @classmethod
    def update_last_id_user_by_id(cls, session, user_id, last_id=None):
        user = session.query(cls).filter_by(id=user_id).first()
        user.last_id = last_id
        session.commit()
        return user

    @classmethod
    def delete_user_by_id(cls, session, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False