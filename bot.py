import telebot

# Thay token dưới đây bằng token bot Telegram của bạn
TOKEN = '7831505272:AAGRgRwNce221xAR9ER-Qo5Dv_LYRrjqOXg'
bot = telebot.TeleBot(TOKEN)

# Hàm xử lý khi có người nhắn tin bất kỳ
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Bạn vừa nói: {message.text}")

print("Bot đang chạy...")
bot.polling()
import telebot   # Thư viện TeleBot để viết bot Telegram
import requests  # Thư viện để gọi API HTTP

# Thay YOUR_TELEGRAM_BOT_TOKEN bằng token bạn nhận được từ BotFather
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Xử lý lệnh /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Xin chào! Nhập danh sách UID (mỗi UID một dòng hoặc cách nhau bằng khoảng trắng).")

# Xử lý tin nhắn chứa UID
@bot.message_handler(func=lambda message: True)
def check_uids(message):
    # Tách các UID từ tin nhắn
    uids = message.text.split()
    reply_lines = []
    for uid in uids:
        # Gọi Graph API lấy ảnh đại diện (không redirect)
        url = f"https://graph.facebook.com/{uid}/picture?redirect=false"
        res = requests.get(url).json()
        # Kiểm tra kết quả
        if 'data' in res and 'url' in res['data']:
            # Xem thử có phải ảnh mặc định (silhouette) hay không
            is_silhouette = res['data'].get('is_silhouette', True)
            if not is_silhouette:
                status = "Nick Live"           # Tài khoản có ảnh đại diện riêng
            else:
                status = "Nick Live (mặc định ảnh)"
        else:
            status = "Nick Die"              # Không tìm thấy dữ liệu => coi như chết
        # Tạo đường dẫn Facebook từ UID
        link = f"https://facebook.com/profile.php?id={uid}"
        # Thêm kết quả vào danh sách
        reply_lines.append(f"UID: {uid}\nTrạng thái: {status}\nLink: {link}")
    # Ghép kết quả và gửi trả lại
    reply = "\n\n".join(reply_lines)
    bot.send_message(message.chat.id, reply)

# Bắt đầu bot (long polling)
bot.polling()
