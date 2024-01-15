import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config.settings import settings
from retry import retry
from persister.supabase import get_supabase, insert_billing_file_processed, update_document_embeeding, get_document_by_pathname, create_document_folder, update_github_document_data, create_normal_document, get_folder_exists
from langchain.vectorstores import SupabaseVectorStore
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document

with open("templates/chat_combine_prompt.txt", "r") as f:
    chat_combine_template = f.read()

gpt_model = "gpt-3.5-turbo"


@retry(tries=10, delay=60)
def store_add_texts_with_retry(store, i):
    store.add_texts([i.page_content])  # , metadatas=[i.metadata]


def get_vector_doc_store(vectorstore):
    openai_embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY)
    docsearch = FAISS.load_local("outputs", openai_embeddings)  # vectorstore
    return docsearch


def get_stream_answer(question, docsearch, chat_history, conversation_id):
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)
    docs = docsearch.similarity_search(question)  # , k=2)
    # join all page_content together with a newline
    docs_together = "\n".join([doc.page_content for doc in docs])
    p_chat_combine = chat_combine_template.replace(
        "{summaries}", docs_together)
    messages_combine = [{"role": "system", "content": p_chat_combine}]
    source_log_docs = []
    for doc in docs:
        if doc.metadata:
            data = json.dumps(
                {"type": "source", "doc": doc.page_content, "metadata": doc.metadata})
            source_log_docs.append(
                {"title": doc.metadata['title'].split('/')[-1], "text": doc.page_content})
        else:
            data = json.dumps({"type": "source", "doc": doc.page_content})
            source_log_docs.append(
                {"title": doc.page_content, "text": doc.page_content})
        yield f"data:{data}\n\n"

    if len(chat_history) > 1:
        tokens_current_history = 0
        # count tokens in history
        chat_history.reverse()
        for i in chat_history:
            if "prompt" in i and "response" in i:
                tokens_batch = llm.get_num_tokens(
                    i["prompt"]) + llm.get_num_tokens(i["response"])
                if tokens_current_history + tokens_batch < settings.TOKENS_MAX_HISTORY:
                    tokens_current_history += tokens_batch
                    messages_combine.append(
                        {"role": "user", "content": i["prompt"]})
                    messages_combine.append(
                        {"role": "system", "content": i["response"]})
    messages_combine.append({"role": "user", "content": question})
    completion = openai.ChatCompletion.create(model=gpt_model, engine=settings.AZURE_DEPLOYMENT_NAME,
                                              messages=messages_combine, stream=True, max_tokens=500, temperature=0)
    reponse_full = ""
    for line in completion:
        if "content" in line["choices"][0]["delta"]:
            # check if the delta contains content
            data = json.dumps(
                {"answer": str(line["choices"][0]["delta"]["content"])})
            reponse_full += str(line["choices"][0]["delta"]["content"])
            yield f"data: {data}\n\n"
    # save conversation to database
    if conversation_id is not None and False:
        conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$push": {"queries": {"prompt": question,
                                   "response": reponse_full, "sources": source_log_docs}}},
        )
    else:
        # create new conversation
        # generate summary
        messages_summary = [{"role": "assistant", "content": "Summarise following conversation in no more than 3 "
                                                             "words, respond ONLY with the summary, use the same "
                                                             "language as the system \n\nUser: " + question + "\n\n" +
                                                             "AI: " +
                                                             reponse_full},
                            {"role": "user", "content": "Summarise following conversation in no more than 3 words, "
                                                        "respond ONLY with the summary, use the same language as the "
                                                        "system"}]
        completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', engine=settings.AZURE_DEPLOYMENT_NAME,
                                                  messages=messages_summary, max_tokens=30, temperature=0)
        # conversation_id = conversations_collection.insert_one(
        #    {"user": "local",
        #     "date": datetime.datetime.utcnow(),
        #     "name": completion["choices"][0]["message"]["content"],
        #     "queries": [{"prompt": question, "response": reponse_full, "sources": source_log_docs}]}
        # ).inserted_id

    # send data.type = "end" to indicate that the stream has ended as json
    # data = json.dumps({"type": "id", "id": str(conversation_id)})
    yield f"data: {completion}\n\n"
    data = json.dumps({"type": "end"})
    yield f"data: {completion}\n\n"


