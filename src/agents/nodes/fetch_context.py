from src.agents.state import HealerState
from src.agents.clients import client

def fetch_context_node(state: HealerState) -> dict:
    print("\n🔍 [NODE 1] Scrolling Vector DB space for codebase context...")
    collection_name = "local_codebase"
    results = client.scroll(collection_name=collection_name, limit=10, with_payload=True)[0]
    
    chunks = []
    for point in results:
        if "code_chunk" in point.payload and "file_path" in point.payload:
            db_path = point.payload["file_path"]
            header = f"--- FILE: {db_path} ---"
            chunks.append(f"{header}\n{point.payload['code_chunk']}")
            
    print(f"📥 Pulled {len(chunks)} context segments with database-mapped paths into memory.")
    return {"context_chunks": chunks, "execution_history": ["Context fetched from DB"]}