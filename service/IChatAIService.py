from abc import ABC, abstractmethod

class IChatAIHandler(ABC):
    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_response') and 
                callable(subclass.get_response) or 
                NotImplemented)

    @abstractmethod
    def get_response(self, message: str) -> str:
        raise NotImplementedError