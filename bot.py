cat > /mnt/user-data/outputs/final-bot/bot.py << 'BOTEOF'
import os
import logging
import random
import string
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "7572855587:AAGfeCPagVcyfWClV939PXFhZyq8Se354No")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "68797657"))

WAITING_RECEIPT, WAITING_NAME, WAITING_PHONE, WAITING_ADDRESS = range(4)

PRODUCTS = [
    {"id": 1,  "name": "وکیوم برقی شارژی آقایان",      "desc": "⚡ دستگاه وکیوم برقی شارژی با کیفیت بالا\n🔋 قابل شارژ با USB\n🎒 همراه با کیف حمل اختصاصی\n✅ گارانتی اصالت کالا"},
    {"id": 2,  "name": "کرم روشن کننده پولونکس",        "desc": "✨ فرمول پیشرفته روشن‌سازی پوست\n🌿 حاوی ترکیبات طبیعی\n💧 مناسب انواع پوست\n✅ گارانتی اصالت کالا"},
    {"id": 3,  "name": "کرم حجم دهنده پولونکس S6",      "desc": "💪 فرمول تخصصی افزایش حجم\n🔬 تکنولوژی S6 پیشرفته\n⚡ نتیجه سریع و ماندگار\n✅ گارانتی اصالت کالا"},
    {"id": 4,  "name": "شربت تقویت نعوظ ویرمان VIP",    "desc": "👑 محصول VIP ویرمان\n🌿 ترکیبات ۱۰۰٪ طبیعی\n⚡ اثرگذاری سریع\n✅ گارانتی اصالت کالا"},
    {"id": 5,  "name": "شربت تاخیری ویرمان VIP",         "desc": "👑 فرمول تاخیری VIP\n🌿 بدون عوارض جانبی\n⏱ افزایش چشمگیر زمان\n✅ گارانتی اصالت کالا"},
    {"id": 6,  "name": "ژل روان کننده پولونکس",          "desc": "💧 فاقد رنگ و بو\n🌿 مناسب پوست حساس\n✔️ سازگار با کاندوم\n✅ گارانتی اصالت کالا"},
    {"id": 7,  "name": "ژل تنگ کننده اینتیمکس",         "desc": "🌸 مخصوص بانوان\n🌿 حاوی ترکیبات گیاهی\n⚡ سریع‌الاثر و ایمن\n✅ گارانتی اصالت کالا"},
    {"id": 8,  "name": "ژل تقویت نعوظ پولونکس",         "desc": "💪 جذب فوری\n🔬 فرمول تخصصی\n⚡ اثرگذاری قوی\n✅ گارانتی اصالت کالا"},
    {"id": 9,  "name": "ژل افزایش میل بانوان پولونکس",  "desc": "🌸 ویژه بانوان\n🌿 ترکیبات طبیعی\n⚡ اثرگذاری سریع\n✅ گارانتی اصالت کالا"},
    {"id": 10, "name": "روغن ماساژ پولونکس X1",          "desc": "🌹 رایحه ملایم و دلپذیر\n💆 مناسب ماساژ درمانی\n🌿 فرمول آرامش‌بخش\n✅ گارانتی اصالت کالا"},
    {"id": 11, "name": "اسپری آقایان اینتیمکس",          "desc": "⚡ تاخیردهنده قوی\n💪 تقویت‌کننده عملکرد\n🌿 بدون عوارض جانبی\n✅ گارانتی اصالت کالا"},
    {"id": 12, "name": "اسپری بانوان اینتیمکس",          "desc": "🌸 افزایش حساسیت\n✨ فرمول ملایم و ایمن\n⚡ اثرگذاری سریع\n✅ گارانتی اصالت کالا"},
    {"id": 13, "name": "اسپری تاخیری گالاردو 212",       "desc": "🏆 پرفروش‌ترین محصول\n⚡ اثرگذاری فوری\n⏱ ماندگاری بالا\n✅ گارانتی اصالت کالا"},
]

