import json
import requests

def uid2roomid(uid):
    return json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={'user-agent': 'Mozilla/5.0'}).content)['data']['live_room']['roomid']

def roomid2uid(room_id):
    return json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}').content)['data']['uid']

def uid2uname(uid):
    return json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={'user-agent': 'Mozilla/5.0'}).content)['data']['name']

def get_people_count(room_id):
    return json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}').content)['data']['online']