import anthropic
from anthropic import Client
import logging
from service.IChatAIService import IChatAIHandler
from common import GlobalValue

class ClaudeAIService(IChatAIHandler):
    __client: Client = None
    __model: str = None
    _base_message = [ {"role": "system", "content":  
                    "You are a intelligent assistant."} ] 

    def __init__(self):
        super().__init__()
        self.__client = anthropic.Client(api_key=GlobalValue.ANTHROPIC_API_KEY)
        self.__model = "claude-3-5-sonnet-20240620"

    def run(self):
        while True: 
            messages = self._base_message
            message = input("User : ") 
            if message: 
                messages.append( 
                    {"role": "user", "content": message}, 
                ) 
                chat = self.__client.messages.create(
                    model=self.__model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": message}
                    ]
                )
            reply = chat.content[0].text
            print(f"Claude: {reply}") 
            messages.append({"role": "assistant", "content": reply})

    async def get_response(self, message):
        try:
            message = self.__client.messages.create(
                model=self.__model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": message}
                ]
            )

            return message.content[0].text
        except Exception as e:
            logging.error(f"Error calling Claude API: {e}")
            return "Sorry, there was an error processing your request. Please try again later."