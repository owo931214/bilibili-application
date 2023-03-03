import requests
import time
import random
import threading
import json

user_cookie = {"SESSDATA":"", "buvid3":"9C2E1061-55EE-B5D9-F0C8-E040FF955F4C08928infoc", "bili_jct":"f9829afb92484fb401e5f032f1c1654f"}
def check_status(targets, cookies):
    for target in targets:
        result = requests.get(url=f"https://api.bilibili.com/x/space/acc/relation?mid={str(target)}",cookies=cookies)
        print(result.text)
        if json.loads(result.text)["code"] == -101:
            raise KeyboardInterrupt
        time.sleep(random.gauss(mu=0.2,sigma=0.1))

def keep_running(target, cookie):
    while(True):
        threading.Thread(target=check_status, args=(target, cookie,))

if __name__ == "__main__":
    check_status(targets=[35798955],cookies=user_cookie)