def get_relative_path(absolute_path, base_path):
    """Convert an absolute path to a relative path based on the given base path."""
    if absolute_path.startswith(base_path):
        relative_path = absolute_path[len(base_path):].lstrip("/")
        return "/" + relative_path
    return absolute_path


def get_folder_parent_id_from_path(folder_path: str, repository_id: str, project_id: str):
    values = split_path(folder_path)
    return ensure_folder_exists(values.get('directory'), repository_id, None, project_id)


created_to_pick = {}


def ensure_folder_exists(folder_path, repository_id, project_name, project_id):
    print('[FOLDER] tried', folder_path)
    if folder_path == '/':
        return
    values = split_path(folder_path)
    document = get_document_by_pathname(
        values.get('directory'), values.get('filename'), repository_id)
    if folder_path in created_to_pick:
        separator = ''
        if values.get('directory') != '/':
            separator = '/'
        return created_to_pick[values.get('directory') + separator+values.get('filename')]
    elif not (len(document.data) > 0):
        parent_id = None
        if values.get('directory') != '/':
            parent_id = get_folder_parent_id_from_path(
                folder_path, repository_id, project_id)
        new_doc = create_document_folder(
            values.get('directory'), values.get('filename'), repository_id, project_id, parent_id)
        created_to_pick[values.get('directory')] = parent_id
        created_to_pick[folder_path] = new_doc.data[0]['id']
        return new_doc.data[0]['id']
    # elif values.get('directory') in created_to_pick:
    #     return created_to_pick[values.get('directory')]
    elif document and document.data:
        created_to_pick[folder_path] = new_doc.data[0]['id']
        return document.data[0]['id']
    return None


def get_content_of_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def insert_or_update_document(document_data: dict, repository_id: str, project_name: str):
    # Ensure the folder for this file exists
    ensure_folder_exists(
        document_data['path'], document_data['repositoryId'], project_name, document_data['projectId'])
    document = get_document_by_pathname(
        document_data['pathName'], document_data['path'], repository_id)
    print(document)
    outputs_absolute_dir = os.path.join(os.getcwd(), settings.output_folder)
    project_absolute_dir = os.path.join(outputs_absolute_dir, project_name)
    if document and document.data:  # If document exists
        # Update the document
        file_to_embeed = project_absolute_dir + '/' + \
            document_data['path']+'/'+document_data['pathName']
        file_to_embeed_content = get_content_of_file(
            file_to_embeed)
        print('here?')
        updated_document = update_github_document_data(
            document.data[0]['id'], document_data, file_to_embeed_content)
        print('herev2?')
        metadata = {
            'projectId': document.data[0]['projectId'],
            'repositoryId': repository_id,
            'documentId': document.data[0]['id'],
            'title': document.data[0]['title'],
            'path': document_data['path']+'/'+document_data['pathName']
        }
        print('herev3?')
        slit_text_to_embeeding(file_to_embeed_content, metadata)
        print('herev4?')
        return updated_document
    else:
        file_to_embeed = project_absolute_dir + '/' + \
            document_data['path']+'/'+document_data['pathName']
        file_to_embeed_content = get_content_of_file(
            file_to_embeed)

        print('herev5?')
        new_document = create_normal_document(
            document_data, file_to_embeed_content)
        print('herev6?')
        metadata = {
            'projectId': new_document.data[0]['projectId'],
            'repositoryId': repository_id,
            'documentId': new_document.data[0]['id'],
            'title': new_document.data[0]['title'],
            'path':  document_data['path']+'/'+document_data['pathName']
        }
        print('herev7?')
        slit_text_to_embeeding(file_to_embeed_content, metadata)
        print('herev8?')
        return new_document


