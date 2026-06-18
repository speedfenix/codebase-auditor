# Architectural Blueprint: Production-Grade Autonomous Codebase Security Auditor & Auto-Healer

## 1. System Design Goals
* **Target Hardware:** Local deployment on Gmktec MiniPC (optimized for multi-threaded Docker container workloads).
* **Execution Paradigm:** Stateless, event-driven agentic state-graph with long-lived human-in-the-loop (HITL) gates.
* **Core Framework:** LangGraph for execution orchestration and state snapshot management.
* **Storage Engine:** Consolidated Single-DB architecture (PostgreSQL + `pgvector`). All polyglot database complexity (e.g., separate vector DB engines) is discarded to eliminate transactional sync issues, data-drift, and infrastructure friction.

---

## 2. Infrastructure & Single-DB Persistence Layout

The entire pipeline operates under a single PostgreSQL instance utilizing the `pgvector` extension with highly optimized HNSW (Hierarchical Navigable Small World) indexing for semantic lookups. This unified system manages both long-term semantic context and transactional application state.

### Relational Schema Blueprint

```sql
-- Enable the vector engine extension
CREATE EXTENSION IF NOT EXISTS pgvector;

-- 1. Immutable Trunk Repository Context (Populated during Ingestion)
CREATE TABLE repo_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id VARCHAR(255) NOT NULL,
    branch_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    ast_hash VARCHAR(64) NOT NULL, -- Used for idempotent delta-syncing
    code_chunk TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL, -- Vector scale matched to target LLM (e.g., 1536 for OpenAI/Gemini)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ON repo_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_repo_file ON repo_chunks (repo_id, file_path);

-- 2. Durable App State Store for Long-Lived Human Interrupt Loops
-- This maps directly to LangGraph's native PostgresSaver schema requirements
CREATE TABLE graph_checkpoints (
    thread_id VARCHAR(255) NOT NULL,
    checkpoint_id VARCHAR(255) NOT NULL,
    checkpoint_data BYTEA NOT NULL, -- Serialized HealerState matrix
    metadata JSONB,
    parent_id VARCHAR(255),
    PRIMARY KEY (thread_id, checkpoint_id)
);
```

---

## 3. Core App State Definition (`HealerState`)

The LangGraph memory layout transitions away from destructive file system modifications to an **in-memory staging matrix**. This allows multi-day user interventions without freezing active operating system compute threads.

```python
from typing import List, Dict, Any, TypedDict

class HealerState(TypedDict):
    # Context Processing Layer
    context_chunks: List[str]            # Extracted semantic raw data elements
    findings: List[Dict[str, Any]]        # Generated structured code vulnerability findings
    
    # Queue Routing Parameters
    pending_files: List[str]             # Files remaining in the active processing queue
    current_file: str                    # Target file undergoing active remediation surgery
    execution_history: List[str]         # Step-by-step transaction log for audit trail tracing
    
    # Virtual Staging Layer for User Intervention
    proposed_patches: Dict[str, str]     # Key: file_path -> Value: Refactored, safe code string
    human_verdict: Dict[str, bool]       # Key: file_path -> Value: True (Accept) / False (Reject)
```

---

## 4. The End-to-End Pipeline Workflow

```
[ Control Plane Dashboard ] ──► Trigger Ingestion ──► In-Memory Context-Shadow Loop
                                                                │
                                                                ▼
   [ Automated Git PR ] ◄── Apply Approved Patches ◄── ⏸️ Breakpoint Interrupt (Postgres Save)
```

### Phase 1: Interactive Control Plane & Delta Ingestion (HITL Gate 1)
1. **User Trigger:** A human interacts with a dashboard UI or CLI tool running on the MiniPC, selects a target GitHub repository, and sets the scope.
2. **Idempotent Syncing:** The ingestion worker evaluates the repository files. It generates Abstract Syntax Tree (AST) hashes for code blocks and checks them against the database. Only missing or modified chunks are sent to the embedding models and written to `repo_chunks`.
3. **Graph Instantiation:** The application boots the LangGraph session under a unique, tracking `thread_id` and passes processing priority to the runtime engine.

### Phase 2: The In-Memory Context-Shadow Loop (Preventing Data-Drift)
1. To prevent the system from using stale data during deep multi-file updates, the vector database remains completely **read-only** during execution.
2. When `fetch_context_node` retrieves relevant code blocks from `repo_chunks`, it performs a quick lookup against the current state's `proposed_patches`.
3. If an agent node has already modified an upstream dependency during this run, the old code snippet is dropped in application memory, and the fresh, uncommitted patch string is injected before the payload reaches the LLM.

### Phase 3: Durable State Interruption & Multi-Day Resiliency (HITL Gate 2)
1. Once the queue controller confirms that `pending_files` is completely empty, the graph routes the session execution into a dedicated check node compiled with a hard breakpoint:
   ```python
   # Compilation configuration ensuring zero compute lock up during human review
   app = workflow.compile(
       checkpointer=PostgresSaver(conn_pool),
       interrupt_before=["apply_approved_patches_node"]
   )
   ```
2. **Total Resource De-allocation:** The graph hits the breakpoint, dumps the `HealerState` payload directly into the `graph_checkpoints` table in PostgreSQL, and closes the active engine thread. Compute consumption drops to 0% CPU and 0MB RAM.
3. **Incremental Interventions:** The human reviewer can open the web UI hours or days later. As they toggle through side-by-side diffs, selecting **Accept** or **Reject**, the UI fires stateless `POST` requests that directly patch the `human_verdict` ledger key within the database checkpoint row.
4. **Seamless Recovery:** When the human hits "Submit Final Changes," the server wakes up, pulls the current ledger state using the session `thread_id`, and resumes execution right where the user left it.

### Phase 4: Clean Git Automation Gateway
1. The final node `apply_approved_patches_node` executes exactly once.
2. It loops through the `human_verdict` directory, drops any rejected items, and applies the approved `proposed_patches` text over a temporary branch (e.g., `security/patch-session-xxx`).
3. It pushes the branch back to the remote server and automatically creates a clean, structured Pull Request via the GitHub API for final engineering review.

---

## 5. Implementation Roadmap for Next Session
1. **Docker Setup:** Configure a local `docker-compose.yml` for PostgreSQL featuring the `pgvector` container image.
2. **LangGraph Schema Setup:** Implement the database checkpointer using `langgraph.checkpoint.postgres`.
3. **Context Switch Node Refactoring:** Re-engineer the application logic to intercept raw text queries and apply the virtual data shadows before they hit the LLM context layer.