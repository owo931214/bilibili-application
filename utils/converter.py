import base64
import json
import zlib
from io import BytesIO

import requests
from PIL import Image, ImageDraw


def uid2roomid(uid):
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()

    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況
    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)['data']['live_room']
    if data:
        return data['roomid']
    else:
        print(data['code'])
        return None


def roomid2uid(room_id):
    data = json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}').content)['data']
    if data:
        return data['uid']
    else:
        print(data['code'])
        return None


def uid2uname(uid):
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()

    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況
    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)
    if data['code'] == 0:
        return data['data']['name']
    else:
        print(data['code'])
        return None


def uid2face(uid):
    data = requests.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}", headers={
        'user-agent': 'Mozilla/5.0'
    }).content.decode()

    # 2023/4/21 出現 {"code":-509,.....}{"code":0.....} 的情況
    if data[45:47] == "}{":
        data = data[46:]

    data = json.loads(data)
    if data['code'] == 0:
        image = requests.get(data['data']['face']).content
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
    else:
        print(data['code'])
        return None


def face_decompress(face):
    image = zlib.decompress(face).decode()
    return image
