from flask import Flask, request, jsonify
from background_jobs import get_process_status, index_project_files
from llm.answer import generate_prompt_answer
from config.settings import settings
from persister.supabase import get_chat, get_repository_by_id

app = Flask(__name__)


@app.route("/")
def home():
    return {"status": "hey, wtf you doing here?"}


@app.route("/api/process_status", methods=["GET"])
def process_status():
    process_id = request.args.get("process_id")
    if not process_id:
        return {"status": "BAD_REQUEST", "details": "no process_id provided"}
    return get_process_status(process_id)


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

    return generate_prompt_answer(prompt=prompt,  id_user=id_user, id_chat=id_chat, id_project=chat_data.data[0]['projectId'])


@app.route('/api/v1/embeed-sync', methods=['POST'])
def embeedSync():
    data = request.get_json()
    id_user = data.get("id_user")
    id_repositories = data.get("id_repositories", [])  # expect an array
    # id_repositories = ['clotwbl80000lyh2zvc1ip4pa']
    processes = []

    for id_repository in id_repositories:
        repository = get_repository_by_id(id_repository)
        if not repository.data:
            return jsonify({"error": "Repository does not exist"}), 404

        print('Process about to index')
        index_project_files(id_user, repository.data[0])
        # queue_item = index_project_files.delay(id_user, repository.data[0])
        # processes.append(queue_item.id)
        # process_status = get_process_status(queue_item.id)
    return {"status": "STARTED", "processes": processes}


@app.route("/api/v1/process_repositories", methods=["POST"])
def process_uploaded_files():
    # data = request.get_json()
    # id_user = data.get("id_user")
    # id_repositories = data.get("id_repositories", [])  # expect an array
    # for id_repository in id_repositories:
    #     repository = get_repository_by_id(id_repository)
    #     if not repository.data:
    #         continue
    #         # return jsonify({"error": "Repository does not exist"}), 404

    #     queue_item = index_project_files.delay(
    #         id_user, repository.data[0])
    #     # process_status = get_process_status(queue_item.id)
    # return {"status": "STARTED"}
    return {"status": "NOT_IMPLEMENTED"}
