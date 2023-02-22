import requests

def login(uid):
    result = requests.get("https://passport.bilibili.com/x/passport-login/captcha?source=main_web")
    print(result.json())

if __name__ == "__main__":
    login(None)