import requests


def get_danmu(roomid):
    url = "https://api.live.bilibili.com/ajax/msg?roomid="
    result = requests.get(url + str(roomid)).json()
    result = result['data']['room']
    return result


print((len(get_danmu(7595278))))
