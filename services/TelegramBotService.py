import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, ApplicationBuilder
from dotenv import load_dotenv
from common import GlobalValue
from services.chat_ai.IChatAIService import IChatAIHandler
from services.chat_ai.ClaudeAIService import ClaudeAIService
from services.chat_ai.ChatGPTAIService import ChatGPTAIService

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TelegramBotService:
    """
    The TelegramBotService class is responsible for running a Telegram bot 
    that can interact with the chosen AI.
    """
    _claude_service: ClaudeAIService = None
    _chat_gpt_service: ChatGPTAIService = None
    _chat_ai_service: IChatAIHandler = None

    def __init__(self) -> None:
        self._claude_service = ClaudeAIService()
        self._chat_gpt_service = ChatGPTAIService()

    def run(self):
        application = ApplicationBuilder().token(GlobalValue.TELEGRAM_BOT_API_KEY).build()
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, self.handle_message))
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: CallbackContext):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a Telegram bot that can interact with the Claude AI. Send me a message, and I'll pass it to Claude.")

    async def handle_message(self, update: Update, context: CallbackContext):
        user_message = update.message.text
        self._set_chat_ai_service(self._claude_service)
        message_response = await self._chat_ai_service.get_response(str(update._effective_user.id), user_message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_response)
        
    def _set_chat_ai_service(self, service: IChatAIHandler):
        self._chat_ai_service = service
