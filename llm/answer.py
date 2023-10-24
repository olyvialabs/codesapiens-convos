import asyncio
from langchain.prompts import PromptTemplate
from config.settings import settings
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain import VectorDBQA, OpenAI
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from persister.supabase import insert_billing_question_processed, get_supabase, insert_chat_message, get_chat_history, MessageType
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings import OpenAIEmbeddings

with open("templates/question_prompt.txt", "r") as f:
    question_prompt = f.read()
with open("templates/chat_combine_prompt.txt", "r") as f:
    chat_combine_template = f.read()


def get_processed_history(chat_id):
    chat_history_data = get_chat_history(chat_id)
    chat_data = chat_history_data.data
    history = []
    if not chat_data:
        return history
    i = 0
    # This is for extreme edge cases
    # For cases where user messages are not followed by assistant messages
    # this shouldn't happend, but let's be safe
    while i < len(chat_data):
        user_message = chat_data[i].get(
            "content") if chat_data[i].get("type") == "user" else None
        assistant_response = None
        # If the current message is from the user, look for the next assistant response
        if user_message:
            i += 1
            while i < len(chat_data) and chat_data[i].get("type") == "user":
                # Collect and concatenate subsequent user messages
                user_message += " " + chat_data[i].get("content")
                i += 1
            # If there's an assistant message after the user message(s)
            if i < len(chat_data) and chat_data[i].get("type") == "assistant":
                assistant_response = chat_data[i].get("content")
        # If there's a valid pairing, append to the history
        if user_message and assistant_response:
            history.append((user_message, assistant_response))
        i += 1

    return history


def generate_prompt_answer(prompt, id_chat='', id_user='', id_project=''):
    openai_embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY)
    supabase_store = SupabaseVectorStore(
        get_supabase(), openai_embeddings, "DocumentEmbeedingChunk", 'match_documents')
    # , 'filter': {'projectId': id_project}
    print('id_project', id_project)
    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.25, model_name="gpt-3.5-turbo-16k"),
        supabase_store.as_retriever(
            search_kwargs={'k': 11}, filter={'projectId': id_project}),
        return_source_documents=True,
        verbose=True,
    )

    history = get_processed_history(id_chat)

    # Insert user's question into Supabase
    user_msg = insert_chat_message(id_user, id_chat, prompt,
                                   MessageType.USER, id_project)

    result = qa(
        {"question": prompt, "chat_history": history})

    # Insert assistant's answer into Supabase
    assistance_msg = insert_chat_message(
        id_user, id_chat, result['answer'], MessageType.ASSISTANT, id_project)
    insert_billing_question_processed(id_user, id_chat, id_project, prompt)
    # Insert billing info
    # insert_billing_question_processed(
    #     user_id=id_user,
    #     project_id=id_project,
    #     question=prompt,
    #     chat_id=id_chat,
    #     tokens=100)

    return {'answer': result['answer'], 'user_message': user_msg, 'assistance_message': assistance_msg, 'sources': []}
