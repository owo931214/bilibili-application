import sqlite3
from datetime import datetime

from utils.converter import *

user_cookie = {
    "SESSDATA": "894cb883%2C1693378035%2C03451%2A31",
    "buvid3": "D16EC6A1-C027-3A0B-2343-9EBE60ED82EE11272infoc",
    "bili_jct": "d1d292f68baeed574696f09d40cc0d43"
}

my_uid = 599041628

db_path = '../database/bilibili_followers.db'
db_conn = sqlite3.connect(db_path)
db_cursor = db_conn.cursor()


def check_db():
    db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS change(`change` int, name varchar, uid int, time varchar);""")
    db_cursor.execute(f"""CREATE TABLE IF NOT EXISTS followers(`status code` int, name varchar, uid int, time varchar);""")


def check_followers_status():
    start1 = time.time()
    db_cursor.execute("""SELECT uid FROM followers;""")
    uids = list(sum(db_cursor.fetchall(), ()))
    datas = []
    print(time.time() - start1)
    start1 = time.time()
    print(len(uids))
    for uid in uids:
        data = json.loads(requests.get(f"https://api.bilibili.com/x/space/acc/relation?mid={str(uid)}", cookies=user_cookie).content)
        if not data["code"] == 0:
            raise Exception("獲取訊息失敗")
        data = data['data']
        follower_info = {
            "uid": uid,
            "status": data['be_relation']['attribute'],
            "time": str(datetime.fromtimestamp(data['be_relation']['mtime'])),
            "name": uid2uname(uid)
        }
        datas.append(tuple(follower_info.values()))
        time.sleep(0.05)
    print(time.time() - start1)
    start1 = time.time()
    db_cursor.executemany("""  
        INSERT INTO change (uid, change, time, name) SELECT ?, ?, ?, ? 
        WHERE NOT EXISTS (SELECT 1 FROM followers WHERE uid = ? AND `status code` = ?);""", [_ + _[:2] for _ in datas])
    print(time.time() - start1)
    start1 = time.time()
    db_cursor.executemany("""
        UPDATE followers SET `status code`=?, time=? 
        WHERE uid = ? AND (`status code` IS NULL OR `status code` <> ? OR time IS NULL OR time <> ?);""", [_[1:3] + _[:3] for _ in datas])
    print(time.time() - start1)
    start1 = time.time()
    db_conn.commit()
    db_cursor.execute("""DELETE FROM followers WHERE `status code` = 0""")
    db_conn.commit()
    print(time.time() - start1)
    start1 = time.time()


def check_new_followers(pn):
    datas = []
    for i in range(pn + 1):
        data = json.loads(requests.get(f"https://api.bilibili.com/x/relation/followers?pn={i}&ps=50&vmid={my_uid}", cookies=user_cookie).content)
        if not data['code'] == 0:
            raise Exception("獲取訊息失敗")
        for follower in data['data']['list']:
            follower_info = {
                "name": follower['uname'],
                "uid": follower['mid'],
            }
            datas.append(tuple(follower_info.values()) + (follower_info['uid'],))
        time.sleep(0.05)
    db_cursor.executemany("""INSERT INTO followers (name, uid)
                        SELECT ?, ? WHERE NOT EXISTS(SELECT 1 FROM followers WHERE uid = ?);""", datas)
    db_conn.commit()


if __name__ == "__main__":
    check_db()
    # r = check_followers_status([316045757, 128912828, 35798955, 4141795, 484819462])
    start = time.time()
    check_new_followers(5)
    print(time.time() - start)
    check_followers_status()
