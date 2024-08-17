from enum import Enum

class Activity(Enum):
    CHAT = "Chat"

class ConversationState(Enum):
    CHOOSE_ACTIVITY = 0
    CHOOSE_AI_MODEL = 1
    START_CHAT = 2

class Command(Enum):
    START = "start"
    END = "end"
    HELP = "help"
    CANCEL = "cancel"

class AI_MODEL(Enum):
    CHATGPT = "ChatGPT"
    CLAUDE = "Claude"