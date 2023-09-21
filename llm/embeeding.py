import os
import json
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from config.settings import settings
from retry import retry
import openai


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


def generate_embeed_data_from_file():
    return


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


def embeed_md_files_to_store(docs):
    # create output folder if it doesn't exist
    if not os.path.exists(f"{settings.output_folder}"):
        os.makedirs(f"{settings.output_folder}")

    init_doc_store_files = [docs[0]]
    docs.pop(0)

    store = FAISS.from_documents(init_doc_store_files, OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY))

    # TODO: Move status update to this part instead of the calling for
    current_doc_index = 0
    for current_doc in docs:
        try:
            store_add_texts_with_retry(store, current_doc)
        except Exception as e:
            print(e)
            print("Error on ", current_doc)
            print("Saving progress")
            print(f"stopped at {current_doc_index} out of {len(docs)}")
            store.save_local(f"{settings.output_folder}")
            break
        current_doc_index += 1
    store.save_local(f"{settings.output_folder}")
    # store.add_texts([i.page_content], metadatas=[i.metadata])
