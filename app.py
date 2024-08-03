import logging
import anthropic
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

claude_client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a Telegram bot that can interact with the Claude AI. Send me a message, and I'll pass it to Claude.")

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    claude_response = await call_claude_api(user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=claude_response)

async def call_claude_api(message):
    try:
        message = claude_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return message.content[0].text
    except Exception as e:
        logging.error(f"Error calling Claude API: {e}")
        return "Sorry, there was an error processing your request. Please try again later."

def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_API_KEY")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()