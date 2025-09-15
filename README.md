import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Bot tokenini shu yerga kiriting
BOT_TOKEN = "8290213646:AAFuNi6cb-Utic4cYH22x7SyFZGbB7rMXJM"

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Notebook ma'lumotlari
NOTEBOOKS = {
    "macbook_air": {
        "name": "MacBook Air M3",
        "price": "$1299",
        "specs": "15.3-inch Liquid Retina display, Apple M3 chip, 8GB RAM, 256GB SSD",
        "image": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba15-midnight-select-202306?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1684518479433"
    },
    "dell_xps": {
        "name": "Dell XPS 13",
        "price": "$999",
        "specs": "13.4-inch InfinityEdge display, Intel Core i7, 16GB RAM, 512GB SSD",
        "image": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/13-9340/media-gallery/notebook-xps-13-9340-nt-blue-gallery-2.psd?fmt=png-alpha&pscan=auto&scl=1&hei=402&wid=402&qlt=100,1&resMode=sharp2&size=402,402&chrss=full"
    },
    "hp_spectre": {
        "name": "HP Spectre x360",
        "price": "$1149",
        "specs": "13.5-inch OLED touchscreen, Intel Core i7, 16GB RAM, 512GB SSD",
        "image": "https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c07791967.png"
    },
    "lenovo_thinkpad": {
        "name": "Lenovo ThinkPad X1 Carbon",
        "price": "$1399",
        "specs": "14-inch 2.8K OLED display, Intel Core i7, 16GB RAM, 512GB SSD",
        "image": "https://p3-ofp.static.pub/fes/cms/2023/08/14/8s4bvd8dgjwii9vo1tqe9o8ajpg6sz518637.png"
    },
    "asus_zenbook": {
        "name": "ASUS ZenBook 14",
        "price": "$899",
        "specs": "14-inch OLED display, AMD Ryzen 7, 16GB RAM, 512GB SSD",
        "image": "https://dlcdnwebimgs.asus.com/gain/2E9E78A3-F4A0-4062-8860-CE05FCD83E31/w800/h600"
    }
}

# Foydalanuvchi ma'lumotlarini saqlash uchun
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlanganda ishlaydigan funksiya"""
    user = update.effective_user
    welcome_text = f"Salom {user.first_name}! 👋\n\n"
    welcome_text += "Men sizga eng zo'r notebooklar haqida ma'lumot beraman! 💻\n\n"
    welcome_text += "Avval o'zingizni tanishtiring:"

    # Kontakt so'rash tugmasi
    keyboard = [
        [KeyboardButton("📱 Kontakt ma'lumotlarini yuborish", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kontakt ma'lumotlarini qabul qilish"""
    contact = update.message.contact
    user_id = update.effective_user.id

    # Foydalanuvchi ma'lumotlarini saqlash
    user_data[user_id] = {
        'name': contact.first_name + (" " + contact.last_name if contact.last_name else ""),
        'phone': contact.phone_number
    }

    success_text = f"Rahmat, {user_data[user_id]['name']}! ✅\n\n"
    success_text += "Endi sizga 5 ta eng zo'r notebookni tavsiya qilaman:"

    # Notebook tanlov tugmalari
    keyboard = []
    for key, notebook in NOTEBOOKS.items():
        keyboard.append([InlineKeyboardButton(
            f"💻 {notebook['name']} - {notebook['price']}",
            callback_data=f"notebook_{key}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(success_text, reply_markup=reply_markup)


async def notebook_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Notebook tanlanganda ishlaydigan funksiya"""
    query = update.callback_query
    await query.answer()

    notebook_key = query.data.split("_", 1)[1]
    notebook = NOTEBOOKS[notebook_key]

    text = f"💻 *{notebook['name']}*\n\n"
    text += f"💰 Narx: {notebook['price']}\n\n"
    text += f"📋 Xususiyatlari:\n{notebook['specs']}\n\n"
    text += "Bu notebook haqida batafsil ma'lumot yuqoridagi rasmda ko'rishingiz mumkin! 👆"

    try:
        await query.message.reply_photo(
            photo=notebook['image'],
            caption=text,
            parse_mode='Markdown'
        )
    except:
        await query.message.reply_text(text, parse_mode='Markdown')

    keyboard = [
        [InlineKeyboardButton("🛒 Sotib olish", callback_data=f"buy_{notebook_key}")],
        [InlineKeyboardButton("🔙 Boshqa notebooklar", callback_data="back_to_list")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("Bu notebookni sotib olishni xohlaysizmi?", reply_markup=reply_markup)


async def buy_notebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sotib olish jarayoni"""
    query = update.callback_query
    await query.answer()

    notebook_key = query.data.split("_", 1)[1]
    notebook = NOTEBOOKS[notebook_key]
    user_id = update.effective_user.id

    if user_id not in user_data:
        await query.message.reply_text(
            "❗️ Avval kontakt ma'lumotlaringizni yuboring!\n"
            "Buning uchun /start buyrug'ini bosing."
        )
        return

    user_info = user_data[user_id]

    # Yangilangan buyurtma matni
    order_text = (
        f"✅ BUYURTMA TASDIQLANDI!\n\n"
        f"👤 Mijoz: {user_info['name']}\n"
        f"📞 Telefon: {user_info['phone']}\n\n"
        f"💻 Mahsulot: {notebook['name']}\n"
        f"💰 Narx: {notebook['price']}\n"
        f"📋 Xususiyatlari: {notebook['specs']}\n\n"
        f"🕐 Yetkazib berish muddati: 3-5 ish kuni\n"
        f"🚚 Yetkazib berish: Bepul (Xorazm bo'ylab)\n\n"
        f"📞 Aloqa uchun: +998 88 360 8285\n"
        f"💬 Telegram: @o_umrbek_008\n\n"
        f"✨ Tez orada siz bilan bog'lanamiz!"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Yana buyurtma berish", callback_data="back_to_list")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(order_text, parse_mode='Markdown', reply_markup=reply_markup)


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bosh menyu callback"""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    welcome_text = f"Salom {user.first_name}! 👋\n\n"
    welcome_text += "Men sizga eng zo'r notebooklar haqida ma'lumot beraman! 💻\n\n"
    welcome_text += "Notebook tanlov qilish uchun tugmani bosing:"

    keyboard = [[InlineKeyboardButton("💻 Notebooklar ro'yxati", callback_data="back_to_list")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(welcome_text, reply_markup=reply_markup)


async def back_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Notebook ro'yxatiga qaytish"""
    query = update.callback_query
    await query.answer()

    keyboard = []
    for key, notebook in NOTEBOOKS.items():
        keyboard.append([InlineKeyboardButton(
            f"💻 {notebook['name']} - {notebook['price']}",
            callback_data=f"notebook_{key}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("5 ta eng zo'r notebook:", reply_markup=reply_markup)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bosh menyu"""
    if update.message.text == "🔙 Bosh menyu":
        await start(update, context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Xatoliklarni qayta ishlash"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(CallbackQueryHandler(notebook_callback, pattern="^notebook_"))
    application.add_handler(CallbackQueryHandler(buy_notebook, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(back_to_list, pattern="^back_to_list$"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    application.add_handler(MessageHandler(filters.TEXT, menu_handler))

    application.add_error_handler(error_handler)

    print("Bot ishga tushdi! Ctrl+C bilan to'xtatish mumkin.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
