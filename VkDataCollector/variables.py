import os
from dotenv import load_dotenv
import telebot

# Load environment variables from .env file
load_dotenv(dotenv_path = '.env')
token = os.getenv('VK_API_SERVICE_TOKEN')
version = os.getenv('VK_API_VERSION')
url = os.getenv('URL')
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'), parse_mode=None)
telegram_watcher_id = os.getenv('TELEGRAM_WATCHER_ID')