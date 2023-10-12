from flask import Flask, request, Response, jsonify
from background_jobs import index_project_files, get_process_status
from llm.embeeding import get_vector_doc_store, get_stream_answer
from llm.answer import generate_prompt_answer
from parser.file.ProjectStructure import ProjectStructure
from parser.file.FolderStructure import FolderStructure
from parser.code.ParseCode import generate_root_config_files, generate_documentation_for_project_per_file, generate_documentation_for_project_per_folder
from llm.open_ai import get_gpt_response_from_template
from config.settings import settings
import json
from llm.embeeding import embeed_md_files_to_store
from llm.tokens import group_and_partition_documents
from persister.supabase import get_chat_history, get_chat

app = Flask(__name__)


@app.route("/")
def home():
    return {"status": "hey, wtf you doing here?"}


@app.route("/api/process_status", methods=["GET"])
def process_status():
    process_id = request.args.get("process_id")
    if not process_id:
        return {"status": "wrong input", "details": "no process_id provided"}
    return get_process_status(process_id)


@app.route("/api/test", methods=["GET"])
def test():
    project_name = '0xpasho|codesapiens'
    output_project_for_indexing = ProjectStructure(
        target_path=settings.output_folder+'/'+project_name)
    raw_docs = []
    all_files = output_project_for_indexing.get_all_files()
    for file in all_files:
        raw_docs.append(file.get_content(file.path))
    raw_docs_v2 = group_and_partition_documents(documents=raw_docs)
    embeed_md_files_to_store(docs=raw_docs_v2)
    return 'test finished'
    # Prepare
    project_name = '0xpasho|codesapiens'
    project = ProjectStructure(
        target_path=settings.temp_folder+'/'+project_name)
    project_main_folder = FolderStructure(
        settings.temp_folder+'/'+project_name)

    # Generates a JSON with all config files classified
    list_of_files_concatenated = ''
    for file_structure in project_main_folder.files:
        list_of_files_concatenated += file_structure.absolute_path + '\n'
    config_list = get_gpt_response_from_template(
        data={'app_name': project_name, 'trimmable_content': list_of_files_concatenated}, template='what_are_these_config_files', trim_content=True)
    config_list = json.loads(config_list)

    # Based on the JSON, generate the documentation for each config file
    generate_root_config_files(
        config_list=config_list, project_name=project_name)

    # Generate all documentation per file
    generate_documentation_for_project_per_file(
        project=project, project_name=project_name)

    # Generate documentation for all folders
    output_project = ProjectStructure(
        target_path=settings.output_folder+'/'+project_name)
    generate_documentation_for_project_per_folder(
        project=output_project, project_name=project_name)

    # Generate indexes
    output_project_for_indexing = ProjectStructure(
        target_path=settings.output_folder+'/'+project_name)
    raw_docs = []
    all_files = output_project_for_indexing.get_all_files()
    for file in all_files:
        raw_docs.append(file.get_content(file.path))
    raw_docs_v2 = group_and_partition_documents(documents=raw_docs)
    embeed_md_files_to_store(docs=raw_docs_v2)
    return 'All Good!'


@app.route("/api/answer", methods=["POST"])
def answer():
    auth_header = request.headers.get('x-codesapiens-auth')
    if auth_header != settings.CROSS_ORIGIN_SERVICE_SECRET:
        return jsonify({"error": "Invalid request"}), 401

    # Get data from request body
    data = request.get_json()
    id_user = data.get("id_user")
    id_chat = data.get("id_chat")
    prompt = data.get("prompt")

    if not id_user or not id_chat or not prompt:
        return jsonify({"error": "Missing id_user, id_chat, or prompt in request body"}), 400

    # Validate chat status
    chat_data = get_chat(id_chat=id_chat)
    if not chat_data.data or chat_data.data[0].get("status") != "active":
        return jsonify({"error": "Chat is not active or does not exist"}), 403

    doc_store = get_vector_doc_store(settings.output_folder)
    return generate_prompt_answer(prompt=prompt, vector_store=doc_store, id_user=id_user, id_chat=id_chat, id_project=chat_data.data[0].get("project_id"))


@app.route("/api/process_project_files", methods=["POST"])
def process_uploaded_files():
    data = request.get_json()
    id_user = data.get("id_user")
    id_chat = data.get("id_chat")
    id_repository = data.get("id_repository")

    queue_item = index_project_files.delay()
    process_status = get_process_status(queue_item.id)
    print(process_status)
    return {"status": "STARTED", "process_id": queue_item.id}
