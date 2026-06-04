import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "7572855587:AAGfeCPagVcyfWClV939PXFhZyq8Se354No")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "68797657"))

# Conversation states
WAITING_NAME, WAITING_PHONE, WAITING_ADDRESS = range(3)

PRODUCTS = [
    {"id": 1,  "name": "وکیوم برقی شارژی آقایان",        "desc": "دستگاه وکیوم برقی شارژی با کیفیت بالا، مناسب برای آقایان، قابل شارژ با USB، همراه با کیف حمل."},
    {"id": 2,  "name": "کرم روشن کننده پولونکس",          "desc": "کرم روشن‌کننده پولونکس با فرمول پیشرفته، مناسب برای روشن‌سازی و یکدست کردن رنگ پوست."},
    {"id": 3,  "name": "کرم حجم دهنده پولونکس S6",        "desc": "کرم حجم‌دهنده پولونکس S6، با فرمول تخصصی برای افزایش حجم و استحکام."},
    {"id": 4,  "name": "شربت تقویت نعوظ ویرمان VIP",      "desc": "شربت تقویتی ویرمان VIP، محصول طبیعی برای تقویت عملکرد جنسی آقایان."},
    {"id": 5,  "name": "شربت تاخیری ویرمان VIP",           "desc": "شربت تاخیری ویرمان VIP، فرمول طبیعی برای افزایش زمان و کیفیت روابط."},
    {"id": 6,  "name": "ژل روان کننده پولونکس",            "desc": "ژل روان‌کننده پولونکس، فاقد رنگ و بو، مناسب برای پوست حساس."},
    {"id": 7,  "name": "ژل تنگ کننده اینتیمکس",           "desc": "ژل تنگ‌کننده اینتیمکس، حاوی ترکیبات گیاهی، مخصوص بانوان، سریع‌الاثر."},
    {"id": 8,  "name": "ژل تقویت نعوظ پولونکس",           "desc": "ژل تقویت نعوظ پولونکس، جذب سریع، فرمول تخصصی برای بهبود عملکرد جنسی آقایان."},
    {"id": 9,  "name": "ژل افزایش میل بانوان پولونکس",    "desc": "ژل افزایش میل پولونکس برای بانوان، با ترکیبات طبیعی و اثرگذاری سریع."},
    {"id": 10, "name": "روغن ماساژ پولونکس X1",            "desc": "روغن ماساژ پولونکس X1، با رایحه ملایم، مناسب برای ماساژ درمانی و آرامش‌بخش."},
    {"id": 11, "name": "اسپری آقایان اینتیمکس",            "desc": "اسپری اینتیمکس برای آقایان، تاخیردهنده و تقویت‌کننده، بدون عوارض جانبی."},
    {"id": 12, "name": "اسپری بانوان اینتیمکس",            "desc": "اسپری اینتیمکس برای بانوان، افزایش حساسیت و لذت، فرمول ملایم و ایمن."},
    {"id": 13, "name": "اسپری تاخیری گالاردو 212",         "desc": "اسپری تاخیری گالاردو 212، محصول پرفروش با اثرگذاری سریع و ماندگاری بالا."},
]

PAYMENT_INFO = """💳 *اطلاعات پرداخت*

🏦 بانک: ملی
💳 کارت: `6037-9975-3343-3026`
🔢 حساب: `0105397618001`
🔁 شبا: `IR790170000000105397618001`
👤 نام صاحب حساب: امیررضا کریم

━━━━━━━━━━━━━━
⚠️ لطفاً مبلغ را واریز کرده، سپس اطلاعات سفارش را وارد کنید."""


def get_main_menu():
    keyboard = [[InlineKeyboardButton("🛍 محصولات", callback_data="products")]]
    return InlineKeyboardMarkup(keyboard)


def get_products_keyboard():
    keyboard = []
    for i in range(0, len(PRODUCTS), 2):
        row = [InlineKeyboardButton(PRODUCTS[i]["name"], callback_data=f"product_{PRODUCTS[i]['id']}")]
        if i + 1 < len(PRODUCTS):
            row.append(InlineKeyboardButton(PRODUCTS[i+1]["name"], callback_data=f"product_{PRODUCTS[i+1]['id']}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *به فروشگاه ما خوش آمدید!*\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text(
            "👋 *به فروشگاه ما خوش آمدید!*\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )

    elif data == "products":
        await query.edit_message_text(
            "🛍 *لیست محصولات*\n\nمحصول مورد نظر خود را انتخاب کنید:",
            reply_markup=get_products_keyboard(),
            parse_mode="Markdown"
        )

    elif data.startswith("product_"):
        product_id = int(data.split("_")[1])
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            keyboard = [
                [InlineKeyboardButton("🛒 ثبت سفارش", callback_data=f"order_{product_id}")],
                [InlineKeyboardButton("🔙 بازگشت به محصولات", callback_data="products")]
            ]
            await query.edit_message_text(
                f"📦 *{product['name']}*\n\n📝 {product['desc']}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

    elif data.startswith("order_"):
        product_id = int(data.split("_")[1])
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            context.user_data["ordered_product"] = product["name"]
            keyboard = [[InlineKeyboardButton("🔙 لغو سفارش", callback_data="products")]]
            await query.edit_message_text(
                PAYMENT_INFO + "\n\n✅ پس از واریز، *نام و نام خانوادگی* خود را بنویسید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return WAITING_NAME

    return ConversationHandler.END


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 *شماره تماس* خود را وارد کنید:", parse_mode="Markdown")
    return WAITING_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📍 *آدرس کامل* خود را وارد کنید:", parse_mode="Markdown")
    return WAITING_ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    product = context.user_data.get("ordered_product", "نامشخص")
    name    = context.user_data.get("name", "")
    phone   = context.user_data.get("phone", "")
    address = context.user_data.get("address", "")

    order_message = (
        f"🛒 *سفارش جدید*\n\n"
        f"📦 محصول: {product}\n"
        f"👤 نام: {name}\n"
        f"📞 شماره: {phone}\n"
        f"📍 آدرس: {address}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=order_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error sending to admin: {e}")

    await update.message.reply_text(
        "✅ *سفارش شما با موفقیت ثبت شد!*\n\n"
        "🙏 ممنون از خریدتان. به زودی با شما تماس خواهیم گرفت.\n\n"
        "برای بازگشت به منو دستور /start را بزنید.",
        parse_mode="Markdown"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❌ سفارش لغو شد.\n\nبرای شروع مجدد /start را بزنید.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            WAITING_NAME:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            WAITING_PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            WAITING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(button_handler),
        ],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    logger.info("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
