import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config.settings import settings
from retry import retry

output_folder = "outputs"


@retry(tries=10, delay=60)
def store_add_texts_with_retry(store, i):
    store.add_texts([i.page_content], metadatas=[i.metadata])


def embeed_md_files_to_store(docs):
    # create output folder if it doesn't exist
    if not os.path.exists(f"{output_folder}"):
        os.makedirs(f"{output_folder}")

    init_doc_store_files = [docs[0]]
    docs.pop(0)

    store = FAISS.from_documents(init_doc_store_files, OpenAIEmbeddings(
        openai_api_key=settings.OPEN_AI_API_KEY))

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
            store.save_local(f"{output_folder}")
            break
        current_doc_index += 1
    store.save_local(f"{output_folder}")
    # store.add_texts([i.page_content], metadatas=[i.metadata])
