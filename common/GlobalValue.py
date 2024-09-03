import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_API_KEY: str = os.getenv('TELEGRAM_BOT_API_KEY')
ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY')
OPEN_AI_API_KEY: str = os.getenv('OPEN_AI_API_KEY')
MAX_MESSAGE_ARRAY_LENGTH: int = int(os.getenv('MAX_MESSAGE_ARRAY_LENGTH'))
MAX_TOKEN_PER_MESSAGE: int = 1024
MAX_TOTAL_TOKEN_USAGE: int = 100000