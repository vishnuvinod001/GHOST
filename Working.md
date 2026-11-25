I want to add an interactive simulation of my personal AI system, **GHOST (Generalized Hybrid Operating System for Thought)**, to my portfolio.

First, understand how GHOST actually works.

### What is GHOST?

GHOST is a local-first personal AI operating system built using Python, FastAPI, Ollama and MCP.

It uses three AI models/components:

- **Qwen3 8B:** Main conversational model responsible for generating responses.
- **Qwen3 0.6B:** Lightweight model that analyses user requests and determines whether an external tool needs to be executed.
- **nomic-embed-text:** Generates embeddings for document retrieval.

### How does GHOST work?

When a user sends a message:

1. The message reaches the FastAPI backend.
2. Qwen3 0.6B analyses the request and determines whether an MCP tool is required.
3. If a tool is required, GHOST executes it through its MCP Manager.
4. GHOST retrieves relevant stored memories.
5. For normal conversations, it retrieves relevant document chunks using FAISS when applicable.
6. The collected context is passed to Qwen3 8B.
7. Qwen3 8B generates the final response.
8. Conversation messages and extracted memories are persisted in SQLite.

### Main capabilities

**Conversational AI:** Natural conversations using a locally hosted LLM.

**Persistent Memory:** Extracts useful information from conversations, categorises it, avoids duplicates and stores it in SQLite.

**Knowledge Base (RAG):** Accepts PDFs, extracts text, splits it into overlapping chunks, generates embeddings, stores them in SQLite and indexes them using FAISS. Retrieves the top three relevant chunks when answering document-related questions.

**Filesystem MCP:** Allows GHOST to list uploaded documents, read, create, edit, delete and search files within its configured workspace.

**Browser MCP:** Fetches user-provided URLs and extracts readable webpage content.

**Task Management:** Supports creating, listing, completing and deleting persistent tasks.

### What I want you to build

Create an interactive, portfolio-friendly simulation that demonstrates how GHOST operates internally.

The simulation should let visitors interact with GHOST and see the internal processing flow, including:

- Incoming user message.
- Lightweight model analysing the request.
- Tool-routing decision.
- Memory retrieval.
- RAG retrieval when relevant.
- MCP tool execution when applicable.
- Main LLM generating the response.
- Final response.

Demonstrate different scenarios, such as ordinary conversation, asking a question about an uploaded document, retrieving a memory, and requesting a file operation.

**Important:** This is a portfolio demonstration, not the actual GHOST backend. Simulate the processing stages and responses realistically. Do not falsely claim to connect to my local Ollama models, SQLite database or MCP servers.

Inspect the existing portfolio architecture before implementation. Integrate this as a self-contained interactive component, preserve the existing portfolio design and functionality, and make the experience visually polished.

The goal is to let recruiters understand that GHOST is more than a chatbot: it is a modular AI system combining LLM inference, routing, memory, RAG and tool execution.
