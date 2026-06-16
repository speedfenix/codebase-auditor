import os
import sys
import json
import time
from typing import List, TypedDict
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from langgraph.graph import StateGraph, END
from qdrant_client import QdrantClient

# =====================================================================
# 1. AGENT STATE MATRIX
# =====================================================================
class HealerState(TypedDict):
    context_chunks: List[str]
    findings: List[dict]          
    pending_files: List[str]      
    current_file: str             
    execution_history: List[str]  

class CodeFlaw(BaseModel):
    file_path: str = Field(description="The name or path of the source file analyzed.")
    severity: str = Field(description="CRITICAL, MEDIUM, or LOW based on impact.")
    explanation: str = Field(description="Clear breakdown of the security vulnerability.")

class SecurityAuditReport(BaseModel):
    findings: List[CodeFlaw]

client = QdrantClient(host="localhost", port=6333)
ai_client = genai.Client()

# =====================================================================
# 2. GRAPH NODE IMPLEMENTATIONS
# =====================================================================

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

def analyze_and_route_node(state: HealerState) -> dict:
    print("\n🧠 [NODE 2] Dispatching consolidated context window to Reasoning Engine...")
    combined_context = "\n\n".join(state["context_chunks"])
    
    system_instruction = (
        "You are an elite automated security auditor. Analyze the provided codebase segments. "
        "Extract all flaws. Return a structured JSON matching the provided schema."
    )
    
    max_retries = 5
    delay = 4  
    response = None
    
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Analyze this code context for critical security vulnerabilities:\n\n{combined_context}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=SecurityAuditReport,
                    temperature=0.1
                )
            )
            break  
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"⚠️  [503 High Demand] Google endpoints are congested at Node 2. Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  
            else:
                raise e  
                
    if not response:
        raise RuntimeError("Google API capacity limits exhausted. Server is completely unavailable.")
    
    report_data = json.loads(response.text)
    all_findings = report_data.get('findings', [])
    print(f"📊 Auditor identified {len(all_findings)} security issues across the codebase.")
    
    critical_files = []
    for f in all_findings:
        filename = os.path.basename(f['file_path'])
        normalized_path = os.path.join("./targets/mock_project", filename)
        
        f['file_path'] = normalized_path
        
        if f['severity'].upper() == 'CRITICAL':
            critical_files.append(normalized_path)
            
    critical_files = list(set(critical_files))
    
    print(f"🚨 Queue established: {len(critical_files)} unique targets mapped to execution directory.")
    for f in critical_files:
        print(f"  -> Target Queue: {f}")
        
    return {
        "findings": all_findings, 
        "pending_files": critical_files,
        "execution_history": ["Codebase vulnerabilities analyzed and normalized"]
    }

def select_next_target_node(state: HealerState) -> dict:
    queue = state.get("pending_files", [])
    if not queue:
        return {"current_file": ""}
    
    next_target = queue[0]
    remaining_queue = queue[1:]
    
    print(f"\n🔄 [QUEUE CONTROLLER] {len(queue)} items left. Popping '{next_target}' into active memory.")
    return {"current_file": next_target, "pending_files": remaining_queue}

def auto_heal_node(state: HealerState) -> dict:
    target = state["current_file"]
    
    if not target.startswith("./targets/mock_project/"):
        target = os.path.join("./targets/mock_project", os.path.basename(target))
        
    print(f"\n🚨 [NODE 3] Entering automated surgery room for: '{target}'")
    
    flaw_desc = next((f['explanation'] for f in state["findings"] if f['file_path'] == target), "Critical security flaw detected.")
    
    with open(target, "r") as f:
        broken_code = f.read()
        
    prompt = f"""You are a senior secure engineer. Rewrite the following source file to COMPLETELY eliminate the security vulnerability described.
    
    TARGET FILE: {target}
    VULNERABILITY DESCRIPTION: {flaw_desc}
    
    CURRENT SOURCE CODE:
    ```python
    {broken_code}
    ```
    
    Output ONLY valid, functional python code. Do not include markdown code block syntax formatting or explanations."""

    # 🛡️ THE FIX: Add an identical resilience layer to Node 3 to catch surgery-phase spikes
    max_retries = 5
    delay = 4  
    response = None
    
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            break  
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"⚠️  [503 High Demand] Google endpoints are congested at Node 3 surgery room. Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  
            else:
                raise e  

    if not response:
        raise RuntimeError("Google API capacity limits exhausted during active file surgery remediation loops.")

    cleaned_code = response.text.replace("```python", "").replace("```", "").strip()
    
    print(f"💾 Dispatched OS tool: Writing safe code block over resource '{target}'...")
    with open(target, "w") as f:
        f.write(cleaned_code)
        
    print(f"🟢 Remediation successful for: {target}")
    return {"execution_history": [f"Successfully patched file system asset: {target}"]}

# =====================================================================
# 3. ROUTER EDGE LOGIC (READ-ONLY)
# =====================================================================
def route_after_queue_check(state: HealerState):
    if not state.get("current_file"):
        print("\n🎉 All critical files successfully processed. Halting graph loop runtime.")
        return "complete"
    return "continue"

# =====================================================================
# 4. GRAPH PIPELINE ASSEMBLY
# =====================================================================
workflow = StateGraph(HealerState)

workflow.add_node("fetch_context", fetch_context_node)
workflow.add_node("analyze_route", analyze_and_route_node)
workflow.add_node("select_next_target", select_next_target_node)
workflow.add_node("auto_heal_node", auto_heal_node)

workflow.set_entry_point("fetch_context")
workflow.add_edge("fetch_context", "analyze_route")
workflow.add_edge("analyze_route", "select_next_target")

workflow.add_conditional_edges(
    "select_next_target",
    route_after_queue_check,
    {
        "continue": "auto_heal_node",
        "complete": END
    }
)

workflow.add_edge("auto_heal_node", "select_next_target")

app = workflow.compile()

# =====================================================================
# 5. EXECUTION ENTRYPOINT WITH TRACEBACK SUPPRESSION
# =====================================================================
if __name__ == "__main__":
    print("🚀 Booting localized autonomous multi-file self-healing cycle...")
    initial_state = {
        "context_chunks": [],
        "findings": [],
        "pending_files": [],
        "current_file": "",
        "execution_history": []
    }
    
    try:
        app.invoke(initial_state)
    except Exception as e:
        print("\n" + "="*70)
        print("🛑 GRAPH EXECUTION TERMINATED: Runtime Error Encountered")
        print("="*70)
        
        err_msg = str(e)
        if "503" in err_msg or "UNAVAILABLE" in err_msg:
            print("🚨 Upstream infrastructure error: Google's Gemini API is currently over-capacity.")
            print("👉 Fix: Wait a few moments for the traffic spike to subside and re-run.")
        elif "FileNotFoundError" in err_msg or "No such file" in err_msg:
            print("🚨 Local target resource error: A file path operation failed.")
            print(f"👉 Details: {err_msg}")
        elif "Connection refused" in err_msg or "6333" in err_msg:
            print("🚨 Database connection error: Unable to talk to the local Qdrant container instance.")
            print("👉 Fix: Ensure your database daemon is active (`docker start qdrant`).")
        else:
            print("🚨 An unexpected failure occurred inside the state orchestration nodes.")
            print(f"👉 Error Message: {err_msg}")
            
        print("-"*70)
        print("💡 Traceback noise suppressed. Run with debugging flags enabled if deep analysis is required.")
        print("="*70 + "\n")
        sys.exit(1)