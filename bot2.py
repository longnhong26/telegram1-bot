import sqlite3
import telebot
from telebot import types

# ==== CẤU HÌNH ====

TOKEN = "7854138406:AAH3GmpX8AW-bPaYkyW0ig9YUoR0XT7Rf68"
DB_FILE = "users.db"

QR_MONTH = "https://drive.google.com/uc?export=download&id=1iktGwlAFyY9dUTKftHSDAiM01B_sECZL"
QR_YEAR = "https://drive.google.com/uc?export=download&id=1iktGwlAFyY9dUTKftHSDAiM01B_sECZL"
QR_LIFETIME = "https://drive.google.com/uc?export=download&id=1iktGwlAFyY9dUTKftHSDAiM01B_sECZL"

bot = telebot.TeleBot(TOKEN)

# ==== KHỞI TẠO DB ====

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        phone TEXT
    )
""")
conn.commit()

# ==== /start ====

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    intro = (
        "ĐỘNG LINK 18 THIÊN ĐƯỜNG GIẢI TRÍ DÀNH CHO ANH EM 🔞\n"
        "➡ Kho hơn 25.000 video 18+, show hàng, lộ link, hack cam…\n\n"
        "➡ Cập nhật video hàng ngày\n\n"
        "➡ Xem trực tiếp trong nhóm không cần vượt link\n\n"
        "➡ Không quảng cáo\n\n"
        "➡ Bảo mật thông tin khách hàng\n\n"
        "Chọn gói đăng ký ở bên dưới 👇"
    )
    bot.send_message(uid, intro)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("VIP THÁNG 🔑", "VIP NĂM 🔑", "VIP VĨNH VIỄN 🔑")
    bot.send_message(uid, "Chọn gói:", reply_markup=markup)

# ==== XỬ LÝ MENU ====

@bot.message_handler(func=lambda msg: msg.text in ["VIP THÁNG 🔑", "VIP NĂM 🔑", "VIP VĨNH VIỄN 🔑"])
def handle_menu(message):
    uid = message.chat.id
    text = message.text

    if text == "VIP THÁNG 🔑":
        caption = (
            "🔓MỞ KHOÁ VIP THÁNG (Sử dụng dịch vụ 3 tháng)\n\n"
            "“Ấn và giữ vào ảnh để lưu ảnh mã QR”\n\n"
            "♻️ HƯỚNG DẪN ĐĂNG KÝ\n\n"
            "• Chuyển số tiền 99.000 VNĐ\n"
            "• Để lại số điện thoại đăng ký telegram ở nội dung chuyển khoản\n"
            "• Sai hoặc thiếu nội dung sẽ không được duyệt nhóm"
        )
        bot.send_photo(uid, QR_MONTH, caption=caption)
    elif text == "VIP NĂM 🔑":
        caption = (
            "🔓MỞ KHOÁ VIP NĂM (Sử dụng dịch vụ 1 năm)\n\n"
            "“Ấn và giữ vào ảnh để lưu ảnh mã QR”\n\n"
            "♻️ HƯỚNG DẪN ĐĂNG KÝ\n\n"
            "• Chuyển số tiền 299.000 VNĐ\n"
            "• Để lại số điện thoại đăng ký telegram ở nội dung chuyển khoản\n"
            "• Sai hoặc thiếu nội dung sẽ không được duyệt nhóm"
        )
        bot.send_photo(uid, QR_YEAR, caption=caption)
    elif text == "VIP VĨNH VIỄN 🔑":
        caption = (
            "🔓MỞ KHOÁ VIP VĨNH VIỄN (Sử dụng dịch vụ vĩnh viễn)\n\n"
            "“Ấn và giữ vào ảnh để lưu ảnh mã QR”\n\n"
            "♻️ HƯỚNG DẪN ĐĂNG KÝ\n\n"
            "• Chuyển số tiền 599.000 VNĐ\n"
            "• Để lại số điện thoại đăng ký telegram ở nội dung chuyển khoản\n"
            "• Sai hoặc thiếu nội dung sẽ không được duyệt nhóm"
        )
        bot.send_photo(uid, QR_LIFETIME, caption=caption)

    bot.send_message(uid, "Khi đã chuyển khoản xong, hãy gửi lệnh:\n\n/done <số_điện_thoại>\n\nVí dụ: /done 0912345678")

# ==== /done ====

@bot.message_handler(commands=['done'])
def done(message):
    uid = message.chat.id
    args = message.text.split()

    if len(args) != 2 or not args[1].isdigit():
        bot.send_message(uid, "❌ Vui lòng gửi đúng: /done 0912345678")
        return

    phone = args[1]
    c.execute("REPLACE INTO users (user_id, phone) VALUES (?, ?)", (uid, phone))
    conn.commit()
    bot.send_message(uid, "✅ Đã lưu thông tin. Vui lòng đợi xác nhận thanh toán…")

# ==== CHẠY BOT ====

print("🚀 Bot đang chạy…")
bot.infinity_polling()
