from supabase import create_client, Client
from config.settings import settings
from enum import Enum
import cuid
from datetime import datetime


class BillingType(Enum):
    QUESTION = "question"
    FILE_PROCESSED = "file_processed"


class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"


def get_supabase():
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY
    supabase: Client = create_client(url, key)
    return supabase


def update_github_document_data(id, data, content):
    supabase = get_supabase()
    data['content'] = content
    print('some reason', id, data)
    return supabase.table('Document').update(data).eq('id', id).execute()


def create_normal_document(data, content):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    data['id'] = unique_id
    data['content'] = content
    return supabase.table('Document').insert(data).execute()


def create_document_folder(folder_path: str, folder_name: str, repository_id: str, project_id: str, parentId: None):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    return supabase.table('Document').insert({
        'id': unique_id,
        'pathName': folder_name,
        'path': folder_path or "/",
        'repositoryId': repository_id,
        'isFolder': True,
        'synced': True,
        'projectId': project_id,
        'title': folder_name,
        "status": 'active',
        'parentId': parentId
    }).execute()


def get_document_by_pathname(pathname: str, path: str, repository_id: str):
    supabase = get_supabase()
    return supabase.table('Document').select('*').eq('pathName', pathname).eq('path', path).eq('repositoryId', repository_id).execute()


def get_folder_exists(path: str, repository_id: str):
    supabase = get_supabase()
    return supabase.table('Document').select('*').eq('path', path).eq('repositoryId', repository_id).execute()


def get_unsynced_repository_docs(repository_id: str):
    supabase = get_supabase()
    return supabase.table('Document').select('*').eq('repositoryId', repository_id).eq('synced', False).execute()


def get_user(user_id: str):
    supabase = get_supabase()
    return supabase.table('User').select('*').eq('id', user_id).execute()


def get_vector_similarity_search(query_embedding: list, id_project: str):
    supabase = get_supabase()
    # Create a filter based on the projectId
    filter_data = {"projectId": id_project}

    # Pass the query_embedding and filter_data as arguments to the RPC function
    params = {"query_embedding": query_embedding, "filter": filter_data}
    return supabase.rpc('match_documents', params).execute()


def update_document_embeeding(document_id: str):
    supabase = get_supabase()
    return supabase.table('Document')\
                   .update({'synced': True})\
                   .eq('id', document_id)\
                   .execute()


def get_chat_history(id_chat: str):
    supabase = get_supabase()
    return supabase.table('ChatHistory').select('*').eq('chatId', id_chat).order('created_at', desc=False).execute()


def get_chat(id_chat: str):
    supabase = get_supabase()
    return supabase.table('Chat').select('*').eq('id', id_chat).execute()


def insert_chat_message(user_id: str, chat_id: str, content: str, message_type: MessageType, project_id: str):
    supabase = get_supabase()
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


def insert_repo_sync(repository_id: str = '', project_id: str = ''):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    # Inserting into chat_history
    repo_sync_data = {
        "id": unique_id,
        "repositoryId": repository_id,
        "projectId": project_id,
    }
    supabase.table('RepositorySync').insert(repo_sync_data).execute()

    return {'id': unique_id}


def update_repo_sync_finished(repository_sync_id: str, logs: str):
    supabase = get_supabase()
    # Current date and time
    current_datetime = datetime.now()

    # Data to be updated
    repo_sync_update_data = {
        "logs": logs,
        "finished_at": current_datetime
    }

    # Updating RepositorySync based on ID
    result = supabase.table('RepositorySync').update(
        repo_sync_update_data).eq('id', repository_sync_id).execute()

    return result


def insert_process(project_id: str, repository_id: str, start_date: str, end_date: str = None, logs: str = None):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    process_data = {
        "id": unique_id,
        "startDate": start_date,
        "endDate": end_date,
        "logs": logs,
        "repositoryId": repository_id,
        "projectId": project_id,
    }
    supabase.table('Process').insert(process_data).execute()
    return {'id': unique_id}


def update_process_end_date_and_logs(process_id: str, logs: str):
    supabase = get_supabase()
    end_date = datetime.now().isoformat()

    updated_data = {
        "endDate": end_date,
        "logs": logs
    }

    supabase.table('Process').update(
        updated_data).eq('id', process_id).execute()


def insert_billing_file_processed(user_id: str, project_id: str, document_id: str, process_id: str):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    billing_file_data = {
        "id": cuid.cuid(),
        "userId": user_id,
        "projectId": project_id,
        "documentId": document_id,
        "metadata": None,
        "processId": process_id,
    }
    supabase.table('BillingFile').insert(billing_file_data).execute()
    return {'id': unique_id}


def insert_billing_question_processed(user_id: str, chat_id: str, project_id: str, question: str):
    supabase = get_supabase()
    unique_id = cuid.cuid()
    billing_question_data = {
        "id": cuid.cuid(),
        "userId": user_id,
        "projectId": project_id,
        "chatId": chat_id,
        "question": question,
    }
    supabase.table('BillingQuestions').insert(billing_question_data).execute()
    return {'id': unique_id}


def get_repository_by_id(repository_id: str):
    supabase = get_supabase()
    return supabase.table('Repository').select('*').eq('id', repository_id).execute()
