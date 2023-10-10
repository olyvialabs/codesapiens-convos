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
from persister.supabase import insert_chat_message, get_chat_history, MessageType

with open("templates/question_prompt.txt", "r") as f:
    question_prompt = f.read()
with open("templates/chat_combine_prompt.txt", "r") as f:
    chat_combine_template = f.read()


async def async_generate(chain, question, chat_history):
    result = await chain.arun({"question": question, "chat_history": chat_history})
    return result


def run_async_chain(chain, question, chat_history):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = {}
    try:
        answer = loop.run_until_complete(
            async_generate(chain, question, chat_history))
    finally:
        loop.close()
    result["answer"] = answer
    print(result)
    return result


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


def generate_prompt_answer_v2(prompt, vector_store, id_chat='', id_user='', id_project=''):
    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.15, model_name="gpt-3.5-turbo"),
        vector_store.as_retriever(search_kwargs={'k': 6}),
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

    return {'answer': result['answer'], 'user_message': user_msg, 'assistance_message': assistance_msg, 'sources': []}


def generate_prompt_answer(prompt, vector_store, history):
    # Preparing data
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,
                     model_name=settings.OPENAI_MODEL)
    messages_combine = [
        SystemMessagePromptTemplate.from_template(chat_combine_template)]
    question = prompt
    messages_combine.append(
        HumanMessagePromptTemplate.from_template("{question}"))
    print(messages_combine[1].json())
    print(messages_combine)
    """
    if history:
        tokens_current_history = 0
        # count tokens in history
        history.reverse()
        for i in history:
            if "prompt" in i and "response" in i:
                tokens_batch = llm.get_num_tokens(i["prompt"]) + llm.get_num_tokens(i["response"])
                if tokens_current_history + tokens_batch < settings.TOKENS_MAX_HISTORY:
                    tokens_current_history += tokens_batch
                    messages_combine.append(HumanMessagePromptTemplate.from_template(i["prompt"]))
                    messages_combine.append(AIMessagePromptTemplate.from_template(i["response"]))
    messages_combine.append(HumanMessagePromptTemplate.from_template("{question}"))
    """

    p_chat_combine = ChatPromptTemplate.from_messages(messages_combine)
    # Processing
    # CONDENSE_QUESTION_PROMPT)
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    # print(question_generator)

    doc_chain = load_qa_chain(
        llm, chain_type="map_reduce", combine_prompt=p_chat_combine)
    chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(k=2),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        verbose=True
    )
    print("QUESTION", prompt)
    # print(chain)
    chat_history = []
    # result = chain({"question": question, "chat_history": chat_history})
    # generate async with async generate method

    # result = run_async_chain(chain, prompt, chat_history)
    # return result["result"]  # "test"

    # Parsing result
    """if "result" in result:
        result["answer"] = result["result"]
    result["answer"] = result["answer"].replace("\\n", "\n")
    try:
        result["answer"] = result["answer"].split("SOURCES:")[0]
    except Exception:
        pass"""

    sources = vector_store.similarity_search(prompt, k=2)
    sources_doc = []
    for doc in sources:
        sources_doc.append(
            {'title': doc.page_content, 'text': doc.page_content})
        """if doc.metadata:
            sources_doc.append(
                {'title': doc.metadata['title'], 'text': doc.page_content})
        else:
            sources_doc.append(
                {'title': doc.page_content, 'text': doc.page_content})"""
    return sources_doc
    result['sources'] = sources_doc
    # TODO: Insert data to db
    return result


def deprecated_generate_prompt_answer(prompt, vector_store, history):
    # Preparing data
    """llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,
                     model_name=settings.OPENAI_MODEL)"""
    llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0)
    """messages_combine = [
        SystemMessagePromptTemplate.from_template(chat_combine_template)]
    print(messages_combine)"""
    """
    if history:
        tokens_current_history = 0
        # count tokens in history
        history.reverse()
        for i in history:
            if "prompt" in i and "response" in i:
                tokens_batch = llm.get_num_tokens(i["prompt"]) + llm.get_num_tokens(i["response"])
                if tokens_current_history + tokens_batch < settings.TOKENS_MAX_HISTORY:
                    tokens_current_history += tokens_batch
                    messages_combine.append(HumanMessagePromptTemplate.from_template(i["prompt"]))
                    messages_combine.append(AIMessagePromptTemplate.from_template(i["response"]))
    messages_combine.append(HumanMessagePromptTemplate.from_template("{question}"))
    """
    # p_chat_combine = ChatPromptTemplate.from_messages(messages_combine)
    # print(p_chat_combine)
    # Processing
    # question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    # print(question_generator)
    # doc_chain = load_qa_chain(
    #    llm, chain_type="map_reduce", combine_prompt=p_chat_combine)
    """chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(k=2),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
    )"""
    print("QUESTION", prompt)
    q_prompt = PromptTemplate(
        input_variables=["context", "question"], template=question_prompt, template_format="jinja2"
    )
    print('after')
    """chat_combine_template2 = PromptTemplate(
        input_variables=["summaries"], template=chat_combine_template, template_format="jinja2"
    )"""
    chat_combine_template2 = PromptTemplate(
        input_variables=["summaries"], template=chat_combine_template, template_format="jinja2"
    )
    qa_chain = load_qa_chain(
        llm=llm, chain_type="map_reduce", combine_prompt=chat_combine_template2, question_prompt=q_prompt
    )
    print('after2')
    chain = VectorDBQA(combine_documents_chain=qa_chain,
                       vectorstore=vector_store, k=3)
    print('after3')
    # chain_prompt = PromptTemplate(template=prompt)
    # print(prompt, chain_prompt)
    result = chain({"query": prompt})
    print(result)
    return
    # print(chain)
    chat_history = []
    # result = chain({"question": question, "chat_history": chat_history})
    # generate async with async generate method
    result = run_async_chain(chain, prompt, chat_history)
    return "test"

    # Parsing result
    if "result" in result:
        result["answer"] = result["result"]
    result["answer"] = result["answer"].replace("\\n", "\n")
    try:
        result["answer"] = result["answer"].split("SOURCES:")[0]
    except Exception:
        pass

    sources = vector_store.similarity_search(prompt, k=2)
    sources_doc = []
    for doc in sources:
        if doc.metadata:
            sources_doc.append(
                {'title': doc.metadata['title'], 'text': doc.page_content})
        else:
            sources_doc.append(
                {'title': doc.page_content, 'text': doc.page_content})
    result['sources'] = sources_doc
    # TODO: Insert data to db
    return result
