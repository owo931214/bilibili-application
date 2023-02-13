import json
import time
import zlib

import websocket

join_data = {
    "clientver": "1.6.3",
    "platform": "web",
    "protover": 1,
    "roomid": 22320946,
    "uid": 0,
    "type": 2
}


def on_message(self, message):
    cz = message[7]
    data = message[16:]
    if cz == 2:
        data = zlib.decompress(data)[16:]
    data = json.loads(data)
    print(f"Received message: {data}")


def on_error(self, error):
    print(f"Error: {error}")


def on_close(self, *args):
    print(f"Connection closed. {args}")


def on_open(self):
    body = json.dumps(join_data).encode('utf-8')
    header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
    message = header + body
    print("Connection opened.")
    ws.send(message.decode("utf-8"))
    print("Joined.")


def heart_beat(self):
    heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 123, 125])
    self.send(heart.decode("utf-8"))


if __name__ == "__main__":
    time_start = time.time()
    ws = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com:2245/sub", on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever()
    print(time.time() - time_start)
