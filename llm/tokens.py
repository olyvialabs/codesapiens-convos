import re
from math import ceil
from typing import List

import tiktoken
from parser.schema.base import Document
from config.open_ai_models import models

min_tokens = 150
max_tokens = 2000


def get_tokens_length(text, encoding_base=models['gpt-3.5-turbo'].encoding_base):
    return len(tiktoken.get_encoding(encoding_base).encode(text))


def group_documents(docs: List[Document]) -> List[Document]:
    temp_docs = []
    current_group = None

    for doc in docs:
        doc_len = get_tokens_length(doc.text)

        if current_group is None:
            print("current_group is None", doc.text)
            current_group = Document(text=doc.text, doc_id=doc.doc_id, embedding=doc.embedding,
                                     extra_info=doc.extra_info)
        elif get_tokens_length(current_group.text) + doc_len < max_tokens and doc_len >= min_tokens:
            print("token lenght", current_group.text + " " + doc.text)
            current_group.text += " " + doc.text
        else:
            print("ELSE", current_group)
            temp_docs.append(current_group)
            current_group = Document(text=doc.text, doc_id=doc.doc_id, embedding=doc.embedding,
                                     extra_info=doc.extra_info)

    if current_group is not None:
        print("final done", current_group)

        temp_docs.append(current_group)

    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    temp_docs = []
    for doc in docs:
        tokens_length = get_tokens_length(doc.text)
        if tokens_length <= max_tokens:
            temp_docs.append(doc)
        else:
            # 5 num_parts = (5000/1000)
            num_parts = ceil(tokens_length / max_tokens)
            # 1000 part_length = (5000/5)
            each_part_length = ceil(len(doc.text) / num_parts)
            # let's say part_length = 1000, then we are going to have 5 parts
            # for a 49450 characters length text
            # [0:999] [1000:1999] [2000:2999] [3000:3999] [4000:4949]
            text_parts = [doc.text[i:i + each_part_length]
                          for i in range(0, len(doc.text), each_part_length)]
            for i, text_part in enumerate(text_parts):
                new_doc = Document(text_part.strip(),
                                   doc_id=f"{doc.doc_id}-{i}",
                                   embedding=doc.embedding,
                                   extra_info=doc.extra_info)
                temp_docs.append(new_doc)
    return temp_docs


def group_and_partition_documents(documents: List[Document]):
    print("Grouping small documents")
    print(documents)
    try:
        documents = group_documents(docs=documents)
    except Exception:
        print("Grouping failed")

    print("Separating large documents")
    # try:
    #     documents = split_documents(docs=documents)
    # except Exception:
    #     print("Split failed")
    return documents
