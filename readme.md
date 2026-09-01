# GHOST 👻

GHOST (Generalized Hybrid Operating System for Thought) is a local-first AI workspace that combines language models, memory, retrieval systems, and external tools into a unified environment.

Designed as a personal AI operating system, GHOST aims to provide a single interface for knowledge management, intelligent assistance, task execution, and long-term collaboration.

## Core Objectives

- Conversational AI
- Persistent memory
- Retrieval-Augmented Generation (RAG)
- MCP-based tool integration
- Document intelligence
- Task and project management
- Multi-model orchestration

---

# Project Status

**Version:** v0.5

## Implemented Features

### Backend Infrastructure

- FastAPI application server
- Qwen model integration
- Intelligent routing layer
- ChromaDB vector storage
- Retrieval-Augmented Generation pipeline
- Memory management system
- Document ingestion and indexing

### MCP Ecosystem

#### Browser MCP

- Web search
- Page retrieval
- Content extraction

#### Filesystem MCP

- File creation
- File reading
- File editing
- File deletion
- File search

### Frontend (UI v2)

#### Navigation System

- Sidebar-based navigation
- Dynamic page rendering
- Single-page application architecture

#### Workspace Pages

- Overview
- Knowledge
- Files
- Tasks
- Brain
- Developer
- Settings

#### Chat Interface

- Interactive chat panel
- FastAPI integration
- End-to-end messaging pipeline

---

# System Architecture

```text
User
 │
 ▼
GHOST Interface
 │
 ▼
FastAPI Backend
 │
 ├── Router Model (Qwen3 0.6B)
 ├── Primary Model (Qwen3 8B)
 ├── Memory System
 ├── ChromaDB
 ├── RAG Pipeline
 └── MCP Layer
      ├── Browser MCP
      └── Filesystem MCP
```

---

# Repository Structure

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

# Workspace Modules

### Overview

Provides a high-level summary of system activity, project information, tool availability, and operational status.

### Knowledge

Displays document statistics, chunking information, embeddings, and vector database health.

### Files

Interface for interacting with the Filesystem MCP and managing local resources.

### Tasks

Centralized dashboard for task tracking and project planning.

### Brain

Dedicated workspace for memory management and knowledge representation.

### Developer

System diagnostics, model information, MCP status, and runtime monitoring.

### Settings

Application configuration and personalization options.

---

# Roadmap

## Near-Term Goals

### Chat Experience

- Message bubbles
- Typing indicators
- Improved response formatting
- Dynamic page titles
- Enhanced scrolling behavior

### Backend Connectivity

- Live dashboard statistics
- Real-time MCP monitoring
- Dynamic memory metrics
- Live document analytics

### Knowledge Features

- Semantic document search
- Document preview system
- Retrieval source citations

---

## Future Development

### Agentic Systems

- Multi-step reasoning
- Autonomous workflows
- Tool orchestration

### Memory Expansion

- Episodic memory
- Semantic memory
- Project-aware memory

### Additional MCP Integrations

- Git MCP
- Calendar MCP
- Email MCP
- Database MCP
- Notion MCP

---

# Vision

GHOST is being built as a long-term AI operating system that can reason, remember, retrieve information, utilize tools, and assist across projects from a single workspace.

The focus is on creating a local-first, extensible, and developer-friendly platform that evolves from a traditional chatbot into a persistent AI collaborator.
