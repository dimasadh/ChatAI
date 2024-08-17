import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
)
from common import GlobalValue
from common.Enums import Activity, ConversationState, Command, AI_MODEL
from services.chat_ai.IChatAIService import IChatAIHandler
from services.chat_ai.ClaudeAIService import ClaudeAIService
from services.chat_ai.ChatGPTAIService import ChatGPTAIService

# ! Make a logging helper!
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

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
        application = Application.builder().token(GlobalValue.TELEGRAM_BOT_API_KEY).build()

        # Add conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                ConversationState.CHOOSE_ACTIVITY.value: [
                    MessageHandler(filters.Regex(f"^({Activity.CHAT.value})$"),
                                   self.choose_activity)
                ],
                ConversationState.CHOOSE_AI_MODEL.value: [
                    MessageHandler(filters.Regex(f"^({AI_MODEL.CHATGPT.value}|{AI_MODEL.CLAUDE.value})$"),
                                   self.choose_ai_model)
                ],
                ConversationState.START_CHAT.value: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   self.start_chat), 
                    CommandHandler(Command.END.value, self.end_conversation)
                ],
            },
            fallbacks=[CommandHandler(Command.CANCEL.value, self.cancel)],
        )
        application.add_handler(conv_handler)

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: CallbackContext):
        reply_keyboard = [[Activity.CHAT.value]]
        await update.message.reply_text(
            "Hi! My name is ChatAI Bot.\n\n"
            "What do you want to do?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose an activity:"
            ),
        )
        return ConversationState.CHOOSE_ACTIVITY.value
    
    async def choose_activity(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info("User %s choose to %s", user.first_name, update.message.text)
        if update.message.text == Activity.CHAT.value:
            reply_keyboard = [[AI_MODEL.CHATGPT.value, AI_MODEL.CLAUDE.value]]
            await update.message.reply_text(
                "You can start conversation with the choosen AI model.\n\n"
                "Which AI model do you want to chat with?",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose an AI model:"
                ),
            )
            return ConversationState.CHOOSE_AI_MODEL.value
        else:
            return self.end_conversation(update, context)

    async def choose_ai_model(self, update: Update, context: CallbackContext) -> int:
        user = update.message.from_user
        chosen_ai = update.message.text
        logging.info("%s want to chat using %s", user.first_name, update.message.text)
        await update.message.reply_text(
            f"Enjoy your conversation with {chosen_ai}. You can end the conversation by typing /end.",
        )

        if chosen_ai == AI_MODEL.CHATGPT.value:
            self._chat_ai_service = self._chat_gpt_service
        elif chosen_ai == AI_MODEL.CLAUDE.value:
            self._chat_ai_service = self._claude_service
        else:
            logging.error("Invalid AI model selected.")
            await update.message.reply_text("Invalid AI model selected.")
            return ConversationState.CHOOSE_AI_MODEL.value

        logging.info("User %s started conversation with %s.", user.first_name, self._chat_ai_service.name)
        await update.message.reply_text(self._chat_ai_service.say_hi(user.first_name))

        return ConversationState.START_CHAT.value
    
    async def start_chat(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        message = update.message.text
        logging.info("User %s is chatting with %s.", user.first_name, self._chat_ai_service.name)
        message_response = await self._chat_ai_service.get_response(str(user.id), message)
        await update.message.reply_text(message_response)
    
    async def end_conversation(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info("User %s ended the conversation with %s.", user.first_name, self._chat_ai_service.name)
        await update.message.reply_text("Thank you for chatting with me. Have a nice day!")
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info("User %s canceled the activity.", user.first_name)
        await update.message.reply_text(
            "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

        
    def _set_chat_ai_service(self, service: IChatAIHandler):
        self._chat_ai_service = service
