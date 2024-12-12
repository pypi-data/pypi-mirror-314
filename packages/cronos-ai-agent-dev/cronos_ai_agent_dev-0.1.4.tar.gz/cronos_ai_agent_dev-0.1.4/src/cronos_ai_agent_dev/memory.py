import os
import pyairtable
import uuid
import json


class Memory:
    def __init__(self):
        self.airtable_api_key = os.environ.get("AIRTABLE_ASSISTANT_DEMO_NOV2024_API_KEY", "")
        self.airtable_base_id = os.environ.get("AIRTABLE_ASSISTANT_DEMO_NOV2024_BASE_ID", "")
        self.table_name_chats = "chats"
        self.table_name_messages = "messages"
        self.airtable_api = pyairtable.Api(self.airtable_api_key)
        self.table_chats = self.airtable_api.table(self.airtable_base_id, self.table_name_chats)
        self.table_messages = self.airtable_api.table(
            self.airtable_base_id, self.table_name_messages
        )

    def reset_conversation(self, chat_id: int):
        # Create random conversation_id
        conversation_id = str(uuid.uuid4())
        formula = '{chat_id}="' + str(chat_id) + '"'
        found_records = self.table_chats.all(formula=formula)
        if len(found_records) == 0:
            self.table_chats.create(
                {"chat_id": chat_id, "current_conversation_id": conversation_id}
            )
        else:
            record_id = found_records[0]["id"]
            self.table_chats.update(record_id, {"current_conversation_id": conversation_id})

    def log_message(
        self,
        chat_id: int,
        sender_id: int,
        sender_type: str,
        message: str,
        history: list,
    ):
        # Create random message_id
        message_id = str(uuid.uuid4())
        # Check if chat_id exists in table_chats
        formula = '{chat_id}="' + str(chat_id) + '"'
        found_records = self.table_chats.all(formula=formula)
        if len(found_records) == 0:
            # Create a random conversation_id
            conversation_id = str(uuid.uuid4())
            # Create new chat record
            self.table_chats.create(
                {"chat_id": chat_id, "current_conversation_id": conversation_id}
            )
        else:
            conversation_id = found_records[0]["fields"]["current_conversation_id"]
        # Log message in table_messages
        self.table_messages.create(
            {
                "message_id": message_id,
                "chat_id": chat_id,
                "conversation_id": conversation_id,
                "sender_type": sender_type,
                "sender_id": sender_id,
                "message": message,
                "history": json.dumps(history, indent=4),
            }
        )

    def get_chat_history(self, chat_id: int):
        # Get conversation_id
        formula = '{chat_id}="' + str(chat_id) + '"'
        found_records = self.table_chats.all(formula=formula)
        if len(found_records) == 0:
            return []
        conversation_id = found_records[0]["fields"]["current_conversation_id"]
        # Get messages
        formula = '{conversation_id}="' + conversation_id + '"'
        found_records = self.table_messages.all(formula=formula, view="chrono")
        history = []
        for record in found_records:
            history.append(
                {
                    "role": record.get("fields", {}).get("sender_type", ""),
                    "message": record.get("fields", {}).get("message", ""),
                }
            )
        return history

    def format_history_for_cohere(self, history: list):
        chat_history_formatted = []
        for message in history:
            if message["role"] == "User":
                chat_history_formatted.append({"role": "User", "message": message["message"]})
            if message["role"] == "Assistant":
                chat_history_formatted.append({"role": "ChatBot", "message": message["message"]})
            if message["role"] == "System":
                chat_history_formatted.append({"role": "System", "message": message["message"]})
        return chat_history_formatted

    def format_history_for_openai(self, history: list):
        formatted_history = []
        for message in history:
            formatted_history.append({"role": message["role"], "content": message["message"]})
        return formatted_history
