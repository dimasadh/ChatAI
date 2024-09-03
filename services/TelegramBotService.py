import logging
from telegram import (
    ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CallbackContext, CommandHandler, ConversationHandler, filters, MessageHandler, CallbackQueryHandler
)
from common import GlobalValue
from common.Enums import Activity, ConversationState, Command, AI_MODEL
from services.chat_ai.IChatAIService import IChatAIHandler
from common.MessageCache import MessageCache
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
                ConversationState.CHOOSE_AI_MODEL.value: [
                    CallbackQueryHandler(self.choose_ai_model, pattern='^(chatgpt|claude)$')
                ],
                ConversationState.START_CHAT.value: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_chat),
                    CommandHandler("finish", self.end_conversation)
                ],
            },
            fallbacks=[CommandHandler(Command.CANCEL.value, self.cancel)],
        )
        application.add_handler(conv_handler)

        # Add a handler for the message outside of the conversation
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.welcome_message))
        application.add_handler(CommandHandler("help", self.help_command))

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: CallbackContext):
        keyboard = [
            [InlineKeyboardButton("ChatGPT 🤖", callback_data='chatgpt')],
            [InlineKeyboardButton("Claude 🧠", callback_data='claude')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Welcome to ChatAI Bot! 🤖✨ Your personal AI assistant is here to help.\n\n"
            "Which AI model would you like to chat with?",
            reply_markup=reply_markup
        )
        return ConversationState.CHOOSE_AI_MODEL.value
    
    async def choose_activity(self, update: Update, context: CallbackContext):
        # ! Will be implemented when the new feature are ready
        user = update.effective_user
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
        query = update.callback_query
        await query.answer()
        chosen_model = query.data

        if chosen_ai == AI_MODEL.CHATGPT.value:
            self._chat_ai_service = self._chat_gpt_service
        elif chosen_ai == AI_MODEL.CLAUDE.value:
            self._chat_ai_service = self._claude_service
        else:
            logging.error("Invalid AI model selected.")
            await update.message.reply_text("Invalid AI model selected.")
            return ConversationState.CHOOSE_AI_MODEL.value

        await query.edit_message_text(f"{model_intro}\n\nHow can I assist you today? (Type /finish to end the conversation)")

        return ConversationState.START_CHAT.value
    
    async def handle_chat(self, update: Update, context: CallbackContext):
        user_message = update.message.text
        ai_response = await chat_ai_service.get_response(str(update.effective_user.id), user_message)
        await update.message.reply_text(ai_response)
    
    async def end_conversation(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info("User %s ended the conversation with %s.", user.first_name, self._chat_ai_service.name)
        user = update.effective_user
        await update.message.reply_text("Thank you for chatting with me. Have a great day! 👋")
        MessageCache.remove_message(str(update.effective_user.id))
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: CallbackContext):
        user = update.effective_user
        logging.info("User %s canceled the activity.", user.first_name)
        await update.message.reply_text("Operation cancelled. Type /start to start again.")
        return ConversationHandler.END

    async def help_command(self, update: Update, context: CallbackContext):
        help_text = (
            "Here's how to use ChatAI Bot:\n\n"
            "/start - Start a new conversation\n"
            "/finish - End the current conversation\n"
            "/cancel - Cancel the current operation\n"
            "/help - Show this help message\n\n"
            "Simply type your message to chat with the AI!"
        )
        await update.message.reply_text(help_text)

    async def welcome_message(self, update: Update, context: CallbackContext):
        user = update.effective_user
        logging.info("User %s sent a message outside of a conversation.", user.first_name)
        
    def _set_chat_ai_service(self, service: IChatAIHandler):
        self._chat_ai_service = service
        welcome_text = (
            f"Hello {user.first_name}! 👋 Welcome to ChatAI Bot, your personal AI assistant.\n\n"
            "Here's what I can do for you:\n"
            "🤖 Chat with AI - Engage in intelligent conversations\n"
            "🌐 Translate (coming soon) - Break language barriers\n\n"
            "To get started, just type /start and choose the AI you wanna chat with!\n"
            "Need help? Type /help for more information."
        )
        
        await update.message.reply_text(welcome_text)

