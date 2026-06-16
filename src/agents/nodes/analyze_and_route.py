import os
import json
import time
from google.genai import types
from src.agents.state import HealerState, SecurityAuditReport
from src.agents.clients import ai_client

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