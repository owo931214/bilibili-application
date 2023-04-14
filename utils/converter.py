import base64
import json
import sys
import time
import zlib
from io import BytesIO

import requests
from PIL import Image


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
        image = requests.get(data['data']['face']).content
        image = Image.open(BytesIO(image)).resize((100, 100), Image.LANCZOS)
        byte_image = BytesIO()
        image.save(byte_image, format='WEBP', optimize=True, quality=1)
        image = base64.b64encode(byte_image.getvalue())
        image = zlib.compress(image)
        return image
    else:
        return None


def face_decompress(face):
    image = zlib.decompress(face).decode()
    return image
