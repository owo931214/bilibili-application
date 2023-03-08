import json
import sqlite3
import threading
import time
import zlib

import brotli
import websocket

db_path = '../database/bilibili_live.db'
db_conn = sqlite3.connect(db_path)
db_cursor = db_conn.cursor()

join_data = {
    "roomid": 4767523,
    "uid": 0,
}


def check_db():
    db_cursor.execute("CREATE TABLE IF NOT EXISTS danmu (msg varchar, name varchar, uid int, is_admin bit, time int);")


def heartbeating(self):
    while True:
        heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1])
        self.send(heart)
        print(">>----Heartbeat----")
        time.sleep(30)


def parsing_msg(message):
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
                    if data['cmd'] == 'STOP_LIVE_ROOM_LIST':
                        print(f"[ 下播的直播間 ] pass")

                    else:
                        print(f"[ 廣播通知 ] {message[16:]}")
                case 8:
                    print(f"[ 成功進入直播間 ]")
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
                            "time": data['info'][0][4],
                        }
                        db_cursor.execute("INSERT INTO danmu VALUES (?, ?, ?, ?, ?);",
                                          tuple(danmu_msg.values()))
                        db_conn.commit()
                        print(f"[ 彈幕訊息 ] {danmu_msg}\n{data}")
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
                    case 'WATCHED_CHANGE':
                        print(f"[ 觀看人數 ] {data['data']['num']}人看過")
                    case _:
                        print(f"[ 未知 ] {data}")


def on_open(self):
    check_db()
    body = json.dumps(join_data).encode('utf-8')
    header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
    message = header + body
    self.send(message)
    threading.Thread(target=heartbeating, args=(self,)).start()


def on_message(self, message):
    parsing_msg(message)


def on_error(self, error):
    print(f"Error: {error}")


def on_close(self, *args):
    db_conn.close()
    print(f"Connection closed with: {args}")


if __name__ == "__main__":
    time_start = time.time()
    wsapp = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com/sub", on_open=on_open, on_message=on_message,
                                   on_error=on_error, on_close=on_close)
    wsapp.run_forever()
    print(time.time() - time_start)
