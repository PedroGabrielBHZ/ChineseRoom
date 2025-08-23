from datetime import datetime
from typing import List, Dict
import uuid
from chineseroom.gemini_client import GeminiClient


class Message:
    def __init__(self, role: str, content: str):
        self.role = role  # 'user', 'assistant', or 'system'
        self.content = content
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"[{self.timestamp}] {self.role}: {self.content}"


class Conversation:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Unique identifier for the conversation
        self.messages: List[Message] = []

    def add_message(self, role: str, content: str):
        message = Message(role, content)
        self.messages.append(message)

    def get_history(self) -> List[Message]:
        return self.messages


class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.client = GeminiClient()

    def start_conversation(self) -> str:
        conversation = Conversation()
        self.conversations[conversation.id] = conversation
        return conversation.id

    def add_message(self, conversation_id: str, role: str, content: str):
        if conversation_id not in self.conversations:
            raise ValueError("Conversation ID not found.")
        self.conversations[conversation_id].add_message(role, content)

    def get_conversation(self, conversation_id: str) -> Conversation:
        if conversation_id not in self.conversations:
            raise ValueError("Conversation ID not found.")
        return self.conversations[conversation_id]

    def reset_conversation(self, conversation_id: str):
        if conversation_id in self.conversations:
            self.conversations[conversation_id] = Conversation()

    def interact(self, conversation_id: str, user_input: str) -> str:
        if conversation_id not in self.conversations:
            raise ValueError("Conversation ID not found.")

        # Add user input to the conversation
        self.add_message(conversation_id, "user", user_input)

        # Get response from GeminiClient
        try:
            response = self.client.ask(user_input)
            self.add_message(conversation_id, "assistant", response)
            return response
        except Exception as e:
            error_message = f"Error: {e}"
            self.add_message(conversation_id, "system", error_message)
            return error_message
