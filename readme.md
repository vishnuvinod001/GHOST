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

The root route (`GET /`) serves `templates/index_v2.html`. The legacy interface remains in `templates/index.html` with its original `static/script.js` implementation.

The UI v2 shell has three persistent regions:

- **Sidebar:** navigation between the seven workspace pages.
- **Workspace:** page-specific dashboards populated from the FastAPI API.
- **Chat panel:** persistent chat interface connected to the existing `POST /chat` route.

### Workspace Pages

| Page | Current implementation |
|---|---|
| Overview | Live document, memory, task, and knowledge counts plus backend/index/MCP configuration status |
| Knowledge | Indexed documents, chunk and embedding counts, and FAISS index state |
| Files | PDF document listing, PDF upload, and document deletion through the existing knowledge API |
| Tasks | SQLite-backed task listing, creation, completion toggling, and deletion |
| Brain | Saved memory records and counts grouped by memory type |
| Developer | Backend/model diagnostics and storage/index counts |
| Settings | Read-only view of the model, router, version, index, and MCP configuration exposed by the backend |

Page navigation loads the corresponding page module from `static/js/`. Shared rendering helpers live in `static/js/pages.js`; API requests are centralized in `static/js/api.js`; navigation and page actions are managed by `static/js/navigation.js`. Chat remains in `static/js/app.js` and sends messages to the existing `POST /chat` route.

**Frontend status:** UI v2 is connected to the current backend data for its available features. Dashboard counts are sourced from SQLite-backed API responses rather than sample values. The page modules are loaded by `templates/index_v2.html`. Non-card page sections use restrained reveal motion; metric cards are not animated. Chat rendering uses text nodes so user and model text is not inserted as raw HTML.

**Scope note:** the Files page manages indexed PDF documents, not arbitrary files in the Filesystem MCP workspace. The backend does not yet expose a general workspace file-list endpoint. Developer diagnostics report MCP configuration, not a live process-health probe. Settings are intentionally read-only because model switching and settings mutation APIs are not implemented.

### Frontend Structure

- `static/css/core/`: design tokens, global styles, motion, and responsive rules.
- `static/css/layout/`: application layout.
- `static/css/components/`: sidebar, workspace, chat, and reusable data cards.
- `static/css/pages/`: page-specific styles.
- `static/js/api.js`: shared GET, POST, and multipart-upload requests.
- `static/js/pages.js`: safe rendering helpers for page content.
- `static/js/overview.js`, `knowledge.js`, `files.js`, `tasks.js`, `brain.js`, `developer.js`, `settings.js`: page-specific data loading and rendering.
- `static/js/navigation.js`: client-side navigation, motion observation, and delegated page actions.
- `static/js/app.js`: chat input, request to `POST /chat`, and safe message rendering.

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
    │   ├── api.js
    │   ├── app.js
    │   ├── brain.js
    │   ├── developer.js
    │   ├── files.js
    │   ├── knowledge.js
    │   ├── navigation.js
    │   ├── overview.js
    │   ├── pages.js
    │   ├── settings.js
    │   └── tasks.js
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
| GET | `/version` | Return backend version, primary model, and configured router model |
| POST | `/chat` | Process a chat message and return a reply |
| POST | `/clear` | Clear stored chat history |
| POST | `/upload-pdf` | Upload, extract, chunk, and embed a PDF |
| GET | `/documents` | List indexed document filenames |
| POST | `/delete-document` | Delete a document and its indexed chunks |
| GET | `/memories` | List stored long-term memory records |
| POST | `/add-task` | Add a task |
| GET | `/tasks` | List tasks |
| POST | `/complete-task` | Toggle a task's completion state |
| POST | `/delete-task` | Delete a task |
| GET | `/stats` | Return document, chunk, embedding, memory, and task counts |
| GET | `/diagnostics` | Return backend, FAISS, and MCP configuration status |

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

- Add a general workspace file-list API so the Files page can browse arbitrary Filesystem MCP content, not only indexed PDFs.
- Add live MCP process-health checks instead of reporting configuration only.
- Add backend settings endpoints if runtime model switching and editable system preferences are required.
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
