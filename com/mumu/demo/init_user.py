from com.mumu.app.my_mysql import Database
from com.mumu.po.User import User


def main():
    # 创建数据库连接
    db = Database.local_database()

    # 创建会话
    session = db.get_session()

    # 查询所有用户
    # 毛割	7896332555	5080333005096879	https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68
    # 毛割2	7948227479	5080267679858797	https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68
    # youarebest-	5832935744	5075594887042132	https://oapi.dingtalk.com/robot/send?access_token=fd1f011bcef1e7275be778967de69162e6ecefff23306e63c946d7cacd4f27d5
    # User.create_table(session, db)
    # User.add_user(session, '毛割', '7896332555', 5080333005096879, 'https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9d')
    # User.add_user(session, '毛割2', '7948227479', 5080267679858797, 'https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5')
    # User.add_user(session, 'youarebest-', '5832935744', 5075594887042132, 'https://oapi.dingtalk.com/robot/send?access_token=fd1f011bcef1e7275be778967de69162e6ecefff23306e63c946d7')


    # 关闭会话和数据库连接
    session.close()
    db.close()

if __name__ == "__main__":
    main()

