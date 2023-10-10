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
# supabase.auth.sign_in_with_password(
#     {'email': "brandon.aguilar2961@alumnos.udg.mx", 'password': "Tester.123t"})
# supabase.postgrest.auth(token=supabase.auth.get_session().access_token)


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
    # Inserting into billing
    # billing_data = {
    #     "type": BillingType.QUESTION.value,
    #     "userId": user_id,
    #     "projectId": project_id,
    # }
    # supabase.table('Billing').insert(billing_data).execute()
