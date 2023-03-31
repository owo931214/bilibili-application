import json
import requests


def uid2roomid(uid):
    if not uid:
        return None
    data = json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content)['data']['live_room']
    if data:
        return data['roomid']
    else:
        return None


def roomid2uid(room_id):
    if not room_id:
        return None
    data = json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}').content)['data']
    if data:
        return data['uid']
    else:
        return None


def uid2uname(uid):
    if not uid:
        return None
    data = json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content)
    if data['code'] == 0:
        return data['data']['name']
    else:
        return None
    
def uid2face(uid):
    if not uid:
        return None
    data = json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content)
    if data['code'] == 0:
        return data['data']['face']
    else:
        return None
