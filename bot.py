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
