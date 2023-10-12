from supabase import create_client, Client
from config.settings import settings
from enum import Enum
import cuid


class BillingType(Enum):
    QUESTION = "question"
    FILE_PROCESSED = "file_processed"


class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"


url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY
supabase: Client = create_client(url, key)


def get_chat_history(id_chat: str):
    return supabase.table('ChatHistory').select('*').eq('chatId', id_chat).order('created_at', desc=False).execute()


def get_chat(id_chat: str):
    return supabase.table('Chat').select('*').eq('id', id_chat).execute()


def insert_chat_message(user_id: str, chat_id: str, content: str, message_type: MessageType, project_id: str):
    unique_id = cuid.cuid()
    # Inserting into chat_history
    chat_history_data = {
        "id": unique_id,
        "userId": user_id,
        "chatId": chat_id,
        "content": content,
        "type": message_type.value,
    }
    supabase.table('ChatHistory').insert(chat_history_data).execute()

    return {'id': unique_id, 'chat_id': chat_id}


def insert_billing_file_processed(user_id: str, project_id: str, document_id: str, extra_data: str):
    unique_id = cuid.cuid()
    billing_file_data = {
        "id": cuid.cuid(),
        "userId": user_id,
        "projectId": project_id,
        "documentId": document_id,
        "metadata": None  # message_type.value,
    }
    supabase.table('BillingFile').insert(billing_file_data).execute()
    return {'id': unique_id}


def insert_billing_question_processed(user_id: str, project_id: str, question: str, chat_id: str, tokens: int):
    unique_id = cuid.cuid()
    billing_question_data = {
        "id": cuid.cuid(),
        # "userId": user_id,
        "projectId": project_id,
        "chatId": chat_id,
        "question": question,
        "tokens_used": tokens,
    }
    supabase.table('BillingQuestions').insert(billing_question_data).execute()
    return {'id': unique_id}
