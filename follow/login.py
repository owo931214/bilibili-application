import json
import time

import requests


def get_gt(uid):
    result = requests.get("https://passport.bilibili.com/x/passport-login/captcha?source=main_web")
    data = result.json()["data"]
    return {
        "token": data["token"],
        "challenge": data["geetest"]["challenge"],
        "gt": data["geetest"]["gt"]
    }


def get_vali(uid):
    data = get_gt(uid)
    result = requests.get(f"https://api.geetest.com/get.php?gt={data['gt']}&challenge={data['challenge']}")
    result = json.loads(result.text[1:-1])
    print(result)
    response = requests.get(f"https://api.geetest.com/ajax.php?gt={data['gt']}&challenge={data['challenge']}")
    print(response.text)


if __name__ == "__main__":
    get_vali(None)
