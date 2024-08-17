from abc import ABC, abstractmethod

class IChatAIHandler(ABC):
    name = ""
    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_response') and 
                callable(subclass.get_response) or 
                NotImplemented)

    @abstractmethod
    def get_response(self, user_id: str, message: str) -> str:
        raise NotImplementedError
    
    def say_hi(self, user_name:str) -> str:
        return f"Hi {user_name}, I'm {self.name}. I'm here to listen and have a conversation with you. What do you want to ask?"
    