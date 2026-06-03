from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔴 توکن ربات (اینجا بگذار)
TOKEN = "7572855587:AAGfeCPagVcyfWClV939PXFhZyq8Se354No"

# 🔵 آیدی تو (ادمین)
ADMIN_ID = 68797657

user_data = {}

# 🏠 شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍 محصولات"]]

    await update.message.reply_text(
        "سلام 🌹\nبه فروشگاه خوش آمدید",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# 🛍 لیست محصولات
async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["وکیوم برقی شارژی آقایان"],
        ["کرم روشن کننده پولونکس"],
        ["کرم حجم دهنده پولونکس S6"],
        ["شربت ویرمان VIP (نعوظ)"],
        ["شربت ویرمان VIP (تاخیری)"],
        ["ژل روان کننده پولونکس"],
        ["ژل تنگ کننده اینتیمکس"],
        ["ژل تقویت نعوظ پولونکس"],
        ["ژل افزایش میل بانوان پولونکس"],
        ["روغن ماساژ پولونکس X1"],
        ["اسپری آقایان اینتیمکس"],
        ["اسپری بانوان اینتیمکس"],
        ["اسپری تاخیری گالاردو 212"],
    ]

    await update.message.reply_text(
        "🛍 محصولات:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# 📦 انتخاب محصول
async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"product": update.message.text}

    keyboard = [["🛒 ثبت سفارش"]]

    await update.message.reply_text(
        f"📦 {update.message.text}\n\n💰 برای ثبت سفارش روی دکمه زیر بزنید 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# 💳 پرداخت
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 اطلاعات پرداخت:\n\n"
        "🏦 بانک ملی\n"
        "💳 کارت: 6037997533433026\n"
        "🧾 حساب: 0105397618001\n"
        "🧷 شبا: IR790170000000105397618001\n"
        "👤 به نام: امیررضا کریم\n\n"
        "بعد از پرداخت، نام خود را وارد کنید:"
    )

# 🧠 گرفتن اطلاعات مشتری
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        return

    if "name" not in user_data[user_id]:
        user_data[user_id]["name"] = text
        await update.message.reply_text("شماره تماس را وارد کنید:")
    elif "phone" not in user_data[user_id]:
        user_data[user_id]["phone"] = text
        await update.message.reply_text("آدرس کامل را وارد کنید:")
    elif "address" not in user_data[user_id]:
        user_data[user_id]["address"] = text

        order = user_data[user_id]

        msg = f"""
🛒 سفارش جدید

📦 محصول: {order['product']}
👤 نام: {order['name']}
📞 موبایل: {order['phone']}
📍 آدرس: {order['address']}
"""

        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

        await update.message.reply_text("✅ سفارش ثبت شد")

        user_data.pop(user_id)

# 🚀 اجرا
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("🛍 محصولات"), products))

    products_list = [
        "وکیوم برقی شارژی آقایان",
        "کرم روشن کننده پولونکس",
        "کرم حجم دهنده پولونکس S6",
        "شربت ویرمان VIP (نعوظ)",
        "شربت ویرمان VIP (تاخیری)",
        "ژل روان کننده پولونکس",
        "ژل تنگ کننده اینتیمکس",
        "ژل تقویت نعوظ پولونکس",
        "ژل افزایش میل بانوان پولونکس",
        "روغن ماساژ پولونکس X1",
        "اسپری آقایان اینتیمکس",
        "اسپری بانوان اینتیمکس",
        "اسپری تاخیری گالاردو 212",
    ]

    for p in products_list:
        app.add_handler(MessageHandler(filters.Regex(p), product))

    app.add_handler(MessageHandler(filters.Regex("🛒 ثبت سفارش"), order))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
