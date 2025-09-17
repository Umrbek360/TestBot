BU BOT o'quvchilardan test oladi
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# BOT TOKENNI YANGILANG VA HECH QACHON HAMMA KO'RSIN DEB QO'YMANG!
BOT_TOKEN = "8290213646:AAFuNi6cb-Utic4cYH22x7SyFZGbB7rMXJM"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)  # name -> name

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
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6FHCiWQh-HSwK-hl696K9S2r7rrCoD80C9A&s"
    },
    "hp_spectre": {
        "name": "HP Spectre x360",
        "price": "$1149",
        "specs": "13.5-inch OLED touchscreen, Intel Core i7, 16GB RAM, 512GB SSD",
        "image": "https://olcha.uz/image/700x700/products/2022-07-05/noutbuk-hp-spectre-x360-16-2-1-i7-11390h-16512gb-ssd-iris-xe-16-16-f0013dx-63252-6.jpeg"
    },
    "lenovo_thinkpad": {
        "name": "Lenovo ThinkPad X1 Carbon",
        "price": "$1399",
        "specs": "14-inch 2.8K OLED display, Intel Core i7, 16GB RAM, 512GB SSD",
        "image": "https://api.cabinet.smart-market.uz/uploads/images/ff8081816152da5cd2f099ec"
    },
    "asus_zenbook": {
        "name": "ASUS ZenBook 14",
        "price": "$899",
        "specs": "14-inch OLED display, AMD Ryzen 7, 16GB RAM, 512GB SSD",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8pZzkQo6YHIW7T2Ns4ZyWOQ0xDOqcicDiXg&s"
    }
}

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"Salom {user.first_name}! 👋\n\n"
        "Men sizga eng zo'r notebooklar haqida ma'lumot beraman! 💻\n\n"
        "Avval o'zingizni tanishtiring:"
    )

    keyboard = [[KeyboardButton("📱 Kontakt ma'lumotlarini yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.effective_user.id

    user_data[user_id] = {
        'name': contact.first_name + (" " + contact.last_name if contact.last_name else ""),
        'phone': contact.phone_number
    }

    success_text = f"Rahmat, {user_data[user_id]['name']}! ✅\n\nEndi sizga 5 ta eng zo'r notebookni tavsiya qilaman:"

    keyboard = [
        [InlineKeyboardButton(f"💻 {notebook['name']} - {notebook['price']}", callback_data=f"notebook_{key}")]
        for key, notebook in NOTEBOOKS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(success_text, reply_markup=reply_markup)

async def notebook_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    notebook_key = query.data.split("_", 1)[1]
    notebook = NOTEBOOKS[notebook_key]

    text = (
        f"💻 *{notebook['name']}*\n\n"
        f"💰 Narx: {notebook['price']}\n\n"
        f"📋 Xususiyatlari:\n{notebook['specs']}\n\n"
        "Bu notebook haqida batafsil ma'lumot yuqoridagi rasmda ko'rishingiz mumkin! 👆"
    )
try:
        # Xabarni rasm bilan yangilash uchun:
        await query.message.delete()  # Avval eski xabarni o'chirish (ixtiyoriy)
        await query.message.chat.send_photo(
            photo=notebook['image'],
            caption=text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Sotib olish", callback_data=f"buy_{notebook_key}")],
                [InlineKeyboardButton("🔙 Boshqa notebooklar", callback_data="back_to_list")]
            ])
        )
    except Exception as e:
        logger.error(f"Rasm yuklashda xato: {e}")
        # Rasm yuklanmasa, matnli xabarni yangilash
        await query.message.edit_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Sotib olish", callback_data=f"buy_{notebook_key}")],
                [InlineKeyboardButton("🔙 Boshqa notebooklar", callback_data="back_to_list")]
            ])
        )

async def buy_notebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    notebook_key = query.data.split("_", 1)[1]
    notebook = NOTEBOOKS[notebook_key]
    user_id = query.from_user.id

    if user_id not in user_data:
        await query.message.reply_text("❗️ Avval kontakt ma'lumotlaringizni yuboring!\n/start buyrug'ini bosing.")
        return

    user_info = user_data[user_id]

    order_text = (
        f"✅ BUYURTMA TASDIQLANDI!\n\n"
        f"👤 Mijoz: {user_info['name']}\n"
        f"📞 Telefon: {user_info['phone']}\n\n"
        f"💻 Mahsulot: {notebook['name']}\n"
        f"💰 Narx: {notebook['price']}\n"
        f"📋 Xususiyatlari: {notebook['specs']}\n\n"
        f"🕐 Yetkazib berish muddati: 3-5 ish kuni\n"
        f"🚚 Yetkazib berish: Bepul (XORAZIM bo'ylab)\n\n"
        f"📞 Aloqa uchun: +998 88 360 82 85\n"
        f"💬 Telegram: https://t.me/o_umrbek_008 \n\n"
        f"✨ *Tez orada siz bilan bog'lanamiz!*"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Yana buyurtma berish", callback_data="back_to_list")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(order_text, parse_mode='Markdown', reply_markup=reply_markup)

async def back_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(f"💻 {notebook['name']} - {notebook['price']}", callback_data=f"notebook_{key}")]
        for key, notebook in NOTEBOOKS.items()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("5 ta eng zo'r notebook:", reply_markup=reply_markup)

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    welcome_text = (
        f"Salom {user.first_name}! 👋\n\n"
        "Men sizga eng zo'r notebooklar haqida ma'lumot beraman! 💻\n\n"
        "Quyidagi ro'yxatdan notebook tanlang:"
    )

    keyboard = [
        [InlineKeyboardButton(f"💻 {notebook['name']} - {notebook['price']}", callback_data=f"notebook_{key}")]
        for key, notebook in NOTEBOOKS.items()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(welcome_text, reply_markup=reply_markup)

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Bosh menyu":
        await start(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
Telegram
Umrbek Obdullayev🖤

SEND MESSAGE
application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(CallbackQueryHandler(notebook_callback, pattern="^notebook_"))
    application.add_handler(CallbackQueryHandler(buy_notebook, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(back_to_list, pattern="^back_to_list$"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), menu_handler))

    application.add_error_handler(error_handler)

    print("✅ Bot ishga tushdi! Ctrl+C bilan to'xtatish mumkin.")
    application.run_polling()

if name == 'main':  # name -> name
    main()
