import uuid
import json
import pika
import shutil
import sqlite3
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI()


UPLOAD_DIR = "uploads"
RESULTS_DB = "results.db"
os.makedirs(UPLOAD_DIR, exist_ok=True)



def init_db():
    conn = sqlite3.connect(RESULTS_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id TEXT PRIMARY KEY, status TEXT, count INTEGER)''')
    conn.commit()
    conn.close()


init_db()



def send_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()



def save_task_init(task_id):
    conn = sqlite3.connect(RESULTS_DB)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (id, status, count) VALUES (?, ?, ?)", (task_id, "PENDING", 0))
    conn.commit()
    conn.close()



@app.post("/detect/upload")
async def detect_upload(file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{task_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    save_task_init(task_id)
    send_to_queue({"id": task_id, "type": "file", "path": file_path})
    return {"task_id": task_id, "status": "PENDING"}



@app.get("/detect/url")
async def detect_url(url: str):
    task_id = str(uuid.uuid4())
    save_task_init(task_id)
    send_to_queue({"id": task_id, "type": "url", "url": url})
    return {"task_id": task_id, "status": "PENDING"}



@app.get("/detect/local")
async def detect_local(path: str):
    task_id = str(uuid.uuid4())
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    save_task_init(task_id)
    send_to_queue({"id": task_id, "type": "file", "path": path})
    return {"task_id": task_id, "status": "PENDING"}



@app.get("/status/{task_id}")
async def get_status(task_id: str):
    conn = sqlite3.connect(RESULTS_DB)
    c = conn.cursor()
    c.execute("SELECT status, count FROM tasks WHERE id=?", (task_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return {"task_id": task_id, "status": row[0], "person_count": row[1]}
    return {"error": "Task not found"}