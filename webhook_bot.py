import telebot
from flask import Flask, request

API_TOKEN = '7831505272:AAGRgRwNce221xAR9ER-Qo5Dv_LYRrjqOXg'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Nhập UID Facebook để kiểm tra.")

@bot.message_handler(func=lambda message: True)
def check_uids(message):
    import requests
    uids = message.text.split()
    reply_lines = []
    for uid in uids:
        url = f"https://graph.facebook.com/{uid}/picture?redirect=false"
        try:
            res = requests.get(url).json()
            if 'data' in res and 'url' in res['data']:
                is_silhouette = res['data'].get('is_silhouette', True)
                if not is_silhouette:
                    status = "Nick Live"
                else:
                    status = "Nick Live (mặc định ảnh)"
            else:
                status = "Nick Die"
            link = f"https://facebook.com/profile.php?id={uid}"
            reply_lines.append(f"UID: {uid}\nTrạng thái: {status}\nLink: {link}")
        except Exception as e:
            reply_lines.append(f"UID: {uid}\nLỗi: {str(e)}")

    reply = "\n\n".join(reply_lines)
    bot.send_message(message.chat.id, reply)

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/')
def index():
    return 'Bot is running via webhook!'

if name == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
