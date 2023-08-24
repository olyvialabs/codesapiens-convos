from flask import Flask, request, Response
import json
from background_jobs import index_project_files, get_process_status
from llm.embeeding import get_vector_doc_store, get_stream_answer
from langchain.prompts import PromptTemplate
from config.settings import settings
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

app = Flask(__name__)

with open("templates/question_prompt.txt", "r") as f:
    template_quest = f.read()
with open("templates/chat_combine_prompt.txt", "r") as f:
    chat_combine_template = f.read()


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


@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.get_json()
    # get parameter from url question
    prompt = data["prompt"]
    q_prompt = PromptTemplate(input_variables=[
                              "context", "question"], template=template_quest, template_format="jinja2")
    # history = data["history"]
    # if history:
    #    history = []
    # history = json.loads(history)
    llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0)


@app.route("/api/process_project_files", methods=["POST"])
def process_uploaded_files():
    # 1. Get the uploaded files
    # 2. Generate md per function per project
    # 3. Generate faiss index
    queue_item = index_project_files.delay()
    process_status = get_process_status(queue_item.id)
    print(process_status)
    return {"status": "STARTED", "process_id": queue_item.id}


# User connectes repo
# On connects, upload folder to server
# On upload, run another request
# The request should be a parser that converts the folder into faiss


# In frontend, we will have:
# Step 1: Connect repo
# Step 2: Upload folders and wait uploading.
# Step 3: Wait to being processed
# Step 4: Show results
