# ==============================================================
# IMPORTS
# ==============================================================

# FastAPI
from fastapi import FastAPI
from fastapi import Request
from fastapi import UploadFile, File

# FastAPI Responses & Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Data Validation
from pydantic import BaseModel

# PDF Processing
from pypdf import PdfReader

# RAG
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import numpy as np

# LLM
import ollama

# Database & Storage
import sqlite3
import json


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

cursor.execute("""
               CREATE TABLE IF NOT EXISTS chat_history (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     role TEXT NOT NULL,
                     content TEXT NOT NULL
                 )
                 """)
conn.commit()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS chunks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   source  TEXT NOT NULL,
                   content TEXT NOT NULL
               ) 
               """)
conn.commit()

#cursor.execute(
#        """
#        DELETE FROM memories
#        WHERE type = "goal"
#        """
#    )
#conn.commit()


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



    
# ==============================================================
# APP CONFIGURATION
# ==============================================================

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates(directory = "templates")

faiss_index = None
stored_chunks = []


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
    
    cursor.execute(
        """
        INSERT INTO chat_history
        (role, content)
        VALUES (?, ?)
        """,
        (
            "user",
            message.text
        )
     )
    
    conn.commit()
    
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
    
    try:
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
    
        memory_data = json.loads(memory_reply)
    
    except Exception as e:
        
        print("Memory extraction failed:", e)
        
        memory_data = {
            "remember": False,
            "memories": []
        }
    
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
    
    
    if message.text.lower() == "what do you know about me?":

        reply = ""

        for memory in existing_memories:
            reply += (
                f"{memory['type'].capitalize()}: "
                f"{memory['value']}\n\n"
            )

        return {
            "reply": reply
        }
    
    
    cursor.execute(
        """
        SELECT role, content
        FROM chat_history
        ORDER BY id
        """
    )
    
    rows = cursor.fetchall()
    
    conversation_history = []
    
    for row in rows:
        conversation_history.append(
            {
                "role": row[0],
                "content": row[1]
            }
        )
    
    retrieved_context = ""
    
    if faiss_index is not None:
        
        response = ollama.embed(
            model = "nomic-embed-text",
            input = message.text
        )
        
        query_embedding = np.array(
            [response["embeddings"][0]]
        ).astype("float32")
        
        distances, indices = faiss_index.search(
            query_embedding,
            k=3
        )
        
        retrieved_chunks = []
        
        for i in indices[0]:
            retrieved_chunks.append(stored_chunks[i])
            
        retrieved_context = "\n\n".join(retrieved_chunks)
    
    if retrieved_context:

        system_prompt = f"""
        You are GHOST, a personal AI assistant.

        Avoid markdown formatting.
        Do not use **bold**, *, #, bullet lists, or emojis unless specifically requested.
        Respond in clean plain text with simple spacing.
        Keep responses professional and easy to read.

        When asked about user memories,
        present the information in separate short sections.

        User Memories:
        {memory_text}

        You are answering questions about the uploaded document.

        Use ONLY the provided context.

        If the answer is not present in the context, say:
        "I could not find that information in the uploaded document."

        Do not use outside knowledge.

        Context:

        {retrieved_context}
        """

    else:

        system_prompt = f"""
        You are GHOST, a personal AI assistant.

        Avoid markdown formatting.
        Do not use **bold**, *, #, bullet lists, or emojis unless specifically requested.
        Respond in clean plain text with simple spacing.
        Keep responses professional and easy to read.

        You are GHOST, a general-purpose AI assistant.

        Answer the user's question directly.

        Only use User Memories when:
        - the user asks about themselves
        - the user asks "what do you know about me?"
        - the user asks about their goals, projects, interests, skills, or preferences

        For all other questions, ignore User Memories unless they are directly relevant.

        User Memories:
        {memory_text}
        """
        
    messages_for_model = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + conversation_history
    
    
    response = ollama.chat(
        model = "qwen3:8b",
        messages = messages_for_model
    )
    
    ai_reply = response["message"]["content"]
    
    cursor.execute(
        """
        INSERT INTO chat_history
        (role, content)
        VALUES (?, ?)
        """,
        (
            "assistant",
            ai_reply
        )
    )
    
    conn.commit()
    
    
    return {
        "reply": ai_reply
    }


@app.post("/clear")
def clear_memory():
    
    cursor.execute(
        """
        DELETE FROM chat_history
        """
    )
    
    conn.commit()
    
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
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    
    chunks = splitter.split_text(pdf_text)
    
    for chunk in chunks:
        
        cursor.execute(
            """
            INSERT INTO chunks
            (source, content)
            VALUES (?, ?)
            """,
            (
                file.filename,
                chunk
            )
            
        )
    conn.commit()
    
    embeddings = []
    
    for chunk in chunks:
        response = ollama.embed(
            model = "nomic-embed-text",
            input = chunk
        )
        embeddings.append(response["embeddings"][0])
    
    global faiss_index
    global stored_chunks
    
    embeddings_np = np.array(embeddings).astype("float32")
    
    if faiss_index is None:
        faiss_index = faiss.IndexFlatL2(768)
    
    faiss_index.add(embeddings_np)
    
    stored_chunks.extend(chunks)
    

    
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
