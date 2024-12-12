import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from .handlers import Handlers
from ...logger import logger

load_dotenv()

class TelegramBot:
    def __init__(self, token=None, assistant_instance=None):
        self.token = token if token else os.environ.get("TELEGRAM_BOT_KEY", "")
        self.application = ApplicationBuilder().token(self.token).build()
        self.handlers_instance = Handlers(assistant_instance=assistant_instance)
        self.add_handlers()

    def add_handlers(self):
        self.application.add_handler(CommandHandler("help", self.handlers_instance.help_command))
        self.application.add_handler(CommandHandler("reset", self.handlers_instance.reset_command))
        self.application.add_handler(CommandHandler("history", self.handlers_instance.history_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), self.handlers_instance.any_message)
        )

    def run(self):
        logger.info("Starting bot...")
        self.application.run_polling()