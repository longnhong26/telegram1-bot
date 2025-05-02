import telebot   # Thư viện TeleBot để viết bot Telegram
import requests  # Thư viện để gọi API HTTP

# Token bot Telegram của bạn
TOKEN = "7831505272:AAGRgRwNce221xAR9ER-Qo5Dv_LYRrjqOXg"
bot = telebot.TeleBot(TOKEN)

# Xử lý lệnh /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Xin chào! Nhập danh sách UID (mỗi UID một dòng hoặc cách nhau bằng khoảng trắng).")

# Xử lý tin nhắn chứa UID
@bot.message_handler(func=lambda message: True)
def check_uids(message):
    uids = message.text.split()
    reply_lines = []
    for uid in uids:
        # Gọi Graph API lấy ảnh đại diện
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

# Chạy bot
print("Bot đang chạy...")
bot.polling()
