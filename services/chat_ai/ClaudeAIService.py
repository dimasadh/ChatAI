import anthropic
import logging
from anthropic import Client
from common import GlobalValue
from common.MessageCache import MessageCache
from common.Enums import AI_MODEL
from services.chat_ai.IChatAIService import IChatAIHandler

class ClaudeAIService(IChatAIHandler):
    __client: Client = None
    __model: str = None
    _base_message = [ {"role": "system", "content":  
                    "I'm here to listen and have a conversation with you. What do you want to ask?"} ]

    def __init__(self):
        super().__init__()
        self.name = "Claude"
        self.__client = anthropic.Client(api_key=GlobalValue.ANTHROPIC_API_KEY)
        self.__model = "claude-3-5-sonnet-20240620"

    def run(self):
        """Claude playground using terminal"""
        user_id = 0
        total_tokens = 0
        while True:
            message = input("User : ") 
            if message: 
                current_message = MessageCache.append(user_id, {"role": "user", "content": message}, 0) 
                response = self.__client.messages.create(
                    model=self.__model, messages=current_message["message"], max_tokens=GlobalValue.MAX_TOKEN_PER_MESSAGE,
                )
            reply = response.content[0].text
            current_token_usages = response.usage.input_tokens + response.usage.output_tokens
            total_tokens += current_token_usages
            MessageCache.append(user_id, {"role": "assistant", "content": reply}, current_token_usages)
            print(f"Claude: {reply}") 
            print(f"Total tokens: {MessageCache.get_token_used(user_id)}")

    async def get_response(self, user_id: str, message: str) -> str:
        try:
            current_message = MessageCache.append(user_id, {"role": "user", "content": message}, 0)
            response = self.__client.messages.create(
                model=self.__model, messages=current_message["message"], max_tokens=GlobalValue.MAX_TOKEN_PER_MESSAGE
            )
            reply = response.content[0].text
            current_token_usages = response.usage.input_tokens + response.usage.output_tokens
            MessageCache.append(
                user_id=user_id, 
                message={"role": "assistant", "content": reply}, 
                token_used=current_token_usages
            )

            return reply
        except Exception as e:
            logging.error(f"Error calling Claude API: {e}")
            return "Sorry, there was an error processing your request. Please try again later."
