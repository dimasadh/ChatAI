import logging
from services.chat_ai.IChatAIService import IChatAIHandler
from openai import OpenAI
from common import GlobalValue
from common.MessageCache import MessageCache

class ChatGPTAIService(IChatAIHandler):
    __client: OpenAI = None
    __model: str = None
    _base_message = [ {"role": "system", "content":  
                    "You are a intelligent assistant."} ] 
    def __init__(self):
        super().__init__()
        self.__client = OpenAI(api_key=GlobalValue.OPEN_AI_API_KEY)
        self.__model = "gpt-3.5-turbo"

    def run(self): 
        user_id = 0
        total_tokens = 0
        if MessageCache.get(user_id) is None:
            MessageCache.set(user_id, self._base_message, 0)
        while True:
            message = input("User : ") 
            if message: 
                current_message = MessageCache.append(user_id, {"role": "user", "content": message}, 0) 
                response = self.__client.chat.completions.create( 
                    model=self.__model, messages=current_message["message"]
                )
            reply = response.choices[0].message.content 
            total_tokens += response.usage.total_tokens
            MessageCache.append(user_id, {"role": "assistant", "content": reply}, response.usage.total_tokens)
            print(f"ChatGPT: {reply}") 
            print(f"Total tokens: {total_tokens}")

    async def get_response(self, user_id: str, message: str) -> str:
        try:
            if MessageCache.get(user_id) is None:
                MessageCache.set(user_id, self._base_message, 0)

            current_message = MessageCache.append(user_id, {"role": "user", "content": message}, 0)
            response = self.__client.chat.completions.create( 
                model=self.__model, messages=current_message["message"], max_tokens=GlobalValue.MAX_TOKEN_PER_MESSAGE
            )
            reply = response.choices[0].message.content
            MessageCache.append(
                user_id=user_id, 
                message={"role": "assistant", "content": reply},
                token_used=response.usage.total_tokens
            )

            return reply
        except Exception as e:
            logging.error(f"Error calling Claude API: {e}")
            return "Sorry, I'm unable to process your request at the moment."