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

class MemoryResponse(BaseModel):
    remember: bool
    memories: list


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
    
    memory_prompt = f"""You are a memory extraction system.
    
    Analyze the user's message.
    
    If it contains important long-term information about the user, extract it.
    
    Important memory categories :
    
    - name
    - education
    - goal
    - project
    - interest
    - preference
    - skill
    - relationship
    
    Examples:
    
    "My name is Vishnu" -> name

    "I am pursuing MCA" -> education

    "I have a Physics degree" -> education

    "I want to become an AI Engineer" -> goal

    "I am building GHOST" -> project

    "I am interested in Machine Learning" -> interest

    "I prefer Python over Java" -> preference

    "I know FastAPI and Python" -> skill

    "I am building GHOST from scratch" -> project

    "You are GHOST and I am building you" -> relationship

    "I ate dosa today" -> not important
    
    
    If the user explicitly says:
    "remember this"
    "save this"
    "store this"
    "don't forget this"
    
    then prioritize storing the relevant information.
    
    Return ONLY valid JSON.
    
    Format:
    
    {{
        "remember" : true,
        "memories" : [
            {{
                "type" : "name",
                "value" : "Vishnu"
            }}
        ]
    }}
    
    User message: 
    {message.text}
    
    """
    
    memory_response = ollama.chat(
        model = "qwen3:8b",
        messages = [
            {
                "role" : "user",
                "content" : memory_prompt
            }
        ]
    )
    
    memory_reply = memory_response["message"]["content"]
    #print(memory_reply)
    
    memory_data = json.loads(memory_reply)
    #print(type(memory_data))
    #print(memory_data)
    
    with open("data/memory.json", "r") as file:
        existing_memories = json.load(file)
        
    memory_text = ""

    for memory in existing_memories:
        memory_text += f'- {memory["type"]}: {memory["value"]}\n'

    #print(memory_text)
        
    if memory_data["remember"]:
        for memory in memory_data["memories"]:
                
            duplicate_found = False
            for existing_memory in existing_memories:
                if (
                    memory["type"].lower() == existing_memory["type"].lower()
                    and
                    memory["value"].lower() == existing_memory["value"].lower()
                ):
                    duplicate_found = True
                    break
        if not duplicate_found:
            existing_memories.append(memory)
    
    with open("data/memory.json", "w") as file:
        json.dump(existing_memories, file, indent = 4)
    
    #print(existing_memories)
    
    #print(type(existing_memories))
    #print(existing_memories)
    
    messages_for_model = [
        {
            "role" : "system",
            "content" : f"""
            
            User Memories:
            {memory_text}
            
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

@app.post("/delete-task")
def delete_task(task_id: TaskID):
    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)
         
    for index, task in enumerate(tasks):
        if task["id"] == task_id.id:
            tasks.pop(index)
            break
    
    # ---------------------------OR--------------------------------    
    # Alternative approach (without pop + enumerate)

    # tasks = [
    #     task
    #     for task in tasks
    #     if task["id"] != task_id.id
    # ]

    # This creates a new list containing all tasks
    # except the one whose id matches task_id.id.
    # More Pythonic, but the current enumerate + pop
    # approach was kept for learning purposes.
    
    # ---------------------------OR------------------------------
    # Alternative approach

    # new_tasks = []

    # for task in tasks:
    #     if task["id"] != task_id.id:
    #         new_tasks.append(task)

    # tasks = new_tasks

    # Keeps every task except the one being deleted.
            
    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent = 4)
    
    return {
        "message" : "Task Deleted"
    }
    
        