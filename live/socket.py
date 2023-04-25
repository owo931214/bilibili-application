import threading
import time
from datetime import datetime

import brotli
import websocket

from utils.converter import *


# 128912828 沙月, 22320946 純寶, 4141795 小沙月, 768756 滋蹦, 24393 雪狐


class HeartBeating(threading.Thread):
    def __init__(self, ws):
        super().__init__()
        self.heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1])
        self.keep_running = True
        self.ws = ws

    def run(self):
        while self.keep_running:
            self.ws.send(self.heart)
            print(">>----Heartbeat----")
            time.sleep(30)


class LiveSocket(websocket.WebSocketApp):
    def __init__(self, room_id=None, uid=None):
        self.heartbeat = None
        if room_id:
            self.room_id = room_id
            self.uid = roomid2uid(room_id)
        elif uid:
            self.room_id = uid2roomid(uid)
            self.uid = uid
        else:
            raise ValueError("You need to enter room_id or uid")
        self.msg = None
        super().__init__("wss://broadcastlv.chat.bilibili.com/sub", on_open=self.on_open, on_message=self.on_message, on_error=self.on_error,
                         on_close=self.on_close)

    def start(self):
        self.heartbeat = HeartBeating(self)
        self.run_forever()

    def on_open(self, ws):
        body = json.dumps({
            "uid": 0,
            "roomid": self.room_id
        }).encode('utf-8')
        header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
        message = header + body
        self.send(message)
        self.heartbeat.start()

    def on_message(self, ws, message):
        self.parsing_msg(message)

    def on_error(self, ws, *args):
        print(f"Error: {args}")

    def on_close(self, ws, *args):
        print(f"Connection closed with: {args}.")
        print("Database closed.")
        self.heartbeat.keep_running = False

    # 收到對應指令碼時執行
    def on_gift(self):
        pass

    def on_danmu(self):
        pass

    def on_guard(self):
        pass

    def on_enter(self):
        pass

    def on_follow(self):
        pass

    def parsing_msg(self, message):
        pt = message[7]
        op = message[11]
        print(f"<<----Protocol code: {pt}----")
        match pt:
            case 0 | 1:
                match op:
                    case 3:
                        print("[ 心跳回復 ]")
                    case 5:
                        data = json.loads(message[16:])
                        match data['cmd']:
                            case 'NOTICE_MSG':
                                print(f"[ 廣播通知 ] pass")
                            case 'ROOM_REAL_TIME_MESSAGE_UPDATE':
                                print(f"[ 粉絲人數變更 ] 當前粉絲數 {data['data']['fans']}")
                            case 'STOP_LIVE_ROOM_LIST':
                                print(f"[ 下播的直播間 ] pass")
                            case 'WIDGET_BANNER':
                                print(f"[ 橫幅訊息 ] pass")
                            case _:
                                print(f"[ 未知 ] {message[16:]}")
                    case 8:
                        print(f"[ 進入直播間 ] 成功進入 {uid2uname(self.uid)} 的直播間")
                    case _:
                        print(f"[ 未知 ] Opcode: {op} | Received message: {message[16:]}")
            case 2 | 3:
                if pt == 2:
                    message = zlib.decompress(message[16:])
                elif pt == 3:
                    message = brotli.decompress(message[16:])

                base = 0
                end = len(message)
                datas = []
                while True:
                    body_len = (message[base] << 24) + (message[base + 1] << 16) + (message[base + 2] << 8) + message[base + 3] - 16
                    datas.append(json.loads(message[base + 16: base + 16 + body_len]))
                    base = base + 16 + body_len
                    if base == end:
                        break
                for data in datas:
                    # TODO
                    match data['cmd']:
                        case 'SEND_GIFT':
                            self.msg = {
                                "giftname": data['data']['giftName'],
                                "count": data['data']['num'],
                                "uname": data['data']['uname'],
                                "uid": data['data']['uid'],
                                "time": str(datetime.fromtimestamp(data['data']['timestamp']))
                            }
                            print(f"[ 禮物訊息(send_gift) ] {self.msg}")
                            self.on_gift()
                        case 'COMBO_SEND':
                            self.msg = {
                                "giftname": data[data]['gift_name'],
                                "count": data[data]['total_num'],
                                "uname": data['data']['uname'],
                                "uid": data['data']['uid'],
                                "time": str(datetime.now())[:-7]
                            }
                            print(f"[ 禮物訊息(combo_send) ] {self.msg}")
                            self.on_gift()
                        case 'DANMU_MSG':
                            self.msg = {
                                "msg": data['info'][1],
                                "uname": data['info'][2][1],
                                "uid": data['info'][2][0],
                                "is_admin": bool(data['info'][2][2]),
                                "time": str(datetime.fromtimestamp(data['info'][0][4] // 1000))
                            }
                            print(f"[ 彈幕訊息 ] {self.msg}")
                            self.on_danmu()
                        case 'ENTRY_EFFECT':
                            print(f"[ 特效 ] pass")
                        case 'GUARD_BUY':
                            self.msg = {
                                "level": data['data']['gift_name'],
                                "uname": data['data']['username'],
                                "uid": data['data']['uid'],
                                "time": str(datetime.fromtimestamp(data['data']['start_time']))
                            }

                            print(f"[ 上艦訊息 ] {self.msg}")
                            self.on_guard()
                        case 'HOT_RANK_CHANGED':
                            pass  # TODO
                        case 'INTERACT_WORD':
                            self.msg = {
                                "act": "關注" if data['data']['msg_type'] == 2 else "進場",
                                "name": data['data']['uname'],
                                "uid": data['data']['uid'],
                                "time": str(datetime.fromtimestamp(data['data']['timestamp']))
                            }
                            print(f"[ 交互訊息 ] {self.msg}")
                            if data['data']['msg_type'] == 2:
                                self.on_follow()
                            else:
                                self.on_enter()
                        case 'LIKE_INFO_V3_CLICK':
                            print(f"[ 點讚訊息 ] 感謝 {data['data']['uname']} 點讚了直播間")
                        case 'LIKE_INFO_V3_UPDATE':
                            print(f"[ 點讚人數 ] {data['data']['click_count']}")
                        case 'ONLINE_RANK_COUNT':
                            print(f"[ 高能用戶數量 ] {data['data']['count']}人")
                        case "ONLINE_RANK_V2":
                            for person in data['data']['list']:
                                print(f"[ 高能榜更新 ] 恭喜 {person['uname']} 榮登高能榜第{person['rank']}!")
                        case "POPULAR_RANK_CHANGED":
                            print(f"[ 人氣排行 ] 當前人氣排行第 {data['data']['rank']}")
                        case 'WATCHED_CHANGE':
                            print(f"[ 觀看人數 ] {data['data']['num']}人看過")
                        case _:
                            print(f"[ 未知 ] {data}")
