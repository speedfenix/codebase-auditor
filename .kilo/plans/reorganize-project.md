# Project Reorganization Plan

This plan proposes an optimized directory structure for `codebase-auditor` to separate tool logic, target code, generated reports/outputs, and documentation assets.

## Current Layout (Flat and Mixed)
Currently, all scripts (initialization, ingestion, standard audit, and agentic graph-based audit), output reports (`.json`, `.md`), and media assets are mixed together at the root:
```
/home/fca/codebase-auditor/
├── agent_graph.py
├── audit_report.json
├── audit.py
├── CheatSheetCommands.notes
├── Gemini_Generated_Image_5pligq5pligq5pli.png
├── graph_audit_report.json
├── handshake.py
├── ingest.py
├── init_db.py
├── mock_project/              <-- Targets to audit
│   ├── auth.py
│   └── payment.py
└── remediation_patch.md
```

---

## Proposed Reorganized Structure

We propose organizing the workspace into clear, functional directories:

```
/home/fca/codebase-auditor/
├── src/                       <-- Core execution & auditing engine logic
│   ├── agents/
│   │   └── agent_graph.py     <-- LangGraph agentic audit logic
│   ├── db/
│   │   └── init_db.py         <-- DB initialization script
│   ├── audit.py               <-- Standard audit script
│   ├── ingest.py              <-- Ingestion/Indexing logic
│   └── handshake.py           <-- Basic API handshake verification
│
├── targets/                   <-- Target codebases to be audited (previously mock_project)
│   └── mock_project/
│       ├── auth.py
│       └── payment.py
│
├── reports/                   <-- Generated audit outputs, patches, and logs
│   ├── audit_report.json
│   ├── graph_audit_report.json
│   └── remediation_patch.md
│
├── docs/                      <-- Documentation, diagrams, cheatsheets, and media
│   ├── assets/
│   │   └── Gemini_Generated_Image_5pligq5pligq5pli.png
│   └── CheatSheetCommands.notes
│
├── README.md
├── .gitignore
└── codebaseAuditor.code-workspace
```

### Key Benefits
1. **Clear Separation of Concerns**: Isolates the *auditor tool* codebase (`src/`) from the *target codebases* under audit (`targets/`).
2. **Clean Output Management**: Keeps the root directory clean by centralizing all generated artifacts and patches inside `reports/`.
3. **Structured Documentation**: Keeps the root uncluttered by moving notes and media assets into `docs/`.

---

## Migration Steps (Non-destructive)
1. **Create Directories**: Create `src/`, `src/agents/`, `src/db/`, `targets/`, `reports/`, and `docs/assets/`.
2. **Move Source Files**: Move Python scripts into their respective directories under `src/`.
3. **Move Mock Projects**: Relocate `mock_project/` under `targets/`.
4. **Move Outputs**: Relocate output JSON and markdown files to `reports/`.
5. **Move Assets**: Move generated images and development notes into `docs/`.
6. **Update Code References**: Carefully update path references in python scripts (such as file paths pointing to target codebase `mock_project`, output paths, database ports/hosts, or module imports).
7. **Test & Verify**: Run `init_db.py`, `ingest.py`, `audit.py`, and `agent_graph.py` to confirm everything still works end-to-end.
