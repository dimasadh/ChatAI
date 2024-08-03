from service.TelegramBotService import TelegramBotService

def main():
    telegram_bot_service = TelegramBotService()
    telegram_bot_service.run()

if __name__ == '__main__':
    main()