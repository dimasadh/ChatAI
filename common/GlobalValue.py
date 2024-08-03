import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_API_KEY: str = os.getenv('TELEGRAM_BOT_API_KEY')
ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY')
OPEN_AI_API_KEY: str = os.getenv('OPEN_AI_API_KEY')