from flask import Flask, request
import requests
import re

TOKEN = "7831505272:AAGRgRwNce221xAR9ER-Qo5Dv_LYRrjqOXg"
API_URL = f"https://api.telegram.org/bot{TOKEN}"
FB_CHECK_URL = "https://graph.facebook.com/"

app = Flask(__name__)

def parse_line(line):
    parts = line.strip().split('|')
    uid = parts[0] if len(parts) > 0 else ''
    password = parts[1] if len(parts) > 1 else ''
    fa2 = parts[2] if len(parts) > 2 else ''
    cookie = ''
    token = ''
    email = ''
    for p in parts[3:]:
        if 'c_user=' in p:
            cookie = p
        elif p.startswith('EAAAA'):
            token = p
        elif '@' in p:
            email = p
    return uid, password, fa2, cookie, token, email

def check_facebook_uid(uid):
    url = f"{FB_CHECK_URL}{uid}"
    response = requests.get(url)
    if response.status_code == 200 and 'id' in response.json():
        return True
    return False

def build_reply(uid, password, fa2, cookie, token, email):
    status = "Nick Live" if check_facebook_uid(uid) else "Nick Die"
    link = f"https://facebook.com/profile.php?id={uid}"
    result = f"""UID: {uid}
Mật khẩu: {password}
2FA: {fa2}
Trạng thái: {status}
Link: {link}
"""
    if cookie:
        result += f"Cookie: {cookie}\n"
    if token:
        result += f"Token: {token}\n"
    if email:
        result += f"Email: {email}\n"
    return result

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        lines = text.strip().splitlines()
        reply = ""
        for line in lines:
            if "|" in line:
                uid, password, fa2, cookie, token, email = parse_line(line)
                if uid and password:
                    reply += build_reply(uid, password, fa2, cookie, token, email) + "\n"
        if reply:
            requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run()
