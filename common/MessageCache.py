import threading
from common.GlobalValue import MAX_MESSAGE_ARRAY_LENGTH

class MessageCache:
    _dict = {}
    _dict_lock = threading.Lock()

    @classmethod
    def set(cls, user_id, message, token_used):
        with cls._dict_lock:
            cls._dict[user_id] = {"message": message, "token_used": token_used}
            return cls._dict[user_id]

    @classmethod
    def get(cls, user_id, default=None):
        with cls._dict_lock:
            return cls._dict.get(user_id, default)
    
    @classmethod
    def remove(cls, user_id):
        with cls._dict_lock:
            if user_id in cls._dict:
                del cls._dict[user_id]
    
    @classmethod
    def remove_message(cls, user_id):
        with cls._dict_lock:
            if user_id in cls._dict:
                cls._dict[user_id]["message"] = []

    @classmethod
    def append(cls, user_id, message, token_used):
        with cls._dict_lock:
            if user_id in cls._dict:
                messages = cls._dict[user_id]["message"]
                if len(messages) >= MAX_MESSAGE_ARRAY_LENGTH:
                    messages.pop(0)
                messages.append(message)
                cls._dict[user_id]["token_used"] += token_used
            else:
                cls._dict[user_id] = {"message": [message], "token_used": token_used}
            return cls._dict[user_id]

    @classmethod
    def get_message(cls, user_id, default=None):
        with cls._dict_lock:
            return cls._dict.get(user_id, {}).get("message", default)

    @classmethod
    def get_token_used(cls, user_id, default=0):
        with cls._dict_lock:
            return cls._dict.get(user_id, {}).get("token_used", default)
        
    @classmethod
    def get_all(cls):
        with cls._dict_lock:
            return cls._dict