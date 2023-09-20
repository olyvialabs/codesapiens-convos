from flask import Flask, request, Response
from background_jobs import index_project_files, get_process_status
from llm.embeeding import get_vector_doc_store, get_stream_answer
from llm.answer import generate_prompt_answer
from parser.file.ProjectStructure import ProjectStructure
from parser.file.FolderStructure import FolderStructure
from parser.code.ParseCode import generate_root_config_files, generate_documentation_to_all_inner_folders
from llm.open_ai import get_gpt_response_from_template
from config.settings import settings
import os
import json

app = Flask(__name__)


@app.route("/")
def home():
    return {"status": "hey, what are you doing here?"}


@app.route("/api/process_status", methods=["GET"])
def process_status():
    process_id = request.args.get("process_id")
    if not process_id:
        return {"status": "wrong input", "details": "no process_id provided"}
    return get_process_status(process_id)


@app.route("/api/stream", methods=["POST"])
def stream():
    data = request.get_json()
    # get parameter from url question
    prompt = data["prompt"]
    # history = data["history"]
    # if history:
    #    history = []
    # history = json.loads(history)
    doc_store = get_vector_doc_store("outputs")
    return Response(
        get_stream_answer(prompt, doc_store,
                          chat_history=[],  # history,
                          conversation_id=""), mimetype="text/event-stream")


@app.route("/api/test", methods=["GET"])
def test():
    project_name = '0xpasho|codesapiens'
    temp_folder = 'temp'  # ,./outputs'
    project = ProjectStructure(target_path=temp_folder+'/'+project_name)

    project_full_path = os.getcwd() + '/' + temp_folder + '/' + project_name
    project_main_folder = FolderStructure(project_full_path)

    list_of_files_concatenated = ''
    for file_structure in project_main_folder.files:
        list_of_files_concatenated += file_structure.path + '\n'
    config_list = get_gpt_response_from_template(
        data={'app_name': project_name, 'trimmable_content': list_of_files_concatenated}, template='what_are_these_config_files', trim_content=True)
    config_list = json.loads(config_list)
    print(config_list)
    generate_root_config_files(
        config_list=config_list, project_name=project_name)
    generate_documentation_to_all_inner_folders(project)

    return 'test'


@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.get_json()
    prompt = data["prompt"]
    # history = data["history"]
    # if history:
    #    history = []
    # history = json.loads(history)
    doc_store = get_vector_doc_store(settings.output_folder)
    return generate_prompt_answer(prompt=prompt, vector_store=doc_store, history=[])


@app.route("/api/process_project_files", methods=["POST"])
def process_uploaded_files():
    queue_item = index_project_files.delay()
    process_status = get_process_status(queue_item.id)
    print(process_status)
    return {"status": "STARTED", "process_id": queue_item.id}
