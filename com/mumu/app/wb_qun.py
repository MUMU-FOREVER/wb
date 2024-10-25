import logging
import sys
from datetime import datetime, timedelta
import time
import requests

from com.mumu.app.wb_db import COOKIE

# 配置日志的基本设置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 微博API配置
WEIBO_API_URL = "https://api.weibo.com/webim/groupchat/query_messages.json"
DEFAULT_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68"

HEADERS = {
    'referer': 'https://api.weibo.com/chat',
    "cookie": COOKIE
}

def get_latest_weibo():
    params = {
        'convert_emoji': 1,
        'query_sender': 1,
        'count': 50,
        'id': '5026306691435767',
        'max_mid': 0,
        'source': 209678993,
        't': int(time.time()*1000)
    }

    try:
        response = requests.get(WEIBO_API_URL, params=params, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data["messages"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Error: {e}")
        sys.exit(0)
    except ValueError as e:
        logging.error(f"JSON Decode Error: {e}")
    return None

def parse_time(time_str):
    # 解析微博时间字符串
    # dt = datetime.fromtimestamp(time_str, "%a %b %d %H:%M:%S +0800 %Y")
    dt = datetime.fromtimestamp(time_str).strftime('%Y-%m-%d %H:%M:%S')
    return dt

def main():
    messages = get_latest_weibo()
    max_id = messages[0]["id"]
    # 初始化前一条消息的时间
    previous_time = None
    formatted_lines = []

    for item in messages:
        if item['from_uid'] == 7948379069 and item['type'] == 321:
            current_time = datetime.fromtimestamp(item['time'])

            if previous_time is not None and (current_time - previous_time) <= timedelta(minutes=10):
                # 如果时间间隔在5分钟之内，不拼接时间
                formatted_lines.append(item['content'])
            else:
                # 否则，拼接时间
                formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                formatted_lines.append(f"\n{formatted_time} ：{item['content']}")

            # 更新前一条消息的时间
            previous_time = current_time

    # 拼接所有字符串
    message = "，".join(formatted_lines)
    print(message)

if __name__ == "__main__":
    main()