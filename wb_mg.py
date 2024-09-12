import requests
import schedule
import time
from collections import OrderedDict
from datetime import datetime, timedelta
import json
import os


# 微博API配置
WEIBO_API_URL = "https://weibo.com/ajax/statuses/mymblog"
WEIBO_LONG_TEXT_URL = "https://weibo.com/ajax/statuses/longtext"
WEIBO_UID = "7896332555"  # 替换为你要监控的用户ID
# 文件名用于保存最后处理的ID
LAST_ID_FILE = "last_processed_id.json"

# 钉钉机器人配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=67236f678a9b4f09aceb663ddf7a2b7775c1a768b1e8c2d0c5bd5e9dcb9fcc68"

# 请替换以下cookie值为你自己的
COOKIE = "XSRF-TOKEN=UmpzytSenQAbkUKSBQTn59yz; SCF=AiqQguBVNRzSu0KoVZbtHpxIUXG1WXyx4KQO7KyzlSExnkM6Fa0nQptKP0V9N_29ZdpihO_Hf7glTfdcgeGRM3E.; SUB=_2A25L5v_5DeRhGeBP6VoW9SvFzDWIHXVomn0xrDV8PUNbmtAbLVPYkW9NRXY2jZNHmvyWtC68ztXEEFuM5-H-i3ao; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhOnREGF5-ni5TiSyvnohsR5JpX5KzhUgL.FoqpeonNSK-4S0.2dJLoIEBLxK-L1K2LBKnLxKqL1-eL1-qLxKnL12BLBKeLxKnL1h5L1h5t; ALF=02_1728715946; WBPSESS=g82Sj9YE-TKAkLUPlqSBQ-g1hN0DRv66HkoL4QWDRt2UEKWEZ6aJ8YtenUCkg4gHUOlQ6gOgDNS50h67uwcEUq38I2vca61TgC38cb7OWc49-SnGRHn8Xtk2qega8OsiqNasHv2ogdjHYEx3pf1Rxg=="

HEADERS = {
    "cookie": COOKIE,
}

def parse_weibo_time(time_str):
    # 解析微博时间字符串
    dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S +0800 %Y")
    return dt

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

def get_last_processed_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_id', 0)
    return 0

def save_last_processed_id(id):
    with open(LAST_ID_FILE, 'w') as f:
        json.dump({'last_id': id}, f)

def check_and_sync():
    print(f"Checking for new Weibo posts at {datetime.now()}")
    latest_weibo = get_latest_weibo()
    ordered_dict = OrderedDict()
    last_id = get_last_processed_id()

    print('遍历wb list返回数据')
    for post in latest_weibo:
        if post["id"] > last_id:
            ordered_dict.setdefault(post.get("mblogid"), post.get("created_at"))
    if not ordered_dict:
        return

    print('遍历获取长消息发送钉钉')
    for id, time in ordered_dict.items():
        long_text = get_long_text(id)
        # 5077764864478181
        # {'visible': {'type': 0, 'list_id': 0}, 'created_at': 'Thu Sep 12 12:55:47 +0800 2024', 'id': 5077764864478181, 'idstr': '5077764864478181', 'mid': '5077764864478181', 'mblogid': 'OwD1ciMYJ', 'user': {'id': 7896332555, 'idstr': '7896332555', 'pc_new': 0, 'screen_name': '一年能赚百倍', 'profile_image_url': 'https://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif?KID=imgbed,tva&Expires=1726136909&ssig=jeSK0RFDtI', 'profile_url': '/u/7896332555', 'verified': False, 'verified_type': -1, 'domain': '', 'weihao': '', 'status_total_counter': {'total_cnt_format': 63, 'comment_cnt': '2', 'repost_cnt': '0', 'like_cnt': '61', 'total_cnt': '63'}, 'avatar_large': 'https://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif?KID=imgbed,tva&Expires=1726136909&ssig=YC1RzGfK55', 'avatar_hd': 'https://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif?KID=imgbed,tva&Expires=1726136909&ssig=YC1RzGfK55', 'follow_me': False, 'following': True, 'mbrank': 1, 'mbtype': 11, 'v_plus': None, 'planet_video': True, 'icon_list': [{'type': 'vip', 'data': {'mbrank': 1, 'mbtype': 11, 'svip': 0, 'vvip': 0}}]}, 'can_edit': False, 'textLength': 1038, 'annotations': [{'shooting': 1, 'client_mblogid': 'd23d25cd-4d10-48f0-8267-33c84cb35405'}, {'source_text': '', 'phone_id': '-1'}, {'mapi_request': True}], 'source': '', 'favorited': False, 'rid': '0_0_50_162479832584234008_0_0_0', 'pic_ids': [], 'pic_num': 0, 'is_paid': False, 'mblog_vip_type': 0, 'number_display_strategy': {'apply_scenario_flag': 19, 'display_text_min_number': 1000000, 'display_text': '100万+'}, 'reposts_count': 0, 'comments_count': 2, 'attitudes_count': 21, 'attitudes_status': 0, 'continue_tag': {'title': '全文', 'pic': 'http://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_article.png', 'scheme': 'sinaweibo://detail?mblogid=5077764864478181&id=5077764864478181&next_fid=232532_mblog&feed_detail_type=0', 'cleaned': True}, 'isLongText': True, 'mlevel': 0, 'content_auth': 0, 'is_show_bulletin': 2, 'comment_manage_info': {'comment_permission_type': -1, 'approval_comment_type': 0, 'comment_sort_type': 0}, 'share_repost_type': 0, 'mblogtype': 0, 'showFeedRepost': False, 'showFeedComment': False, 'pictureViewerSign': False, 'showPictureViewer': False, 'rcList': [], 'analysis_extra': 'follow:1', 'readtimetype': 'mblog', 'mixed_count': 0, 'is_show_mixed': False, 'text': '做事情一定要按照规则、规律，这样可以做好，不能急，不要把极小概率的成功当做常态，如果这样盲目地效仿就很容易出现东施效颦的丑态，你要知道自己该干什么，你的规则怎样？你的计划怎样？你做的怎样？在你做事情之前就要了解大概，制定规则，再操作，但在操作的时候会出现一些不同的东西，这个时候你 \u200b\u200b\u200b ...<span class="expand">展开</span>', 'text_raw': '做事情一定要按照规则、规律，这样可以做好，不能急，不要把极小概率的成功当做常态，如果这样盲目地效仿就很容易出现东施效颦的丑态，你要知道自己该干什么，你的规则怎样？你的计划怎样？你做的怎样？在你做事情之前就要了解大概，制定规则，再操作，但在操作的时候会出现一些不同的东西，这个时候你 \u200b\u200b\u200b', 'region_name': '发布于 上海', 'customIcons': []}
        message = f"新微博消息：\n{long_text}\n发布时间：{parse_weibo_time(time)}"
        print(send_to_dingtalk(message))

    save_last_processed_id(latest_weibo[0]["id"])

def main():
    print("启动微博同步程序...")
    check_and_sync()


if __name__ == "__main__":
    main()