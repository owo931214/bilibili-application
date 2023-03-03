import json
import threading
import time
import zlib

import brotli
import websocket


def heartbeating(self):
    while True:
        heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1])
        self.send(heart)
        print(">>----Heartbeat----")
        time.sleep(30)


def load_msg(message):
    base = 0
    end = len(message)
    datas = []
    while True:
        body_len = (message[base] << 24) + (message[base + 1] << 16) + (message[base + 2] << 8) + message[base + 3] - 16
        datas.append(json.loads(message[base + 16: base + 16 + body_len]))
        base = base + 16 + body_len
        if base == end:
            break
    return datas


def on_open(self):
    join_data = {
        "roomid": 24393,
        "uid": 0,
    }
    body = json.dumps(join_data).encode('utf-8')
    header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
    message = header + body
    print("Connection opened.")
    self.send(message)
    print("Joined.")
    threading.Thread(target=heartbeating, args=(self,)).start()


def on_message(self, message):
    pt = message[7]
    op = message[11]
    print(f"<<----Protocol code: {pt}----")
    match pt:
        case 0, 1:
            match op:
                case 3:
                    print("Get heartbeat response")
                case 8:
                    print(f"Successfully entered the room | Received message: {json.loads(message[16:])}")
                case _:
                    print(f"Could not process message: {json.loads(message[16:])}")
        case 2:
            message = zlib.decompress(message[16:])
            datas = load_msg(message)
            for data in datas:
                print(f"Opcode: {op} | Received message: {data}")
        case 3:
            message = brotli.decompress(message[16:])
            datas = load_msg(message)
            for data in datas:
                print(f"Opcode: {op} | Received message: {data}")


def on_error(self, error):
    print(f"Error: {error}")


def on_close(self, *args):
    print(f"Connection closed with: {args}")


if __name__ == "__main__":
    time_start = time.time()
    wsapp = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com/sub", on_open=on_open, on_message=on_message,
                                   on_error=on_error, on_close=on_close)
    wsapp.run_forever()
    print(time.time() - time_start)
