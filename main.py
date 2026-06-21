# ==============================================================
# IMPORTS
# ==============================================================

import os

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

# Ghost Replies
import random

# ==============================================================
# VERSION & MESSAGES
# ==============================================================

GHOST_VERSION = "0.4.0"

EMPTY_MESSAGE_REPLIES = [

    "Standing by, Boss.",

    "Awaiting input, Boss.",

    "I'm listening, Boss.",

    "No message detected, Boss.",

    "Ready when you are, Boss.",

    "Systems operational. Awaiting instructions.",

    "Your move, Boss.",

    "I appear to have received silence.",

    "Communication channel open, Boss.",

    "Standing by for further instructions."

]

# ==============================================================
# GHOST PERSONALITY DESCRIPTION
# ==============================================================

ghost_identity = """
You are GHOST, an advanced personal AI operating system created by Vishnu.

Your identity is GHOST.
The underlying language model is only the engine powering you.

Your creator and primary user is Vishnu.

Address him as "Boss" naturally when appropriate, but do not overuse it.

When asked who you are:
You are GHOST, a personal AI system built by Vishnu.

When discussing ongoing development:
GHOST itself is the project being developed.
"""

#---------------------------------------------------------------

ghost_personality = """
Personality:

- Intelligent
- Calm
- Efficient
- Observant
- Professional
- Slightly witty

Communication Style:

- Think like an engineering partner.
- Avoid sounding like customer support.
- Avoid generic assistant phrases.
- Keep greetings short and natural.
- Be direct and practical.
- Give detailed technical explanations when required.

Do not introduce yourself as ChatGPT or Qwen.

Do not mention the underlying model unless explicitly asked.

Greeting Rules:

When the user greets you:

- Keep responses short.
- Do not ask "How can I help you today?"
- Do not ask "How can I assist you today?"
- Do not give customer-support style responses.

Examples:

User: Hey GHOST

GHOST:
Good evening, Boss.
GHOST online.

User: Morning

GHOST:
Good morning, Boss.
All systems operational.

User: What's our status?

GHOST:
Knowledge Base operational.
Embeddings indexed.
Current priority: Delete Documents.

User: What's the plan?

GHOST:
Current priority: Delete Documents.
Source Citations follow.
"""
#---------------------------------------------------------------

ghost_formatting = """
Formatting Rules:

Avoid markdown formatting.

Do not use:
- **
- *
- #
- emojis

unless explicitly requested.

Respond in clean plain text.

Use short paragraphs and spacing for readability.
"""


# ==============================================================
# DATABASE SETUP
# ==============================================================

conn = sqlite3.connect("ghost.db", check_same_thread = False)
cursor = conn.cursor()

# ==============================================================
# AUTOMATIC FAISS BUILDING AND APP STARTUP
# ==============================================================

def rebuild_faiss():
    
    global faiss_index
    global stored_chunks
    
    local_cursor = conn.cursor()
    
    local_cursor.execute(
        """
        SELECT content, source
        FROM chunks
        """
    )
    
    chunk_rows = local_cursor.fetchall()
    
    stored_chunks = []
    
    for content, source in chunk_rows:
        stored_chunks.append(
            {
                "content": content,
                "source": source 
            }
        )
    
    if not chunk_rows:
        print("No chunks found")
        return
    
    local_cursor.execute(
        """
        SELECT embedding
        FROM embeddings
        ORDER BY chunk_id
        """
    )
    
    embedding_rows = local_cursor.fetchall()
    
    embeddings = []
    
    for row in embedding_rows:
        embeddings.append(
            json.loads(row[0])
        )
        
    embeddings_np = np.array(
        embeddings,
        dtype = np.float32
    )
    
    faiss_index = faiss.IndexFlatL2(768)
    faiss_index.add(embeddings_np)
    
    print(f"Loaded {len(stored_chunks)} chunks into FAISS")

#------------------------------------------------------------------------------------------
def populate_missing_embeddings():
    
    local_cursor = conn.cursor()
    
    local_cursor.execute("""
                         SELECT id, content
                         FROM chunks
                         WHERE id NOT IN (
                             SELECT chunk_id
                             FROM embeddings
                         )
                         """)
    
    rows = local_cursor.fetchall()
    
    print(f"Missing embeddings: {len(rows)}")
    
    for chunk_id, content in rows:
        
        response = ollama.embed(
            model = "nomic-embed-text",
            input = content
        )
        
        embedding = response["embeddings"][0]
        
        local_cursor.execute(
            """
            INSERT INTO embeddings
            (chunk_id, embedding)
            VALUES (?, ?)
            """,
            (
                chunk_id,
                json.dumps(embedding)
            )
        )
        
        print(f"Added embedding for chunk {chunk_id}")
        
    conn.commit()
    print("Embedding migration complete")
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

cursor.execute("""
               CREATE TABLE IF NOT EXISTS embeddings (
                   chunk_id INTEGER PRIMARY KEY,
                   embedding TEXT NOT NULL,
                   FOREIGN KEY(chunk_id) REFERENCES chunks(id)
               )
               """)
conn.commit()
#populate_missing_embeddings()

#cursor.execute(
#        """
#        DELETE FROM memories
#        WHERE type = "interest" AND value = "batman"
#        """
#    )
#conn.commit()
#cursor.execute("""
#SELECT COUNT(*) FROM embeddings
#""")

#

#print(cursor.fetchone()[0])

#

#cursor.execute("""
#SELECT COUNT(*) FROM chunks
#""")

#

#print(cursor.fetchone()[0])

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

