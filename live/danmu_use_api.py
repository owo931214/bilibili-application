import requests, time
from bilibili_api import live, sync, Credential, user



sessdata = "4f3e770b%2C1675916889%2Cca246%2A81"
bili_jct = "df25c68df5fb29302c65643bb3e8bbb0"
buvid = "6F906E77-7DC7-4D9E-86AF-178740C7B61A148804infoc"
room_id = 22764086
credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid)
room = live.LiveRoom(room_display_id=room_id, credential=credential)

credential = Credential(sessdata="你的 SESSDATA", bili_jct="你的 bili_jct", buvid3="你的 buvid3")

user = user.User(uid=599041628, credential=credential)

fans_list = sync(user.get_followers())
for fans in fans_list['list']:
    print(fans)
    print(fans['uname'], fans['mid'])
# 發送彈幕
# url = "https://api.live.bilibili.com/msg/send"
# params = {
#     "color": 16777215,
#     "fontsize": 25,
#     "mode": 1,
#     "msg": message,
#     "rnd": int(time.time()),
#     "roomid": room_id
# }
#
# # 請求發送彈幕
# response = requests.post(url, params=params)
# print(type(response), response.json())