def gen_order_id():
    return ''.join(random.choices(string.digits, k=6))

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍 مشاهده محصولات", callback_data="products")],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_products_keyboard():
    keyboard = []
    for i in range(0, len(PRODUCTS), 2):
        row = [InlineKeyboardButton(f"• {PRODUCTS[i]['name']}", callback_data=f"product_{PRODUCTS[i]['id']}")]
        if i + 1 < len(PRODUCTS):
            row.append(InlineKeyboardButton(f"• {PRODUCTS[i+1]['name']}", callback_data=f"product_{PRODUCTS[i+1]['id']}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 بازگشت به منو", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def cancel_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ لغو سفارش", callback_data="main_menu")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    text = (
        "━━━━━━━━━━━━━━━━━━\n"
        "🏪 *فروشگاه رسمی پولونکس*\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "سلام عزیز! 👋\n"
        "به فروشگاه تخصصی ما خوش آمدید.\n\n"
        "📦 ارسال به سراسر کشور\n"
        "🔒 پرداخت امن و مطمئن\n"
        "✅ ضمانت اصالت کالا\n\n"
        "از منوی زیر انتخاب کنید:"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        context.user_data.clear()
        text = (
            "━━━━━━━━━━━━━━━━━━\n"
            "🏪 *فروشگاه رسمی پولونکس*\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📦 ارسال به سراسر کشور\n"
            "🔒 پرداخت امن و مطمئن\n"
            "✅ ضمانت اصالت کالا\n\n"
            "از منوی زیر انتخاب کنید:"
        )
        await query.edit_message_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")

    elif data == "support":
        await query.edit_message_text(
            "📞 *پشتیبانی فروشگاه*\n\n"
            "برای ارتباط با پشتیبانی پیام دهید.\n"
            "⏰ پاسخگویی: ۹ صبح تا ۱۱ شب",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )

    elif data == "products":
        await query.edit_message_text(
            "🛍 *محصولات فروشگاه*\n\n"
            "محصول مورد نظر را انتخاب کنید:",
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
            text = (
                f"📦 *{product['name']}*\n"
                f"━━━━━━━━━━━━━━\n\n"
                f"{product['desc']}\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"برای ثبت سفارش دکمه زیر را بزنید:"
            )
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("order_"):
        product_id = int(data.split("_")[1])
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            order_id = gen_order_id()
            context.user_data["ordered_product"] = product["name"]
            context.user_data["order_id"] = order_id
            text = (
                f"🧾 *شماره سفارش: #{order_id}*\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"💳 *اطلاعات پرداخت:*\n\n"
                f"🏦 بانک ملی\n"
                f"💳 کارت: `6037-9975-3343-3026`\n"
                f"🔢 حساب: `0105397618001`\n"
                f"🔁 شبا: `IR790170000000105397618001`\n"
                f"👤 به نام: *امیررضا کریم*\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📸 پس از واریز، *فیش پرداخت* را همینجا ارسال کنید:"
            )
            await query.edit_message_text(text, reply_markup=cancel_keyboard(), parse_mode="Markdown")
            return WAITING_RECEIPT

    return ConversationHandler.END

async def get_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["receipt"] = update.message.photo[-1].file_id
        context.user_data["receipt_type"] = "photo"
    elif update.message.document:
        context.user_data["receipt"] = update.message.document.file_id
        context.user_data["receipt_type"] = "document"
    else:
        await update.message.reply_text(
            "⚠️ لطفاً *تصویر فیش* پرداخت را ارسال کنید:",
            reply_markup=cancel_keyboard(),
            parse_mode="Markdown"
        )
        return WAITING_RECEIPT

    await update.message.reply_text(
        "✅ فیش دریافت شد!\n\n👤 لطفاً *نام و نام خانوادگی* خود را وارد کنید:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    return WAITING_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "📞 لطفاً *شماره تماس* خود را وارد کنید:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    return WAITING_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text(
        "📍 لطفاً *آدرس کامل* (استان، شهر، خیابان، پلاک) را وارد کنید:",
        reply_markup=cancel_keyboard(),
        parse_mode="Markdown"
    )
    return WAITING_ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    product  = context.user_data.get("ordered_product", "نامشخص")
    name     = context.user_data.get("name", "")
    phone    = context.user_data.get("phone", "")
    address  = context.user_data.get("address", "")
    order_id = context.user_data.get("order_id", "------")
    receipt  = context.user_data.get("receipt")
    receipt_type = context.user_data.get("receipt_type", "photo")
    now = datetime.now().strftime("%Y/%m/%d - %H:%M")

    admin_text = (
        f"🛒 *سفارش جدید*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔖 شماره سفارش: #{order_id}\n"
        f"🕐 زمان: {now}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📦 محصول: {product}\n"
        f"👤 نام: {name}\n"
        f"📞 شماره: {phone}\n"
        f"📍 آدرس: {address}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    try:
        if receipt:
            if receipt_type == "photo":
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=receipt, caption=admin_text, parse_mode="Markdown")
            else:
                await context.bot.send_document(chat_id=ADMIN_ID, document=receipt, caption=admin_text, parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error sending to admin: {e}")

    await update.message.reply_text(
        f"🎉 *سفارش شما با موفقیت ثبت شد!*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🔖 شماره پیگیری: *#{order_id}*\n\n"
        f"📦 محصول: {product}\n"
        f"👤 نام: {name}\n"
        f"📞 شماره: {phone}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✅ سفارش شما دریافت و در حال بررسی است.\n"
        f"📲 به زودی با شما تماس خواهیم گرفت.\n\n"
        f"🙏 از خرید شما سپاسگزاریم!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏪 بازگشت به فروشگاه", callback_data="main_menu")]])
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
            WAITING_RECEIPT: [
                MessageHandler(filters.PHOTO | filters.Document.ALL, get_receipt),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_receipt),
            ],
            WAITING_NAME:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            WAITING_PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            WAITING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
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
BOTEOF
