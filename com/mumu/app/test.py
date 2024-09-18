from com.mumu.app.my_mysql import Database
from com.mumu.po.User import User

# 使用示例
if __name__ == "__main__":
    # 数据库连接信息
    USER = 'root'
    PASSWORD = 'root'
    HOST = 'localhost'  # 或者你的MySQL服务器地址
    DATABASE = 'wb'

    list = [1,2,3]
    print(list)
    print(list.reverse())
    print(list)

    # # 创建数据库连接
    # db = Database(USER, PASSWORD, HOST, DATABASE)
    #
    # # 创建表
    # User.create_table(db)
    #
    # # 创建会话
    # session = db.get_session()
    #
    # # 添加新用户
    # User.add_user(session, '毛割', "7896332555", 5079899849359702, "https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68")
    #
    # # 查询所有用户
    # users = User.get_all_users(session)
    # for user in users:
    #     print(user)
    #
    # # 关闭会话和数据库连接
    # session.close()
    # db.close()
