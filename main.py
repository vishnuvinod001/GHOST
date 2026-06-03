from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from fastapi import UploadFile, File
from pypdf import PdfReader
import os
import ollama
import json


with open("data/chat_history.json", "r") as file:
    conversation_history = json.load(file)

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates(directory = "templates")


class Message(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "index.html"
    )
    
@app.post("/chat")
def chat(message: Message):
    
    with open(
        "data/documents/pdf_text.txt", "r", encoding = "utf-8"
    ) as file:
        pdf_text = file.read()
    
    conversation_history.append(
        {
            "role" : "user",
            "content" : message.text
        }
    )
    
    messages_for_model = [
        {
            "role" : "system",
            "content" : f"""
            Use the following document to answer questions.
            
            {pdf_text}
            """
        }
    ] + conversation_history
    
    
    with open("data/chat_history.json", "w") as file:
        json.dump(conversation_history, file, indent=4)
    
        
    response = ollama.chat(
        model = "qwen3:8b",
        messages = messages_for_model
    )
    
    ai_reply = response["message"]["content"]
    
    conversation_history.append(
        {
            "role" : "assistant",
            "content" : ai_reply
        }
    )
    
    with open("data/chat_history.json", "w") as file:
        json.dump(conversation_history, file, indent = 4) 
    
    return {
        "reply": ai_reply
    }


@app.post("/clear")
def clear_memory():
    
    global conversation_history
    
    conversation_history = []
    
    with open("data/chat_history.json", "w") as file:
        json.dump(conversation_history, file, indent = 4)
    
    return {"message" : "Memory Cleared"}


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    
    pdf_path = f"data/documents/{file.filename}"
    
    with open(pdf_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    reader = PdfReader(pdf_path)
    
    pdf_text = ""
    
    for page in reader.pages:
        pdf_text += page.extract_text()
    
    with open("data/documents/pdf_text.txt", "w", encoding= "utf-8") as file:
        file.write(pdf_text)
        
    return {
        "message" : "PDF Uploaded successfully"
    }
    
    
class Task(BaseModel):
    task: str
    
@app.post("/add-task")
def add_task(task: Task):
    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)
            
    new_task = {
        "id" : len(tasks) + 1,
        "task" : task.task,
        "completed" : False
    }
        
    tasks.append(new_task)
        
    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent = 4)
        
    return {
        "message" : "Task Added"
    }

@app.get("/tasks")
def get_tasks():
    
    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)
        
    return tasks

class TaskID(BaseModel):
    id: int

@app.post("/complete-task")
def complete_task(task_id: TaskID):
    
    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)
    
    for task in tasks:
        if task["id"] == task_id.id:
            task["completed"] = not task["completed"]
    
    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent = 4)
    
    return {
        "message" : "Task Completed"
    }
    