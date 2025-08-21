import os
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from bot_handlers import (
    start, button_handler, test_start_handler, 
    answer_handler, account_handler, admin_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Get bot token from environment variable
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
    
    # Create the Application
    application = Application.builder().token(bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(test|account|admin|back_main)$"))
    application.add_handler(CallbackQueryHandler(test_start_handler, pattern="^test_"))
    application.add_handler(CallbackQueryHandler(answer_handler, pattern="^answer_"))
    application.add_handler(CallbackQueryHandler(account_handler, pattern="^account_"))
    application.add_handler(CallbackQueryHandler(admin_handler, pattern="^admin_"))
    
    # Run the bot
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
