import requests
import schedule
import json
from datetime import datetime

# 微博API配置
WEIBO_API_URL = "https://weibo.com/ajax/statuses/mymblog"
WEIBO_UID = "7896332555"  # 替换为你要监控的用户ID
LAST_ID=5077764864478180

# 钉钉机器人配置
DINGTALK_WEBHOOK = "YOUR_DINGTALK_WEBHOOK_URL"

# 请替换以下cookie值为你自己的
COOKIE = "XSRF-TOKEN=UmpzytSenQAbkUKSBQTn59yz; SCF=AiqQguBVNRzSu0KoVZbtHpxIUXG1WXyx4KQO7KyzlSExnkM6Fa0nQptKP0V9N_29ZdpihO_Hf7glTfdcgeGRM3E.; SUB=_2A25L5v_5DeRhGeBP6VoW9SvFzDWIHXVomn0xrDV8PUNbmtAbLVPYkW9NRXY2jZNHmvyWtC68ztXEEFuM5-H-i3ao; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhOnREGF5-ni5TiSyvnohsR5JpX5KzhUgL.FoqpeonNSK-4S0.2dJLoIEBLxK-L1K2LBKnLxKqL1-eL1-qLxKnL12BLBKeLxKnL1h5L1h5t; ALF=02_1728715946; WBPSESS=g82Sj9YE-TKAkLUPlqSBQ-g1hN0DRv66HkoL4QWDRt2UEKWEZ6aJ8YtenUCkg4gHUOlQ6gOgDNS50h67uwcEUq38I2vca61TgC38cb7OWc49-SnGRHn8Xtk2qega8OsiqNasHv2ogdjHYEx3pf1Rxg=="

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "client-version": "v2.46.10",
    "cookie": COOKIE,
    "priority": "u=1, i",
    "referer": f"https://weibo.com/u/{WEIBO_UID}",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2024.09.10.1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "UmpzytSenQAbkUKSBQTn59yz"  # 请确保这与cookie中的XSRF-TOKEN值匹配
}


def get_latest_weibo():
    params = {
        "uid": WEIBO_UID,
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
        print(f"Request Error: {e}")
    except ValueError as e:
        print(f"JSON Decode Error: {e}")
    return None


def send_to_dingtalk(message):
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=data, headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"DingTalk Send Error: {e}")
        return False


def check_and_sync():
    print(f"Checking for new Weibo posts at {datetime.now()}")


def main():
    json_str = '[{"visible":{"type":0,"list_id":0},"created_at":"Thu Sep 12 12:55:47 +0800 2024","id":5077764864478181,"idstr":"5077764864478181","mid":"5077764864478181","mblogid":"OwD1ciMYJ","customIcons":[]}]'
    latest_weibo = json.loads(json_str)
    print(latest_weibo)
    ids = list()
    print(latest_weibo[0]["id"])
    for post in latest_weibo:
        if post["id"] > LAST_ID:
            ids.append(post["id"])
    print(ids)

    print(f"last_id=' {LAST_ID}")
    for id in reversed(ids):
        print(id)

if __name__ == "__main__":
    main()