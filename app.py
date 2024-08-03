from service.TelegramBotService import TelegramBotService

def main():
    telegram_bot_service = TelegramBotService()
    telegram_bot_service.run()

def runClaudePlayground():
    from service.ClaudeAIService import ClaudeAIService
    claude_service = ClaudeAIService()
    claude_service.run()

if __name__ == '__main__':
    main()
    # runClaudePlayground()
