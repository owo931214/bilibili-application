import json
import time
import zlib

import websocket


def on_open(wsapp):
    join_data = {
        "roomid": 24393,
        "uid": 0,
    }
    body = json.dumps(join_data).encode('utf-8')
    header = bytes([0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1])
    message = header + body
    print("Connection opened.")
    ws.send(message, opcode=websocket.ABNF.OPCODE_BINARY)
    print("Joined.")


def on_message(wsapp, message):
    pt = message[7]
    if pt == 2:
        message = zlib.decompress(message[16:])
        base = 0
        end = len(message)
        datas = []
        while True:
            body_len = (message[base] << 24) + (message[base + 1] << 16) + \
                       (message[base + 2] << 8) + message[base + 3] - 16
            datas.append(json.loads(message[base + 16: base + 16 + body_len]))
            base = base + 16 + body_len
            if base == end:
                break
        for data in datas:
            print(f"Received message: {data}")
    else:
        data = json.loads(message[16:])
        print(f"Received message: {data}")



def on_ping(wsapp):
    heart = bytes([0, 0, 0, 18, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 123, 125])
    wsapp.send(heart.decode("utf-8"))
    print("Ping.")


def on_error(wsapp, error):
    print(f"Error: {error}")


def on_close(wsapp, *args):
    print(f"Connection closed with: {args}")


if __name__ == "__main__":
    time_start = time.time()
    ws = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com:2245/sub", on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close, on_ping=on_ping)
    ws.run_forever(ping_interval=30, ping_payload="payload")
    print(time.time() - time_start)
