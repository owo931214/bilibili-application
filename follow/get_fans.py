import json
import random
import threading
import time

import requests

user_cookie = {
    "SESSDATA": "894cb883%2C1693378035%2C03451%2A31",
    "buvid3": "D16EC6A1-C027-3A0B-2343-9EBE60ED82EE11272infoc",
    "bili_jct": "d1d292f68baeed574696f09d40cc0d43"
}


def check_status(targets, cookies):
    data = {}
    for target in targets:
        result = requests.get(url=f"https://api.bilibili.com/x/space/acc/relation?mid={str(target)}", cookies=cookies)
        match json.loads(result.text)["code"]:
            case -101:
                raise Exception("未登入")
            case -400:
                raise Exception("請求錯誤")
            case 0:
                data[target] = json.loads(result.text)["data"]
        time.sleep(max(random.gauss(mu=0.2, sigma=0.1), 0.05))
    return data


def keep_running(target, cookie):
    while True:
        threading.Thread(target=check_status, args=(target, cookie,))


if __name__ == "__main__":
    result = check_status(targets=[128912828, 35798955, 4141795, 484819462], cookies=user_cookie)
    for _ in result:
        print(result[_], "\n")
