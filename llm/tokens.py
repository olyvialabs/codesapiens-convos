import re
from math import ceil
from typing import List

import tiktoken
from langchain.docstore.document import Document as LCDocument
from config.open_ai_models import models

min_tokens = 150
max_tokens = 2000


def get_tokens_length(text, encoding_base=models['gpt-3.5-turbo'].encoding_base):
    return len(tiktoken.get_encoding(encoding_base).encode(text))


def group_documents(docs: List[LCDocument]) -> List[LCDocument]:
    temp_docs = []

    for doc in docs:
        chunks = [doc[i:i+1000] for i in range(0, len(doc), 1000)]
        # Iterate through the chunks
        for idx, chunk in enumerate(chunks):
            lc_document = LCDocument(
                page_content=chunk, metadata={"source": "local"})
            temp_docs.append(lc_document)
        # continue
        # print(doc)
        # print('===================')
        # lc_document = LCDocument(
        #     page_content=doc, metadata={"source": "local"})
        # temp_docs.append(lc_document)

    return temp_docs


def group_and_partition_documents(documents: List[LCDocument]):
    print("Grouping small documents")
    temp_docs = []
    try:
        temp_docs = group_documents(docs=documents)
    except Exception:
        print("Grouping failed")

   # print("Separating large documents")
    # try:
    #     documents = split_documents(docs=documents)
    # except Exception:
    #     print("Split failed")
    return temp_docs
