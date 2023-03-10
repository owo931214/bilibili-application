import json
import sqlite3
import threading
import time
import zlib
import requests
from datetime import datetime
from base import *
import brotli
import websocket

db_path = '../database/bilibili_live.db'
db_conn = sqlite3.connect(db_path)
db_cursor = db_conn.cursor()

heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1])

global_attr = {}




def check_db():
    db_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS danmu
        (message varchar, name varchar, uid int, is_admin bit, time varchar, `room id` int);
        """)


def heartbeating(ws):
    while True:
        ws.send(heart)
        print(">>----Heartbeat----")
        time.sleep(30)


class LiveSocket(websocket.WebSocketApp):
    def __init__(self, room_id = None, uid = None):
        if room_id:
            self.room_id = room_id
            self.uid = roomid2uid(room_id)
        elif uid:
            self.room_id = uid2roomid(uid)
            self.uid = uid
        else:
            raise ValueError("You need to enter room_id or uid")
        
        super(LiveSocket, self).__init__("wss://broadcastlv.chat.bilibili.com/sub", on_open=self.on_open,
                                         on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.thread = threading.Thread(target=heartbeating, args=(self,))
        self.run_forever()

    def on_open(self, ws):
        check_db()
        body = json.dumps({
            "uid": 0,
            "roomid": self.room_id
        }).encode('utf-8')
        header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
        message = header + body
        self.send(message)
        self.thread.start()

    def on_message(self, ws, message):
        self.parsing_msg(message)

    def on_error(self, ws, *args):
        print(f"Error: {args}")

    def on_close(self, ws, *args):
        print(f"Connection closed with: {args}.")
        db_conn.close()
        print("Database closed.")
        del self.thread
        print("Thread break.")

    def parsing_msg(self, message):
        pt = message[7]
        op = message[11]
        print(f"<<----Protocol code: {pt}----")
        match pt:
            case 0 | 1:
                match op:
                    case 3:
                        print("[ 心跳回復 ]")
                        print(f"[ 直播間訊息 ] 當前直播間共{get_people_count(self.room_id)}人")
                    case 5:
                        data = json.loads(message[16:])
                        match data['cmd']:
                            case 'STOP_LIVE_ROOM_LIST':
                                print(f"[ 下播的直播間 ] pass")
                            case 'NOTICE_MSG':
                                print(f"[ 廣播通知 ] pass")
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
                    body_len = (message[base] << 24) + (message[base + 1] << 16) + (message[base + 2] << 8) + message[
                        base + 3] - 16
                    datas.append(json.loads(message[base + 16: base + 16 + body_len]))
                    base = base + 16 + body_len
                    if base == end:
                        break
                # TODO
                for data in datas:
                    match data['cmd']:
                        case 'COMBO_SEND':
                            pass  # TODO
                        case 'DANMU_MSG':
                            danmu_msg = {
                                "msg": data['info'][1],
                                "name": data['info'][2][1],
                                "uid": data['info'][2][0],
                                "is_admin": bool(data['info'][2][2]),
                                "time": str(datetime.fromtimestamp(data['info'][0][4] // 1000)),
                                "room_id": self.room_id
                            }

                            db_cursor.execute(f"""INSERT INTO danmu VALUES (?, ?, ?, ?, ?, ?);""",
                                              tuple(danmu_msg.values()))
                            db_conn.commit()
                            print(f"[ 彈幕訊息 ] {danmu_msg}")
                        case 'ENTRY_EFFECT':
                            effect = {data['data']}
                            print(f"[ 特效 ] {effect}")
                        case 'GUARD_BUY':
                            guard_msg = {
                                "level": data['data']['gift_name'],
                                "time": data['data']['start_time']
                            }
                            print(f"[ 上艦 ] {guard_msg}")
                        case 'HOT_RANK_CHANGED':
                            pass  # TODO
                        case 'INTERACT_WORD':
                            interact_msg = {
                                "act": "關注" if data['data']['msg_type'] == 2 else "進場",
                                "time": data['data']['timestamp'],
                                "uid": data['data']['uid'],
                                "name": data['data']['uname']
                            }
                            print(f"[ 交互訊息 ] {interact_msg}")
                        case 'ONLINE_RANK_COUNT':
                            print(f"[ 高能用戶數量 ] {data['data']['count']}人")
                        case "ONLINE_RANK_V2":
                            for person in data['data']['list']:
                                print(f"[ 高能榜更新 ] 恭喜 {person['uname']} 榮登高能榜第{person['rank']}!")
                        case 'WATCHED_CHANGE':
                            print(f"[ 觀看人數 ] {data['data']['num']}人看過")
                        case _:
                            print(f"[ 未知 ] {data}")


if __name__ == "__main__":
    time_start = time.time()
    wsapp = LiveSocket(room_id=5938587)  # 4767523, 22320946, 4141795
    print(time.time() - time_start)
