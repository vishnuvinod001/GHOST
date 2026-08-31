# GHOST 👻

GHOST (Generalized Hybrid Operating System for Thought) is a local-first AI assistant designed to combine LLM reasoning, memory, retrieval, tools, and project management into a single workspace.

The goal is to create a personal AI operating system capable of:

- Conversational AI
- Persistent memory
- Retrieval-Augmented Generation (RAG)
- MCP tool integration
- Document intelligence
- Task and project management
- Multi-model routing

---

# Current Status

Version: v0.5

## Completed

### Core Backend
- FastAPI backend
- Qwen model integration
- Router model integration
- ChromaDB vector database
- RAG pipeline
- Memory system
- Document ingestion pipeline

### MCP Tools

#### Browser MCP
- Web search
- Page retrieval
- Content extraction

#### Filesystem MCP
- Read files
- Create files
- Edit files
- Delete files
- Search files

### Frontend (UI v2)

#### Navigation
- Sidebar navigation
- Dynamic page switching
- Single-page dashboard architecture

#### Pages
- Overview
- Knowledge
- Files
- Tasks
- Brain
- Developer
- Settings

#### Chat
- Frontend chat interface
- Backend communication
- End-to-end message flow

---

# Architecture

```text
User
 │
 ▼
GHOST UI
 │
 ▼
FastAPI Backend
 │
 ├── Router Model (Qwen3 0.6B)
 │
 ├── Main Model (Qwen3 8B)
 │
 ├── Memory System
 │
 ├── ChromaDB
 │
 ├── RAG Pipeline
 │
 └── MCP Layer
      │
      ├── Browser MCP
      └── Filesystem MCP
```

---

# Project Structure

```text
GHOST
│
├── main.py
│
├── templates
│   ├── index.html
│   └── index_v2.html
│
├── static
│   │
│   ├── css
│   │   ├── variables.css
│   │   ├── global.css
│   │   ├── layout.css
│   │   ├── sidebar.css
│   │   ├── workspace.css
│   │   ├── cards.css
│   │   ├── chat.css
│   │   ├── animations.css
│   │   ├── responsive.css
│   │   │
│   │   └── pages
│   │       ├── overview.css
│   │       ├── knowledge.css
│   │       ├── files.css
│   │       ├── tasks.css
│   │       ├── brain.css
│   │       ├── developer.css
│   │       └── settings.css
│   │
│   └── js
│       ├── navigation.js
│       ├── pages.js
│       └── app.js
│
├── memory
├── rag
├── mcp
├── models
└── chroma_db
```

---

# Current UI Pages

## Overview
System summary, activity feed, status dashboard, project overview.

## Knowledge
Document statistics, embeddings, chunk information, vector database status.

## Files
Filesystem MCP dashboard and file management interface.

## Tasks
Task tracking and project management dashboard.

## Brain
Memory system and knowledge graph dashboard.

## Developer
Diagnostics, MCP status, model status, and system information.

## Settings
Configuration and system preferences.

---

# Roadmap

## Near-Term

### Chat Improvements
- Chat bubbles
- Typing animation
- Better response formatting
- Dynamic page headers
- Improved scrolling

### Backend Integration
- Real-time dashboard data
- Live MCP status
- Live memory statistics
- Live document statistics

### Knowledge System
- Semantic search
- Document preview
- Source citations

---

## Long-Term

### Agentic Capabilities
- Multi-step planning
- Autonomous workflows
- Tool orchestration

### Memory Expansion
- Episodic memory
- Semantic memory
- Project memory

### Additional MCP Tools
- Git MCP
- Calendar MCP
- Email MCP
- Database MCP
- Notion MCP

---

# Vision

GHOST aims to become a personal AI operating system that can:

- Remember information
- Search knowledge
- Use tools
- Manage projects
- Assist with development
- Act as a long-term AI collaborator

while remaining local-first, extensible, and fully customizable.