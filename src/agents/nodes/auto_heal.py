import os
import time
from google.genai import types
from typing import Dict, Any
from src.agents.clients import ai_client

def auto_heal_node(state: Dict[str, Any]) -> dict:
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