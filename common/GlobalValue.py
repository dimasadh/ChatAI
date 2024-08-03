import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_API_KEY: str = os.getenv('TELEGRAM_BOT_API_KEY')
