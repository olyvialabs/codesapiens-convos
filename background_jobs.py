from celery import Celery
from celery.result import AsyncResult
from parser.DirectoryIterator import DirectoryIterator

celery = Celery()


def get_process_status(process_id):
    process = AsyncResult(process_id)
    return {"status": process.status, "details": process.info}


def get_metadata_from_filename(title):
    return {'title': title}


# ['.js', '.md', '.ts', '.tsx', '.jsx', ],
@celery.task(bind=True)
def index_project_files(self):
    self.update_state(state='PROGRESS', meta={'current': 1})
    full_path = 'temp/test-code'
    reader_params = {
        'input_dir': full_path,
        'input_files': None,
        'recursive': True,
        'required_exts': ['.md', '.js'],
        'num_files_limit': None,
        'exclude_hidden': True,
        'file_metadata': get_metadata_from_filename
    }
    raw_docs = DirectoryIterator(**reader_params).load_data()
    for doc in raw_docs:
        print(doc.text)

    return {"status": "unknown"}