def split_path(input_path):
    """
    Splits the given input path into directory and filename.

    Args:
    - input_path (str): The input path to split.

    Returns:
    - dict: Dictionary containing 'directory' and 'filename' keys.
    """
    directory, filename = os.path.split(input_path)

    # Add a leading slash to the directory if not present
    if not directory.startswith("/"):
        directory = "/" + directory

    return {
        "directory": directory,
        "filename": filename
    }


curr_being_processed = {}


def embeed_github_files_to_store(repository, project_name, user_id, process_id, id_project):
    outputs_absolute_dir = os.path.join(os.getcwd(), settings.output_folder)
    project_absolute_dir = os.path.join(outputs_absolute_dir, project_name)
    for root, dirs, files in os.walk(project_absolute_dir, topdown=False):
        for filename in files:
            print(filename)
            file_path = os.path.join(root, filename).replace(
                project_absolute_dir, "").lstrip("/")
            print(file_path)
            print(file_path)
            print(file_path)
            print(file_path)
            print('the path?', os.path.dirname(file_path) or '/')
            split_data = split_path(file_path)
            print('We are talking about [] => ', filename)
            doc_data = {
                'title': filename,
                'pathName': split_data.get('filename'),
                'path': split_data.get('directory') or "/",
                'repositoryId': repository['id'],
                'projectId': id_project,
                'synced': True,
                'parentId': ensure_folder_exists(split_data.get('directory'), repository['id'], None, id_project),
                "status": 'active',
            }

            doc = insert_or_update_document(
                doc_data, repository['id'], project_name)
            print('wtf passed here', doc)
            insert_billing_file_processed(
                user_id, id_project, doc.data[0]['id'],  process_id)

    return


# It's important to overlap the text so it doesn't just start from the position it got cut
def chunk_text(text, chunk_length, overlap=500):
    if len(text) <= chunk_length:
        # Return the entire text as a single chunk if it's shorter than the chunk length
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_length
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def convert_to_text_to_docs(text, metadata):
    # Cutting strings of 2500 piece, with 500 chars overlap
    pieces = chunk_text(text, 2500, 500)
    return [Document(page_content=piece, metadata=metadata) for piece in pieces]


def slit_text_to_embeeding(text, metadata):
    docs = convert_to_text_to_docs(text, metadata)
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    try:
        # sometimes says error but it's correct
        SupabaseVectorStore(
            get_supabase(), embeddings, "DocumentEmbeedingChunk").add_documents(docs)
    except Exception as e:
        print('Error', e)


def embeed_md_files_to_store(project_id, repository_id, docs, files_map, user_id, process_id):
    current_doc_index = 0
    total_docs = len(docs)
    print(f"Total documents to process: {total_docs}")
    for current_doc in docs:
        try:
            doc_path = current_doc['path']
            id = files_map['/'+doc_path]
            print(f'Value: {doc_path} - ID: {id}')
            document_id = id
            print(
                f"Processing document {current_doc_index}/{total_docs}: {doc_path}")
            if not document_id:
                raise ValueError(
                    f"No document ID found for path: {doc_path}")
            # Assuming 'get_embedding' is a method to retrieve the embedding

            doc = update_document_embeeding(document_id)
            insert_billing_file_processed(
                user_id, project_id, document_id,  process_id)
            metadata = {
                'projectId': doc.data[0]['projectId'],
                'repositoryId': repository_id,
                'documentId': doc.data[0]['id'],
                'title': doc.data[0]['title'],
                'path': doc_path
            }
            slit_text_to_embeeding(
                current_doc['content'], metadata)
        except Exception as e:
            print(
                f"Error processing document {current_doc_index}/{total_docs}: {e}")
        current_doc_index += 1
