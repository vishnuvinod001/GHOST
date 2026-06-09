# ==============================================================
# IMPORTS
# ==============================================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from fastapi import UploadFile, File
from pypdf import PdfReader
import ollama
import json
import sqlite3

# ==============================================================
# DATABASE SETUP
# ==============================================================

conn = sqlite3.connect("ghost.db", check_same_thread = False)
cursor = conn.cursor()

# ==============================================================
# TABLE CREATION
# ==============================================================

cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task TEXT NOT NULL,
                   completed INTEGER DEFAULT 0
                )
                """)
conn.commit()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS memories (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   type TEXT NOT NULL,
                   value TEXT NOT NULL,
                   UNIQUE(type, value)
                )
                """)
conn.commit()

with open("data/memory.json", "r") as file:
    memories = json.load(file)
    
for memory in memories:
    cursor.execute(
        """
        INSERT OR IGNORE INTO memories
        (type, value)
        VALUES (?, ?)
        """,
            (
               memory["type"],
              memory["value"]
            )
        )
conn.commit()
    

# ==============================================================
# PYDANTIC MODELS
# ==============================================================
class MemoryResponse(BaseModel): # Future validation model for memory extraction
    remember: bool
    memories: list
    
class Message(BaseModel):
    text: str
    
class Task(BaseModel):
    task: str
    
class TaskID(BaseModel):
    id: int


with open("data/chat_history.json", "r") as file:
    conversation_history = json.load(file)
    
# ==============================================================
# APP CONFIGURATION
# ==============================================================

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates(directory = "templates")


# ==============================================================
# MAIN CHAT ROUTES
# ==============================================================

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
    
    Treat these as instructions.
    
    Extract only the information that follows,
    not the command itself.
    
    then prioritize storing the relevant information.
    
    "Remember that I am pursuing MCA"
    → education

    "Save that I want to become an AI Engineer"
    → goal

    "Don't forget that I prefer Python"
    → preference

    "Store the fact that I am building GHOST"
    → project
    
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
    
    cursor.execute(
    """
    SELECT type, value
    FROM memories
    """
    )
    
    rows = cursor.fetchall()
    
    existing_memories = []
    
    memory_text = ""
    
    for row in rows:
        existing_memories.append(
            {
                "type": row[0],
                "value": row[1]
            }
        )
        
        memory_text += f"- {row[0]}: {row[1]}\n"

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
                
                cursor.execute(
                    """INSERT INTO memories
                    (type, value)
                    VALUES (?, ?)
                    """,
                    (
                        memory["type"],
                        memory["value"]
                    )
                )
                
                conn.commit()
                existing_memories.append(memory)
    
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


# ==============================================================
# PDF ROUTES
# ==============================================================

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
    
# ==============================================================
# TASK ROUTES
# ==============================================================   

@app.post("/add-task")
def add_task(task: Task):
    
    cursor.execute(
    """
    INSERT INTO tasks
    (task, completed)
    VALUES (?, ?)
    """,
    (
        task.task,
        0
     )
    )
    
    conn.commit()
    
    return{
        "message" : "Task Added"
    }


@app.get("/tasks")
def get_tasks():
    
    cursor.execute(
    """
    SELECT * FROM tasks
    """
    )
    rows = cursor.fetchall()
    
    tasks = []
    
    for row in rows:
        tasks.append(
            {
                "id" : row[0],
                "task" : row[1],
                "completed" : bool(row[2])
            }
        )
    return tasks


@app.post("/complete-task")
def complete_task(task_id: TaskID):
    
    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id = ?
        """,
        (
            task_id.id,
        )
    )
    conn.commit()
    return{
        "message" : "Task Completed"
    }


@app.post("/delete-task")
def delete_task(task_id: TaskID):
    
    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (
            task_id.id,
        )
    )
    
    conn.commit()
    
    return {
        "message" : "Task Deleted"
    }  