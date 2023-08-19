from flask import Flask, request
from background_jobs import index_project_files, get_process_status
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


@app.route("/api/process_project_files", methods=["POST"])
def process_uploaded_files():
    # 1. Get the uploaded files
    # 2. Generate md per function per project
    # 3. Generate faiss index
    queue_item = index_project_files.delay()
    return {"status": "processing", "process_id": queue_item.id}


# User connectes repo
# On connects, upload folder to server
# On upload, run another request
# The request should be a parser that converts the folder into faiss


# In frontend, we will have:
# Step 1: Connect repo
# Step 2: Upload folders and wait uploading.
# Step 3: Wait to being processed
# Step 4: Show results
