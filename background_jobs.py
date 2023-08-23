from celery import Celery
from celery.result import AsyncResult
from parser.schema.base import Document
from parser.code.base import transform_to_docs
from parser.code.javascript import extract_functions_and_classes
from parser.DirectoryIterator import DirectoryIterator
from celery.utils.log import get_task_logger
from llm.embeeding import embeed_md_files_to_store
from llm.tokens import group_and_partition_documents
logger = get_task_logger(__name__)

celery = Celery()
celery.config_from_object("config.celery_config")


def get_process_status(process_id):
    print(process_id)
    process = AsyncResult(process_id)
    return {"status": process.status, "details": process.info}


def get_metadata_from_filename(title):
    return {'title': title}


# ['.js', '.md', '.ts', '.tsx', '.jsx', ],
@celery.task(bind=True)
def index_project_files(self):
    print(celery.autodiscover_tasks())
    self.update_state(state='STARTING')
    full_path = './temp/test-code'
    reader_params = {
        'input_dir': full_path,
        'input_files': None,
        'recursive': True,
        'required_exts': ['.js'],
        'num_files_limit': None,
        'exclude_hidden': True,
        'file_metadata': get_metadata_from_filename
    }

    result = extract_functions_and_classes(
        './temp/test-code')
    print(result)
    transform_to_docs(result[0], result[1], './temp/test-code')
    return
    raw_docs = DirectoryIterator(**reader_params).load_data()
    self.update_state(state='PROGRESS')
    # raw_docs = group_and_partition_documents(documents=raw_docs)
    # parsed_docs = [Document.to_langchain_format(
    #    raw_doc) for raw_doc in raw_docs]
    # embeed_md_files_to_store(docs=parsed_docs)

    self.update_state(state='FINISHED')

    return {"status": "FINISHED"}