faiss_index = None
stored_chunks = []

app = FastAPI()
rebuild_faiss()

app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates(directory = "templates")


# ==============================================================
# MAIN CHAT ROUTES
# ==============================================================

@app.get("/version")
def get_version():
    return {"version" : GHOST_VERSION}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "index.html"
    )
    
@app.post("/chat")
def chat(message: Message):
    
    if not message.text.strip():
        return {
            "reply": random.choice(
                EMPTY_MESSAGE_REPLIES
            )
    }
    
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
    
    small_talk = [
        "hi",
        "hello",
        "hey",
        "morning",
        "good morning",
        "good evening",
        "thanks",
        "thank you",
        "bye"
    ]
    
    if (
        faiss_index is not None
        and
        message.text.lower().strip() not in small_talk
        ):
        
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
        retrieved_sources = set()
        
        for i in indices[0]:
            
            retrieved_chunks.append(
                stored_chunks[i]["content"]
            )
            
            retrieved_sources.add(
                stored_chunks[i]["source"]
            )
            
        retrieved_context = "\n\n".join(retrieved_chunks)
    
    if retrieved_context:

        system_prompt = f"""
            {ghost_identity}

            {ghost_personality}

            {ghost_formatting}

            User Memories:
            {memory_text}

            You are answering questions about uploaded documents.

            Use ONLY the provided context.

            If the answer is not present in the context, say:

            I could not find that information in the uploaded document.

            Do not use outside knowledge.

            Context:

            {retrieved_context}
            
            Sources:
            
            {", ".join(retrieved_sources)}
        """

    else:

        system_prompt = f"""
            {ghost_identity}

            {ghost_personality}

            {ghost_formatting}

            User Memories:
            {memory_text}

            Answer the user's question directly.

            Only use User Memories when:

            - the user asks about themselves
            - the user asks what you know about them
            - the user asks about their goals
            - the user asks about their projects
            - the user asks about their interests
            - the user asks about their skills
            - the user asks about their preferences

            For all other questions, ignore User Memories unless directly relevant.
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
    
    citation_text = ""
    
    if retrieved_context:
        
        if len(retrieved_sources) == 1:
            
            citation_text = (
                "\n\n📚 Reference Document:\n" 
                + "\n".join(retrieved_sources)
            )
            
        else:
            
            citation_text = (
                "\n\n📚 Reference Documents:\n" 
                + "\n".join(retrieved_sources)
            )
    
    return {
        "reply": ai_reply + citation_text
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
    
    embeddings = []
    
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
        
        chunk_id = cursor.lastrowid
        
        response = ollama.embed(
            model = "nomic-embed-text",
            input = chunk
        )
        
        embedding = response["embeddings"][0]
        
        cursor.execute(
            """
            INSERT INTO embeddings
            (chunk_id, embedding)
            VALUES (?, ?)
            """,
            (
                chunk_id,
                json.dumps(embedding)
            )
        )
        conn.commit()
        
        
        print("Inserted:", chunk_id)
        embeddings.append(embedding)
        
    conn.commit()
    
    
    
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


@app.get("/documents")
def get_documents():
    
    local_cursor = conn.cursor()
    
    local_cursor.execute("""
                   
        SELECT DISTINCT source
        FROM chunks
    """)
    
    documents = local_cursor.fetchall()
    
    return [doc[0] for doc in documents]

@app.post("/delete-document")
def delete_document(filename: str):
    
    local_cursor = conn.cursor()
    
    local_cursor.execute(
        """
        SELECT id
        FROM chunks
        WHERE source = ?
        
        """, (filename,)
    )
    
    chunk_ids = [row[0] for row in local_cursor.fetchall()]
    
    for chunk_id in chunk_ids:
        
        local_cursor.execute(
            """
            DELETE FROM embeddings
            WHERE chunk_id = ?
            """, (chunk_id,)
        )
        
        local_cursor.execute(
            """
            DELETE FROM chunks
            WHERE source = ?
            """, (filename,)
        )
        
    conn.commit()
    
    pdf_path = f"data/documents/{filename}"
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        
    rebuild_faiss()
        
    return {
        "message" : f"{filename} deleted successfully"
    }
# ==============================================================
# TASK ROUTES
# ==============================================================   

@app.post("/add-task")
def add_task(task: Task):
    
    local_cursor = conn.cursor()
    
    local_cursor.execute(
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
    
    local_cursor = conn.cursor()
    
    local_cursor.execute(
    """
    SELECT * FROM tasks
    """
    )
    rows = local_cursor.fetchall()
    
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
    local_cursor = conn.cursor()
    
    local_cursor.execute(
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
    
    local_cursor = conn.cursor()
    
    local_cursor.execute(
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

# ==============================================================
# OTHER API ROUTES
# ==============================================================  

@app.get("/stats")
def get_stats():
    
    local_cursor = conn.cursor()
    
    local_cursor.execute("""
                         SELECT COUNT(DISTINCT source)
                         FROM chunks
                         """)
    pdf_count = local_cursor.fetchone()[0]
    
    local_cursor.execute("""
                         SELECT COUNT(*)
                         FROM chunks
                         """)
    chunk_count = local_cursor.fetchone()[0]
    print("Chunk count:", chunk_count)
    
    local_cursor.execute("""
                         SELECT COUNT(*)
                         FROM tasks
                         """)
    task_count = local_cursor.fetchone()[0]
    
    return {
        "pdf_count" : pdf_count,
        "chunk_count" : chunk_count,
        "task_count" : task_count
    }