# Local Codebase Auditor (Hybrid AI Agent)

An enterprise-grade, state-driven AI agent designed to audit local source repositories for security vulnerabilities, architectural flaws, and unhandled exceptions. This project transitions traditional software engineering methodologies into probabilistic, agentic AI patterns.

## 🏗️ Architecture Blueprint

This system utilizes a **Hybrid AI Architecture** engineered to maximize local data sovereignty and security while eliminating high computational RAM overhead on consumer hardware:

1. **Local Orchestration:** Python backend powered by `LangGraph` managing state machines and cyclic self-correction agent loops.
2. **Local Vector Workspace:** A lightweight `Qdrant` Vector Database engine containerized via native Docker on Linux to map and search semantic code chunks.
3. **Cloud Inference Brain:** Secure API plumbing routing abstract semantic contexts up to Google Cloud's `gemini-2.5-flash` model via Google AI Studio for zero-RAM logic processing.

Local Source Code ] ──► [ Vectorized Embeddings ] ──► [ Local Qdrant Docker Container ]
▲
│ Context Queries
▼
[ Google AI Studio Key ] ──► [ Python LangGraph Controller ] ◄───────┘
│
▼
[ Evaluated Structural JSON Output ]


## 🛠️ Tech Stack & Dependencies

- **Language Engine:** Python 3.10+
- **Agent Orchestration:** LangGraph
- **Database Infrastructure:** Qdrant (Running natively in Docker)
- **Model Inference Provider:** Google Gen AI SDK (`gemini-2.5-flash`)
- **Data Validation Layer:** Pydantic v2

## 🚀 Getting Started (Local Development Setup)

### 1. Initialize Infrastructure
Ensure the native Linux Docker daemon is running, then spin up the lightweight vector storage container:
```bash
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant

### 2. Configure Environment & Keys
Isolate your package manager and configure your secure runtime credentials inside your terminal context:

Bash
python3 -m venv venv
source venv/bin/activate
pip install langgraph google-genai qdrant-client pydantic langchain-community

# Inject your Google AI Studio access token
export GEMINI_API_KEY="your-api-key-here"
### 3. Verify System Handshake
Execute the Day 1 connectivity script to perform a cross-network handshake between your local environment, the Qdrant instance, and Google's TPUs:

Bash
python handshake.py


📅 Development Roadmap
[x] Day 1: Environment architecture virtualization, Docker network bridging, and cloud handshake logic.

[ ] Day 2: Text splitting, local directory token parsing, and hierarchical code chunk indexing.

[ ] Day 3: Structured schema output forcing via validation barriers.

[ ] Day 4: Graph state routing rules and system loops.

[ ] Day 5: Agent tool registration for context-aware injection.

[ ] Day 6: Algorithmic self-correction circuits and evaluation loops.

[ ] Day 7: System diagnostics, edge case processing, and markdown reporter builds.
