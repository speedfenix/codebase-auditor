import os
import json
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from google.genai.errors import APIError
from qdrant_client import QdrantClient

# ==========================================
# 1. DEFINE THE VALIDATION BARRIER (SCHEMA)
# ==========================================
class AuditFinding(BaseModel):
    vulnerability_type: str = Field(description="Category of the flaw (e.g., SQL Injection, Hardcoded Secret, Blind Exception Handling)")
    severity: str = Field(description="Classification level: CRITICAL, HIGH, MEDIUM, LOW")
    file_path: str = Field(description="The source file location of the bug")
    flawed_code: str = Field(description="The exact string or snippet of code containing the issue")
    explanation: str = Field(description="Deep architectural analysis of why this code is dangerous")
    remediation: str = Field(description="The complete, corrected code snippet showing how to secure it")

class CodebaseAuditReport(BaseModel):
    project_summary: str = Field(description="A high-level sentence summarizing the posture of the audited code")
    findings: List[AuditFinding] = Field(description="Collection of structured flaw models found during semantic indexing")

# ==========================================
# 2. RUNTIME LOGIC
# ==========================================
def main():
    print("🧠 Starting Day 3: Structured Extraction & Validation Barriers...")
    
    # Init local and cloud connectors
    ai_client = genai.Client()
    db_client = QdrantClient(host="localhost", port=6333)
    collection_name = "local_codebase"

    # Fetch your vectors out of your local Qdrant container
    print("📥 Retrieving vectorized code context records from local Qdrant...")
    scroll_result, _ = db_client.scroll(
        collection_name=collection_name,
        with_payload=True,
        with_vectors=False,
        limit=10
    )
    
    if not scroll_result:
        print("❌ No context data points discovered. Run ingest.py first!")
        return

    # Compile the code fragments into an aggregated payload context
    context_accumulator = []
    for point in scroll_result:
        context_accumulator.append(
            f"--- FILE: {point.payload['file_path']} ---\n{point.payload['text']}\n"
        )
    
    full_codebase_context = "\n".join(context_accumulator)
    
    # Design the system prompt targeting zero conversational leak
    prompt = f"""
    You are an elite, defensive AppSec Static Analysis Agent. 
    Analyze the provided codebase context for structural vulnerabilities, syntax oversights, and data isolation flaws.
    
    CODEBASE CONTEXT FOR AUDIT:
    {full_codebase_context}
    """

    print("🚀 Passing context through Gemini Cloud Verification barriers...")
    
    # Call Gemini, forcing the response to conform strictly to our Pydantic layout
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CodebaseAuditReport, # The validation barrier injection
                temperature=0.1 # Drop temperature to ensure deterministic output
            ),
        )
    except APIError as e:
        if e.code == 503:
            print("❌ LLM API Error 503: The model is currently experiencing high demand. Please try again later.")
        else:
            print(f"❌ LLM API Error ({e.code}): {e.message}")
        return
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return

    # 3. PRINT THE STRUCTURAL RESULT
    print("🟢 SUCCESS! Structured Validation Complete.\n")
    
    # The output is guaranteed to be clean JSON matching our exact model structure
    raw_json_string = response.text
    parsed_report = json.loads(raw_json_string)
    
    print(json.dumps(parsed_report, indent=2))
    
    # Save the output file locally for day 7 reporting
    with open("audit_report.json", "w") as f:
        f.write(raw_json_string)
    print("\n💾 Formatted blueprint outputted safely to 'audit_report.json'")

if __name__ == "__main__":
    main()
