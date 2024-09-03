from services.TelegramBotService import TelegramBotService
import os

def main():
    telegram_bot_service = TelegramBotService()
    telegram_bot_service.run()

def runChatGPTPlayground():
    from services.chat_ai.ChatGPTAIService import ChatGPTAIService
    chat_gpt_service = ChatGPTAIService()
    chat_gpt_service.run()

def runClaudePlayground():
    from services.chat_ai.ClaudeAIService import ClaudeAIService
    claude_service = ClaudeAIService()
    claude_service.run()

def checkEnv():
    print(os.getenv("TELEGRAM_BOT_API_KEY"))
    print(os.getenv("ANTHROPIC_API_KEY"))
    print(os.getenv("OPEN_AI_API_KEY"))

    from dotenv import load_dotenv
    load_dotenv()

    print(os.getenv("TELEGRAM_BOT_API_KEY"))
    print(os.getenv("ANTHROPIC_API_KEY"))
    print(os.getenv("OPEN_AI_API_KEY"))

if __name__ == '__main__':
    checkEnv()
    main()
    # runClaudePlayground()
    # runChatGPTPlayground()