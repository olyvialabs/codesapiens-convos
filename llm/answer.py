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
from langchain.memory import ConversationBufferMemory

with open("templates/question_prompt.txt", "r") as f:
    question_prompt = f.read()
with open("templates/chat_combine_prompt.txt", "r") as f:
    chat_combine_template = f.read()


def get_processed_history(chat_id):
    chat_history_data = get_chat_history(chat_id)
    chat_data = chat_history_data.data
    history = ""
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
            # history.append((user_message, assistant_response))
            # let's cut the texts so it don't overflow.
            # per row will be ~550 * 7 which is the amonut of history from the chat...
            history = history + 'Human:' + \
                user_message[0:250]+'\nAssistant:'+assistant_response[0:300]
        i += 1

    return history


def generate_prompt_answer(prompt, id_chat='', id_user='', id_project='', id_repository='', isOnlyRepositorySearch=False):
    openai_embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY)
    supabase_store = SupabaseVectorStore(
        get_supabase(), openai_embeddings, "DocumentEmbeedingChunk", 'match_documents')
    # memory = ConversationBufferMemory(
    #    memory_key="chat_history", input_key='question', output_key='answer', return_messages=True)
    history = get_processed_history(id_chat)

    combine_docs_prompt_template = """
        You are a codesapiens, friendly and helpful AI assistant by Olyvia Labs that provides help with documents. You give thorough answers with code examples if possible.
        Use the following pieces of context to help answer the users question. If its not relevant to the question, provide friendly responses.
        Return text in the original language of the follow up question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        When using code examples, use the following format:
        ```(language)
        (code)
        ```

        Use the following pieces of chat history and context to answer the question at the end.
        Chat history
        ------------
        """+history.replace('"', '\"')+"""
        Context
        ------------
        {context}

        Question: {question}
        Helpful Answer:
    """

    combine_docs_prompt = PromptTemplate.from_template(
        combine_docs_prompt_template)
    filter = {'projectId': id_project}
    if id_repository and isOnlyRepositorySearch:
        filter = {'repositoryId': id_repository}

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0.25, model_name="gpt-3.5-turbo-16k"),
        retriever=supabase_store.as_retriever(
            search_kwargs={'k': 7, 'filter': filter}),
        return_source_documents=True,
        verbose=True,
        # memory=memory,
        combine_docs_chain_kwargs={"prompt": combine_docs_prompt},
    )
    # Insert user's question into Supabase
    # user_msg = insert_chat_message(id_user, id_chat, prompt,
    #                               MessageType.USER, id_project)

    result = qa(
        {"question": prompt, "chat_history": []})

    # Insert assistant's answer into Supabase
    # assistance_msg = insert_chat_message(
    #    id_user, id_chat, result['answer'], MessageType.ASSISTANT, id_project)
    # insert_billing_question_processed(id_user, id_chat, id_project, prompt)

    return {'answer': result['answer'], 'user_message': prompt, 'assistance_message': result['answer'], 'sources': []}
