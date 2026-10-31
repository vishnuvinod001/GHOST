# GHOST 👻

**GHOST — Generalized Hybrid Operating System for Thought** — is a local-first AI workspace being developed as a personal AI operating system. It brings conversational AI, persistent user memory, document retrieval, task management, and MCP-based tools into one application.

The long-term goal is to evolve beyond a conventional chatbot into a persistent, extensible AI collaborator.

---

## Current Project Status

- **Project milestone:** v0.5 (UI v2)
- **Backend version constant:** v0.4.0 (reported by `GET /version`)
- **Backend:** FastAPI
- **Primary model:** Qwen3 8B through Ollama
- **Tool router:** Qwen3 0.6B through Ollama
- **Embedding model:** `nomic-embed-text`
- **Relational storage:** SQLite
- **Vector retrieval:** FAISS
- **Tool protocol:** Model Context Protocol (MCP)

> Version note: the v0.5 label is used by the new UI and project milestone, while `main.py` still reports backend version `0.4.0`. These version identifiers have not yet been unified.

## Features in the Repository

### Conversational AI

- Chat requests are handled by the FastAPI `POST /chat` endpoint.
- Ollama runs the Qwen3 8B model for response generation.
- Qwen3 0.6B classifies requests to decide whether an MCP tool should be called.
- Conversation messages and assistant replies are stored in SQLite.
- The UI displays user messages, assistant replies, and an animated typing indicator.

### Persistent Memory

- GHOST asks Qwen3 8B to extract potentially useful long-term user information from messages.
- Extracted memories are stored in the SQLite `memories` table.
- Duplicate memories are checked by type and value before insertion.
- Stored memories are included in the system prompt and used when relevant to the user's question.

### Document Knowledge and RAG

- PDF files are accepted through `POST /upload-pdf`.
- PDF text is extracted with pypdf.
- Text is split into chunks using LangChain's `RecursiveCharacterTextSplitter` (1,000-character chunks with 200-character overlap).
- Each chunk is embedded using Ollama's `nomic-embed-text` model.
- Chunk text and embedding vectors are stored in SQLite.
- FAISS is used for nearest-neighbour retrieval; the current retrieval function requests the top three chunks.
- Retrieved document context is passed to the main model, and source filenames are appended to the response.
- Documents can be listed and deleted through the document API.

**Implementation detail:** the current RAG implementation uses SQLite plus FAISS. ChromaDB is not used by the current `main.py` pipeline.

### Tasks

- Tasks are stored in the SQLite `tasks` table.
- The backend supports adding, listing, completing/toggling, and deleting tasks.

### MCP Tool Integration

GHOST launches its MCP servers as subprocesses over standard input/output through the MCP Python client.

#### Filesystem MCP

The filesystem server currently defines these tools:

| Tool | Purpose |
|---|---|
| `list_documents` | List entries in `data/documents` |
| `read_file` | Read a file under the GHOST workspace |
| `create_file` | Create a file under the workspace or configured projects directory |
| `edit_file` | Replace, append, or prepend content in a workspace file |
| `delete_file` | Delete a workspace file |
| `search_files` | Search workspace filenames recursively |

Filesystem access is restricted by path-prefix checks in the server. The projects directory is currently configured as a machine-specific Windows path in `ghost_mcp/filesystem/server.py`; configure this for your own environment before using that destination.

#### Browser MCP

| Tool | Purpose |
|---|---|
| `ping` | Return a basic server health response |
| `fetch_url` | Fetch a URL and extract readable page text with requests and BeautifulSoup |

The current Browser MCP implementation fetches a supplied URL. It does **not** currently implement a search-engine/web-search tool.

> **Known integration item to verify:** the filesystem manager's allow-list currently names `search_file`, while the server tool is named `search_files`. Align these names for filename search to be routable. The result formatter also has dedicated formatting only for `list_documents`, `read_file`, and `fetch_url`; other tool results currently fall back to string conversion.

---

## Architecture

```text
                         User
                          |
                          v
                    GHOST UI v2
                 HTML / CSS / JavaScript
                          |
                          v
                       FastAPI
                          |
             +------------+-------------+
             |            |             |
             v            v             v
       Tool Router     Memory         RAG
       Qwen3 0.6B      SQLite      SQLite + FAISS
             |            |             |
             |            |       nomic-embed-text
             |            |             |
             +------------+-------------+
                          |
                          v
                  Response Generation
                     Qwen3 8B
                          |
                          v
                    Chat Response

             MCP tool execution path
                          |
                          v
                   MCP Manager
                    /       \
                   v         v
             Filesystem    Browser
                MCP          MCP
```

### Main Backend Flow

1. The UI sends a message to `POST /chat`.
2. The router model determines whether the request needs a tool.
3. If a tool is selected, the MCP manager executes it and returns the result.
4. GHOST loads stored memories and, for normal chat requests, retrieves relevant document chunks.
5. The main Qwen3 8B model generates the response.
6. User and assistant messages are persisted in SQLite.

Tool requests currently follow a separate prompt path: the tool result is supplied to the main model, rather than being added to the normal conversation-history/RAG path.

---

## Frontend — UI v2

The root route (`GET /`) currently serves `templates/index_v2.html`. The older interface remains in `templates/index.html`.

The UI v2 shell has three persistent regions:

- **Sidebar:** navigation between workspace pages.
- **Workspace:** the selected page.
- **Chat panel:** persistent chat interface.

### Workspace Pages

