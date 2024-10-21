import logging
import sys
import time
from datetime import datetime
import requests
import schedule

from com.mumu.app.my_mysql import Database
from com.mumu.po.User import User

# 配置日志的基本设置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 微博API配置
WEIBO_API_URL = "https://weibo.com/ajax/statuses/mymblog"
WEIBO_LONG_TEXT_URL = "https://weibo.com/ajax/statuses/longtext"
DEFAULT_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68"

# 请替换以下cookie值为你自己的
COOKIE = "UOR=www.google.com,weibo.com,www.google.com; SINAGLOBAL=1501339418390.0996.1715742721445; SCF=AlXLBiPjXZ_bBVH2QOsVabjZA2-YvdgzlxSY6FAn4Ll-h4cig6xGxQEJgadx011XWSc56QOxztSUcELCyXRhY40.; XSRF-TOKEN=bo8-njf8HFq20MRXnKenpA3U; _s_tentry=weibo.com; Apache=2275004033601.6953.1729137026872; ULV=1729137026927:7:1:1:2275004033601.6953.1729137026872:1726649678263; ALF=1732086609; SSOLoginState=1729494609; SUB=_2A25KEY4fDeRhGeBP6VoW9SvFzDWIHXVpbo_XrDV8PUJbkNAbLUH4kW1NRXY2jQ0VR_jr3fW8cEjL1i4OAnpSpOyD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhOnREGF5-ni5TiSyvnohsR5JpX5KMhUgL.FoqpeonNSK-4S0.2dJLoIEBLxK-L1K2LBKnLxKqL1-eL1-qLxKnL12BLBKeLxKnL1h5L1h5t; WBPSESS=g82Sj9YE-TKAkLUPlqSBQ-g1hN0DRv66HkoL4QWDRt2UEKWEZ6aJ8YtenUCkg4gHah8uvSm-lv9XxsEZxTkGdvbfwk6r456pYU6cZCO5JXsaV36ZV5RFvS5W9CTp3vprANiW4mim8QtUhG-LEy_4eg=="

HEADERS = {
    "cookie": COOKIE,
}

def parse_time(time_str):
    # 解析微博时间字符串
    dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S +0800 %Y")
    return dt

def send_error_message():
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": "cookie失效导致调用失败"
        }
    }
    try:
        response = requests.post(DEFAULT_WEBHOOK, json=data, headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logging.error(f"DingTalk Send Error: {e}")
        return False

def get_latest_weibo(uid):
    params = {
        "uid": uid,
        "page": 1,
        "feature": 0
    }
    try:
        response = requests.get(WEIBO_API_URL, params=params, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if data.get("data", {}).get("list"):
                return data["data"]["list"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Error: {e}")
        send_error_message()
        sys.exit(0)
    except ValueError as e:
        logging.error(f"JSON Decode Error: {e}")
    return None


def get_long_text(id):
    params = {
        "id": id
    }
    try:
        response = requests.get(WEIBO_LONG_TEXT_URL, params=params, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["longTextContent"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Error: {e}")
    except ValueError as e:
        logging.error(f"JSON Decode Error: {e}")
    return None


def send_to_dingtalk(user, long_text, time):
    message = f"发布人：【{user.name}】  发布时间：{parse_time(time)} \n{long_text}"
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(user.webhook, json=data, headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logging.error(f"DingTalk Send Error: {e}")
        return False

def send_message(user, message):
    # 短消息直接发送
    if "span" in message.get('text'):
        long_text = get_long_text(message.get("mblogid"))
        send_to_dingtalk(user, long_text, message.get("created_at"))
    else:
        send_to_dingtalk(user, message.get("text"), message.get("created_at"))

def check_and_sync(user):
    latest_weibo = get_latest_weibo(user.uid)

    if not latest_weibo:
        return
    for message in latest_weibo:
        if message["id"] > user.last_id and user.uid == str(message.get('user').get('id')):
            send_message(user, message)
    user.last_id=latest_weibo[0]["id"]


def check_and_sync_log():
    logging.info("============== start =================")

    # 创建数据库连接
    db = Database.local_database()

    # 创建会话
    session = db.get_session()

    # 查询所有用户
    users = User.get_all_users(session)
    for user in users:
        check_and_sync(user)
        user.update_last_id_user_by_id(session, user.id, user.last_id)

    # 关闭会话和数据库连接
    session.close()
    db.close()
    logging.info("============== end =================")

def main():
    check_and_sync_log()
    # 配置每小时执行一次的任务
    for hour in range(9, 24):  # 从 9 点到 23 点
        schedule.every().day.at(f"{hour:02d}:00").do(check_and_sync_log)

    while True:
        # 检查是否有任务需要执行
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()