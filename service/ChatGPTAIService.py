from service.IChatAIService import IChatAIHandler
from openai import OpenAI
from common import GlobalValue

class ChatGPTAIService(IChatAIHandler):
    _client = None
    _base_message = [ {"role": "system", "content":  
                    "You are a intelligent assistant."} ] 
    def __init__(self):
        super().__init__()
        self._client = OpenAI(api_key=GlobalValue.OPEN_AI_API_KEY)

    def run(self): 
        while True: 
            messages = self._base_message
            message = input("User : ") 
            if message: 
                messages.append( 
                    {"role": "user", "content": message}, 
                ) 
                chat = self._client.chat.completions.create( 
                    model="gpt-3.5-turbo", messages=messages 
                ) 
            reply = chat.choices[0].message.content 
            print(f"ChatGPT: {reply}") 
            messages.append({"role": "assistant", "content": reply})

    async def get_response(self, message):
        self._base_message.append({"role": "user", "content": message})
        chat = self._client.chat.completions.create( 
            model="gpt-3.5-turbo", messages=self._base_message 
        )
        reply = chat.choices[0].message.content
        self._base_message.append({"role": "assistant", "content": reply})
        return reply