| Page | Current implementation |
|---|---|
| Overview | Static welcome, summary cards, activity, and system-status content |
| Knowledge | Static document, chunk, and embedding summaries |
| Files | Static file summary and Filesystem MCP tool list |
| Tasks | Static task summary and example task lists |
| Brain | Static memory/project summary and timeline |
| Developer | Static tool, server, and system-status summaries |
| Settings | Static model and feature summary |

Navigation is implemented client-side by replacing the workspace content with page templates from `static/js/pages.js`. Chat submission is handled in `static/js/app.js` and sends requests to the FastAPI backend.

**Frontend status:** the shell, navigation, page layouts, styling, and chat request path exist. The workspace dashboards currently contain hardcoded sample values and are not yet connected to live backend statistics or feature-specific APIs. Several planned page-specific JavaScript files exist but are currently empty.

### Frontend Structure

- `static/css/core/`: design tokens, global styles, animations, and responsive rules.
- `static/css/layout/`: application layout.
- `static/css/components/`: sidebar, workspace, chat, and reusable cards.
- `static/css/pages/`: page-specific styles.
- `static/js/pages.js`: HTML templates for workspace pages.
- `static/js/navigation.js`: client-side page switching.
- `static/js/app.js`: chat input, API request, and message rendering.

---

## Repository Structure

```text
GHOST/
├── main.py
├── GHOST.md
├── readme.md
├── ghost_mcp/
│   ├── browser/
│   │   ├── client.py
│   │   └── server.py
│   ├── filesystem/
│   │   ├── client.py
│   │   └── server.py
│   ├── formatter.py
│   ├── manager.py
│   ├── router.py
│   └── tool_prompt.py
├── templates/
│   ├── index.html
│   └── index_v2.html
└── static/
    ├── css/
    │   ├── core/
    │   ├── layout/
    │   ├── components/
    │   └── pages/
    ├── js/
    │   ├── app.js
    │   ├── navigation.js
    │   ├── pages.js
    │   └── page-specific modules (work in progress)
    ├── script.js
    └── style.css
```

Runtime data such as the SQLite database, uploaded PDFs, and workspace files is generated locally and is not part of the tracked source tree. See `.gitignore` for ignored runtime paths.

---

## API Reference

The following routes are currently defined in `main.py`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the UI v2 page |
| GET | `/version` | Return backend version and primary model |
| POST | `/chat` | Process a chat message and return a reply |
| POST | `/clear` | Clear stored chat history |
| POST | `/upload-pdf` | Upload, extract, chunk, and embed a PDF |
| GET | `/documents` | List indexed document filenames |
| POST | `/delete-document` | Delete a document and its indexed chunks |
| POST | `/add-task` | Add a task |
| GET | `/tasks` | List tasks |
| POST | `/complete-task` | Toggle a task's completion state |
| POST | `/delete-task` | Delete a task |
| GET | `/stats` | Return document, chunk, and task counts |

### Request Examples

Chat:

```json
{
  "text": "Hello GHOST"
}
```

Add task:

```json
{
  "task": "Review the GHOST roadmap"
}
```

Complete or delete task:

```json
{
  "id": 1
}
```

Document deletion accepts a `filename` query parameter.

---

## Local Setup

### Prerequisites

- Python
- [Ollama](https://ollama.com/) installed and running
- The following Ollama models:
  - `qwen3:8b`
  - `qwen3:0.6b`
  - `nomic-embed-text`

Pull the models:

```bash
ollama pull qwen3:8b
ollama pull qwen3:0.6b
ollama pull nomic-embed-text
```

### Install Python Dependencies

The repository currently does not include a dependency lockfile or requirements file. Install the packages imported by the application and MCP servers:

```bash
pip install fastapi uvicorn jinja2 python-multipart pypdf langchain-text-splitters faiss-cpu numpy ollama mcp requests beautifulsoup4
```

### Prepare Runtime Directories

The PDF upload route writes files under `data/documents/`. Create that directory before uploading PDFs:

```bash
mkdir -p data/documents
```

The filesystem MCP server creates its workspace directory when it starts. Review the configured `PROJECTS_ROOT` path in `ghost_mcp/filesystem/server.py` if you intend to use the projects location.

### Run GHOST

From the repository root:

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Make sure Ollama is running and the required models are available before starting chat, memory extraction, embedding, or tool-routing operations.

---

## Current Limitations and Next Steps

The following are visible gaps between the current code and the broader GHOST vision:

- Connect UI v2 dashboard cards to live backend data instead of hardcoded sample values.
- Build functional Knowledge, Files, Tasks, Brain, Developer, and Settings interactions.
- Split frontend behavior into the planned page-specific JavaScript modules.
- Resolve the `search_file` / `search_files` MCP tool-name mismatch.
- Complete consistent formatting and handling for all MCP tool results.
- Add a dependency manifest with pinned, tested package versions.
- Reconcile the UI/project v0.5 label with the backend `GHOST_VERSION` value.
- Expand the Browser MCP beyond direct URL fetching if web search is required.
- Add automated tests for API routes, RAG ingestion/retrieval, memory, and MCP tool execution.
- Continue toward source citations, richer memory/knowledge representations, and agentic workflows.

---

## Development Direction

GHOST is being developed around four connected capabilities:

1. **Conversation** — a persistent interface for interacting with the assistant.
2. **Knowledge** — document ingestion, embeddings, retrieval, and source-aware answers.
3. **Memory** — durable user context stored locally.
4. **Tools** — controlled interaction with files and web pages through MCP.

The immediate engineering focus is to connect the existing UI v2 pages to real backend functionality, strengthen the integration boundaries, and make the current capabilities reliable before expanding the system's agentic features.
