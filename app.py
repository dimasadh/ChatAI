from services.TelegramBotService import TelegramBotService

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

if __name__ == '__main__':
    main()
    # runClaudePlayground()
    # runChatGPTPlayground()