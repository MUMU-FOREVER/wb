import logging
from datetime import datetime

import requests

def parse_time(time_str):
    # 解析微博时间字符串
    dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S +0800 %Y")
    return dt

# 配置日志的基本设置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_to_dingtalk(name, long_text, time):
    message = f"发布人：【{name}】  发布时间：{parse_time(time)} \n{long_text}"
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
