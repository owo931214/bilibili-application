import base64
import json
import time
import zlib
from io import BytesIO

import requests
from PIL import Image, ImageDraw


def uid2roomid(uid):
    time.sleep(0.5)
    # 2023/5/22 暫時無法使用
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()

    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況
    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)
    if data['code'] == 0:
        return data['data']['live_room']['roomid']
    elif data['code'] == -799:
        data = json.loads(requests.get(f"https://api.live.bilibili.com/live_user/v1/Master/info?uid={uid}").content)
        if data['code'] == 0:
            return data['data']['room_id']
        else:
            print(data)
            return None
    else:
        print(data)
        return None


def roomid2uid(room_id):
    time.sleep(0.5)
    data = json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}').content)
    if data['code'] == 0:
        return data['data']['uid']
    else:
        print(data)
        return None


def uid2uname(uid):
    time.sleep(0.5)
    # 2023/5/22 暫時無法使用
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()
    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況

    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)
    if data['code'] == 0:
        return data['data']['name']
    elif data['code'] == -799:
        data = json.loads(requests.get(f"https://api.bilibili.com/x/web-interface/card?mid={uid}").content)
        if data['code'] == 0:
            return data['data']['card']['name']
        else:
            print(data)
            return None
    else:
        print(data)
        return None


def uid2face(uid):
    time.sleep(0.5)
    # 2023/5/22 暫時無法使用
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()
    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況
    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)
    if data['code'] == 0:
        image = get_face(data['data']['face'])
        return image
    elif data['code'] == -799:
        data = json.loads(requests.get(f"https://api.bilibili.com/x/web-interface/card?mid={uid}").content)
        if data['code'] == 0:
            return get_face(data['data']['card']['face'])
        else:
            print(data)
            return None
    else:
        print(data)
        return None


def get_face(face_url):
    image = requests.get(face_url).content
    image = Image.open(BytesIO(image)).resize((50, 50), Image.LANCZOS)

    # 用圓形遮罩圖片
    mask = Image.new('L', (50, 50), 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice(((0, 0), (50, 50)), 0, 360, fill=255)
    image.putalpha(mask)

    # 保存並壓縮圖片
    byte_image = BytesIO()
    image.save(byte_image, format='WEBP', optimize=True, quality=1)
    image = base64.b64encode(byte_image.getvalue())
    image = zlib.compress(image)
    return image


def face_decompress(face):
    image = zlib.decompress(face).decode()
    return image
